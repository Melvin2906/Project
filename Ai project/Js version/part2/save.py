# init_db.py
import sqlite3

conn = sqlite3.connect("history.db")
c = conn.cursor()

# Active FTS5
c.execute("""
CREATE VIRTUAL TABLE IF NOT EXISTS history_fts
USING fts5(question, content='');
""")

conn.commit()
conn.close()
