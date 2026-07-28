import sqlite3
import re

DB_NAME = "history.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Crée les tables si elles n'existent pas encore. A appeler au démarrage du serveur."""
    conn = get_db_connection()
    conn.executescript(
        """
        -- Recherche de questions fréquentes (suggestions) --
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            normalized TEXT NOT NULL UNIQUE,
            count INTEGER NOT NULL DEFAULT 1,
            last_asked TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE VIRTUAL TABLE IF NOT EXISTS questions_fts USING fts5(
            question,
            content='questions',
            content_rowid='id'
        );

        CREATE TRIGGER IF NOT EXISTS questions_ai AFTER INSERT ON questions BEGIN
            INSERT INTO questions_fts(rowid, question) VALUES (new.id, new.question);
        END;

        CREATE TRIGGER IF NOT EXISTS questions_ad AFTER DELETE ON questions BEGIN
            INSERT INTO questions_fts(questions_fts, rowid, question) VALUES ('delete', old.id, old.question);
        END;

        CREATE TRIGGER IF NOT EXISTS questions_au AFTER UPDATE ON questions BEGIN
            INSERT INTO questions_fts(questions_fts, rowid, question) VALUES ('delete', old.id, old.question);
            INSERT INTO questions_fts(rowid, question) VALUES (new.id, new.question);
        END;

        -- Historique des conversations --
        -- user_id référence l'id utilisateur du serveur Node/MySQL (dans le
        -- token JWT), pas une table locale : les comptes vivent uniquement
        -- côté Node, cette DB ne fait que stocker les conversations.
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL DEFAULT 'Nouvelle conversation',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.commit()
    conn.close()


def _normalize(question):
    return re.sub(r"\s+", " ", question.strip().lower())


def record_question(question):
    original = question.strip()
    normalized = _normalize(original)
    if not normalized:
        return

    conn = get_db_connection()
    row = conn.execute(
        "SELECT id FROM questions WHERE normalized = ?", (normalized,)
    ).fetchone()

    if row:
        conn.execute(
            "UPDATE questions SET count = count + 1, last_asked = CURRENT_TIMESTAMP WHERE id = ?",
            (row["id"],),
        )
    else:
        conn.execute(
            "INSERT INTO questions (question, normalized) VALUES (?, ?)",
            (original, normalized),
        )
    conn.commit()
    conn.close()


def suggest(query, limit=5):
    query = query.strip()
    if not query:
        return []

    conn = get_db_connection()
    rows = conn.execute(
        """
        SELECT q.question, q.count, bm25(questions_fts) AS rank
        FROM questions_fts
        JOIN questions q ON q.id = questions_fts.rowid
        WHERE questions_fts MATCH ?
        ORDER BY rank ASC, q.count DESC
        LIMIT ?
        """,
        (query + "*", limit),
    ).fetchall()
    conn.close()

    return [row["question"] for row in rows]


def create_conversation(user_id, title="Nouvelle conversation"):
    conn = get_db_connection()
    cur = conn.execute(
        "INSERT INTO conversations (user_id, title) VALUES (?, ?)", (user_id, title)
    )
    conn.commit()
    conv_id = cur.lastrowid
    conn.close()
    return conv_id


def list_conversations(user_id):
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT id, title, created_at FROM conversations WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_conversation(conversation_id):
    conn = get_db_connection()
    row = conn.execute(
        "SELECT * FROM conversations WHERE id = ?", (conversation_id,)
    ).fetchone()
    conn.close()
    return row


def delete_conversation(conversation_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
    conn.commit()
    conn.close()

def add_message(conversation_id, role, content):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
        (conversation_id, role, content),
    )
    conn.commit()
    conn.close()


def get_messages(conversation_id):
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT role, content, created_at FROM messages WHERE conversation_id = ? ORDER BY id ASC",
        (conversation_id,),
    ).fetchall()
    conn.close()
    return [{"role": row["role"], "content": row["content"]} for row in rows]
