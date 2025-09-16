from flask import Flask, request, jsonify
from flask_cors import CORS
from configparser import ConfigParser
from chat_bot_using_gemini import ChatBot

# Charger la clé API
config = ConfigParser()
config.read("C:/Users/Utilisateur/Project/Ai project/Python version/Gemini.ini")
api_key = config['gemini_ai']['API_KEY']

# Initialiser le chatbot
chatbot = ChatBot(api_key=api_key)
chatbot.start_convertion()

# Créer l'app Flask
app = Flask(__name__)
CORS(app)  # Autorise toutes les origines

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_message = data.get("message", "")
    try:
        response = chatbot.send_prompt(user_message)
        return jsonify({"reply": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Serveur Flask actif. Utilise POST /ask pour parler au bot."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
