from flask import Flask, request, jsonify, session, send_file, g
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from configparser import ConfigParser
from functools import wraps
from chatbot_base import ChatBot
import sugestions as db
import authentification as auth
import io
import os
import secrets

config = ConfigParser()
config.read("Gemini.ini")

api_key = os.environ.get("GEMINI_API_KEY") or config.get("gemini", "api_key", fallback=None)
if not api_key:
    raise RuntimeError(
        "Clé API Gemini manquante : définis la variable d'env GEMINI_API_KEY "
        "ou ajoute-la dans Gemini.ini sous [gemini] api_key=... "
        "(peut être une valeur bidon si tu utilises un LLM local)"
    )

secret_key = os.environ.get("FLASK_SECRET_KEY")
if not secret_key:
    secret_key = secrets.token_hex(32)
    print(
        "ATTENTION: FLASK_SECRET_KEY non défini dans l'environnement, une clé "
        "temporaire a été générée (les sessions seront invalidées à chaque redémarrage)."
    )

chatbot = ChatBot(api_key=api_key)
chatbot.start_convertion()

db.init_db()

app = Flask(__name__)
CORS(app)
app.secret_key = secret_key

limiter = Limiter(get_remote_address, app=app, default_limits=["60 per minute"])

def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authentification requise"}), 401

        token = auth_header.split(" ", 1)[1]
        try:
            payload = auth.decode_token(token)
        except ValueError as e:
            return jsonify({"error": str(e)}), 401

        g.user_id = payload["id"]
        g.username = payload["username"]
        return f(*args, **kwargs)

    return wrapper


def _owned_conversation_or_404(conversation_id):
    """Vérifie que la conversation existe et appartient à l'utilisateur courant."""
    conversation = db.get_conversation(conversation_id)
    if not conversation or conversation["user_id"] != g.user_id:
        return None
    return conversation


@app.route("/conversations", methods=["GET"])
@require_auth
def get_conversations():
    return jsonify(db.list_conversations(g.user_id))


@app.route("/conversations", methods=["POST"])
@require_auth
def create_conversation():
    data = request.json or {}
    title = data.get("title", "Nouvelle conversation")
    conv_id = db.create_conversation(g.user_id, title)
    return jsonify({"id": conv_id, "title": title})


@app.route("/conversations/<int:conv_id>/messages", methods=["GET"])
@require_auth
def get_conversation_messages(conv_id):
    if not _owned_conversation_or_404(conv_id):
        return jsonify({"error": "Conversation introuvable"}), 404
    return jsonify(db.get_messages(conv_id))


@app.route("/conversations/<int:conv_id>", methods=["DELETE"])
@require_auth
def delete_conversation(conv_id):
    if not _owned_conversation_or_404(conv_id):
        return jsonify({"error": "Conversation introuvable"}), 404
    db.delete_conversation(conv_id)
    return jsonify({"status": "ok"})

@app.route("/update-timezone", methods=["POST"])
def update_timezone():
    data = request.json or {}
    timezone = data.get("timezone")

    if not timezone:
        return jsonify({"error": "No timzone provided"}), 400

    session['timezone'] = timezone
    chatbot.update_datetime(timezone=timezone)

    return jsonify({"status": "ok", "timezone": timezone})

@app.route("/ask", methods=["POST"])
@require_auth
@limiter.limit("20 per minute")
def ask():
    data = request.json or {}
    user_message = data.get("message", "")
    conversation_id = data.get("conversation_id")

    if not conversation_id:
        return jsonify({"error": "conversation_id manquant"}), 400

    if not _owned_conversation_or_404(conversation_id):
        return jsonify({"error": "Conversation introuvable"}), 404

    if user_message:
        db.record_question(user_message)

    timezone = session.get("timezone", "UTC")
    context = chatbot.update_datetime(timezone)

    history = db.get_messages(conversation_id)
    full_messages = list(chatbot._conversation_history) + history + [
        {"role": "user", "content": context + user_message}
    ]

    response = chatbot.send_prompt_with_history(full_messages)

    db.add_message(conversation_id, "user", user_message)
    db.add_message(conversation_id, "assistant", response)

    return jsonify({"reply": response, "conversation_id": conversation_id})


@app.route("/ask-image", methods=["POST"])
@require_auth
@limiter.limit("10 per minute")
def ask_image():
    prompt = request.form.get("message", "")
    conversation_id = request.form.get("conversation_id")
    image_file = request.files.get("image")

    if not image_file:
        return jsonify({"error": "No image provided"}), 400
    if not conversation_id or not _owned_conversation_or_404(int(conversation_id)):
        return jsonify({"error": "Conversation introuvable"}), 404

    timezone = session.get("timezone", "UTC")
    context = chatbot.update_datetime(timezone)
    final_message = context + prompt
    image_bytes = image_file.read()
    response = chatbot.send_prompt_with_image(final_message, image_bytes)

    db.add_message(conversation_id, "user", f"[Image envoyée] {prompt}")
    db.add_message(conversation_id, "assistant", response)

    return jsonify({"reply": response})


@app.route("/suggest", methods=["GET"])
def suggest():
    query = request.args.get("q", "")
    return jsonify(db.suggest(query))


@app.route("/generate-image", methods=["POST"])
@require_auth
@limiter.limit("5 per minute")
def create_image():
    data = request.json or {}
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "Prompt manquant"}), 400

    image_bytes = chatbot.generate_image(prompt)

    if image_bytes:
        return send_file(
            io.BytesIO(image_bytes),
            mimetype='image/png',
            as_attachment=False,
            download_name="generated_image.png"
        )
    else:
        return jsonify({"error": "La génération d'image a échoué"}), 500


@app.route("/generate-doc", methods=["POST"])
@require_auth
@limiter.limit("5 per minute")
def generate_doc():
    data = request.json or {}
    prompt = data.get("prompt", "")
    file_type = data.get("type", "pdf")

    if file_type not in ("pdf", "docx", "xlsx"):
        return jsonify({"error": "Type de fichier non supporté"}), 400
    if not prompt:
        return jsonify({"error": "Prompt vide"}), 400

    try:
        file_bytes = chatbot.generate_document(prompt, file_type)

        if file_bytes:
            mime_types = {
                "pdf": "application/pdf",
                "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            }
            return send_file(
                io.BytesIO(file_bytes),
                mimetype=mime_types.get(file_type, "application/octet-stream"),
                as_attachment=True,
                download_name=f"generated_file.{file_type}"
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/ask-document", methods=["POST"])
@require_auth
@limiter.limit("10 per minute")
def ask_document():
    prompt = request.form.get("message", "Analyse ce document")
    conversation_id = request.form.get("conversation_id")
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "Aucun fichier reçu"}), 400
    if not conversation_id or not _owned_conversation_or_404(int(conversation_id)):
        return jsonify({"error": "Conversation introuvable"}), 404

    file_bytes = file.read()
    mime_type = file.content_type
    response = chatbot.read_document(prompt, file_bytes, mime_type)

    db.add_message(conversation_id, "user", f"[Document envoyé] {prompt}")
    db.add_message(conversation_id, "assistant", response)

    return jsonify({"reply": response})


@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Serveur Flask actif. Utilise POST /ask pour parler au bot."})


if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
