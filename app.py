from flask import Flask, jsonify, request, render_template
import sqlite3

app = Flask(__name__)

# Database initialization
def create_tables():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS todo (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS done (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT)''')
    conn.commit()
    conn.close()

create_tables()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks/todo', methods=['GET'])
def get_todo_tasks():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM todo''')
    todo_tasks = [{'id': row[0], 'task': row[1]} for row in c.fetchall()]
    conn.close()
    return jsonify({'tasks': todo_tasks})

@app.route('/api/tasks/done', methods=['GET'])
def get_done_tasks():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM done''')
    done_tasks = [{'id': row[0], 'task': row[1]} for row in c.fetchall()]
    conn.close()
    return jsonify({'tasks': done_tasks})

@app.route('/api/tasks/add', methods=['POST'])
def add_task():
    task_data = request.get_json()
    task = task_data.get('task')
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''INSERT INTO todo (task) VALUES (?)''', (task,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task added successfully'})

@app.route('/api/tasks/move_to_done', methods=['POST'])
def move_to_done():
    task_id = request.get_json().get('id')
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''SELECT task FROM todo WHERE id = ?''', (task_id,))
    task = c.fetchone()
    if task:
        c.execute('''INSERT INTO done (task) VALUES (?)''', (task[0],))
        c.execute('''DELETE FROM todo WHERE id = ?''', (task_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Task moved to Done'})
    conn.close()
    return jsonify({'message': 'Task not found'})

if __name__ == '__main__':
    app.run(debug=True)
