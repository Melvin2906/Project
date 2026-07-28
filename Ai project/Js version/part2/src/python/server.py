from flask import Flask, request, jsonify, session, send_file
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from configparser import ConfigParser
from chatbot_base import ChatBot
import sugestions as db
import io
import os
import secrets

config = ConfigParser()
config.read("Gemini.ini")

api_key = os.environ.get("GEMINI_API_KEY") or config.get("gemini", "api_key", fallback=None)
if not api_key:
    raise RuntimeError(
        "Clé API Gemini manquante : définis la variable d'env GEMINI_API_KEY "
        "ou ajoute-la dans Gemini.ini sous [gemini] api_key=..."
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


@app.route("/update-timezone", methods=["POST"])
def update_timezone():
    data = request.json
    timezone = data.get("timezone")

    if not timezone:
        return jsonify({"error": "No timzone provided"}), 400

    session['timezone'] = timezone
    chatbot.update_datetime(timezone=timezone)

    return jsonify({"status": "ok", "timezone": timezone})


@app.route("/ask", methods=["POST"])
@limiter.limit("20 per minute")
def ask():
    data = request.json
    user_message = data.get("message", "")

    if user_message:
        db.record_question(user_message)

    timezone = session.get("timezone", "UTC")
    context = chatbot.update_datetime(timezone)
    final_prompt = context + user_message

    response = chatbot.send_prompt(final_prompt)
    return jsonify({"reply": response})


@app.route("/ask-image", methods=["POST"])
@limiter.limit("10 per minute")
def ask_image():
    prompt = request.form.get("message", "")
    image_file = request.files.get("image")

    if not image_file:
        return jsonify({"error": "No image provided"}), 400

    timezone = session.get("timezone", "UTC")
    context = chatbot.update_datetime(timezone)
    final_message = context + prompt
    image_bytes = image_file.read()
    response = chatbot.send_prompt_with_image(final_message, image_bytes)

    return jsonify({"reply": response})


@app.route("/suggest", methods=["GET"])
def suggest():
    query = request.args.get("q", "")
    return jsonify(db.suggest(query))


@app.route("/generate-image", methods=["POST"])
@limiter.limit("5 per minute")
def create_image():
    data = request.json
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
@limiter.limit("5 per minute")
def generate_doc():
    data = request.json
    prompt = data.get("prompt", "")
    file_type = data.get("type", "pdf")

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
@limiter.limit("10 per minute")
def ask_document():
    prompt = request.form.get("message", "Analyse ce document")
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "Aucun fichier reçu"}), 400

    file_bytes = file.read()
    mime_type = file.content_type
    response = chatbot.read_document(prompt, file_bytes, mime_type)
    return jsonify({"reply": response})


@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Serveur Flask actif. Utilise POST /ask pour parler au bot."})


if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
