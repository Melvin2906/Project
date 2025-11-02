from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "history.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")

    if question:
        conn = get_db_connection()
        # Insère directement dans la table FTS
        conn.execute("INSERT INTO history_fts (question) VALUES (?)", (question,))
        conn.commit()
        conn.close()

    # Ici tu branches Gemini normalement
    return jsonify({"response": f"Réponse simulée à: {question}"})

@app.route("/suggest", methods=["GET"])
def suggest():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify([])

    conn = get_db_connection()
    # Recherche FTS (full-text search)
    rows = conn.execute(
        "SELECT question FROM history_fts WHERE question MATCH ? LIMIT 5;",
        (query + "*",)  # * = recherche préfixe
    ).fetchall()
    conn.close()

    matches = [row["question"] for row in rows]
    return jsonify(matches)

if __name__ == "__main__":
    app.run(debug=True)
