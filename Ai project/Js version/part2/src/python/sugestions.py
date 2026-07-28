import sqlite3
import re

DB_NAME = "history.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Crée les tables si elles n'existent pas encore. A appeler au démarrage du serveur."""
    conn = get_db_connection()
    conn.executescript(
        """
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
        """
    )
    conn.commit()
    conn.close()


def _normalize(question):
    return re.sub(r"\s+", " ", question.strip().lower())


def record_question(question):
    """Enregistre une question posée par un utilisateur, ou incrémente son
    compteur de popularité si une question équivalente existe déjà (comparaison
    insensible à la casse / espaces)."""
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
    """Retourne les questions les plus 'pertinentes' pour une saisie donnée :
    d'abord par qualité du match texte (bm25, plus bas = meilleur), puis par
    popularité (nombre de fois posée) en cas d'égalité."""
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
