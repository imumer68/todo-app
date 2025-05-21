
from flask import Flask, render_template, request, redirect
import sqlite3, os

app = Flask(__name__)
DB_PATH = os.path.join(app.root_path, 'todos.db')

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        conn.execute('CREATE TABLE todos (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT NOT NULL)')
        conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    if request.method == 'POST':
        todo_text = request.form.get('todo')
        if todo_text:
            conn.execute('INSERT INTO todos (text) VALUES (?)', (todo_text,))
            conn.commit()
        conn.close()
        return redirect('/')
    cursor = conn.execute('SELECT id, text FROM todos ORDER BY id DESC')
    todos = cursor.fetchall()
    conn.close()
    return render_template('index.html', todos=todos)

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete(todo_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    # Listen on all interfaces so App Runner can route to it
    app.run(host='0.0.0.0', port=5000)
