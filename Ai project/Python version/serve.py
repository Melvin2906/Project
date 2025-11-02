from flask import Flask, request, jsonify
from flask_cors import CORS
from configparser import ConfigParser
from chat_bot_using_gemini import ChatBot
import sqlite3

# Charger la clé API
config = ConfigParser()
path = "C:/Users/Utilisateur/Project/Ai project/Python version/Gemini.ini"
config.read(path)
api_key = config['gemini_ai']['API_KEY']

# Initialiser le chatbot
chatbot = ChatBot(api_key=api_key)
chatbot.start_convertion()

# Créer l'app Flask
app = Flask(__name__)
CORS(app)

DB_NAME = "history.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_message = data.get("message", "")
    try:
        # Stocker la question dans l’historique SQLite
        if user_message:
            conn = get_db_connection()
            conn.execute("INSERT INTO history_fts (question) VALUES (?)", (user_message,))
            conn.commit()
            conn.close()

        # Renvoyer la réponse de Gemini
        response = chatbot.send_prompt(user_message)
        return jsonify({"reply": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/suggest", methods=["GET"])
def suggest():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify([])

    conn = get_db_connection()
    rows = conn.execute(
        "SELECT question FROM history_fts WHERE question MATCH ? LIMIT 5;",
        (query + "*",)
    ).fetchall()
    conn.close()

    matches = [row["question"] for row in rows]
    return jsonify(matches)

@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Serveur Flask actif. Utilise POST /ask pour parler au bot."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
