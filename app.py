from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

DB_FILE = os.getenv('DB_FILE', 'notes.db')

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db()

    if request.method == 'POST':
        content = request.form.get('content')

        if not content or len(content.strip()) < 3:
            flash("Note must be at least 3 characters", "error")
            return redirect(url_for('index'))

        conn.execute(
            "INSERT INTO notes (content, timestamp) VALUES (?, ?)",
            (content.strip(), datetime.now().strftime("%Y-%m-%d %H:%M"))
        )
        conn.commit()
        flash("Note added successfully 🚀", "success")

    notes = conn.execute("SELECT * FROM notes ORDER BY id DESC").fetchall()
    conn.close()

    return render_template('index.html', notes=notes)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM notes WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    flash("Note deleted ❌", "success")
    return redirect(url_for('index'))

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)