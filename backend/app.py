from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import pymysql.cursors

app = Flask(__name__)
CORS(app)

# ✅ Create a reusable DB connection function
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='yourpassword',  # 🔁 Replace with your actual MySQL password
        database='taskdb1',
        cursorclass=pymysql.cursors.DictCursor
    )

# ✅ GET all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    conn.close()
    tasks = [{'id': row['id'], 'title': row['title'], 'completed': bool(row['completed'])} for row in rows]
    return jsonify(tasks)

# ✅ POST: Add a task
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    title = data['title']
    completed = int(data.get('completed', False))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title, completed) VALUES (%s, %s)", (title, completed))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task added'}), 201

# ✅ PUT: Toggle completion
@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    data = request.json
    completed = int(data['completed'])
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET completed=%s WHERE id=%s", (completed, id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task updated'})

# ✅ DELETE a task
@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task deleted'})

# ✅ Run server
if __name__ == '__main__':
    print("🚀 Flask server starting...")
    app.run(port=5500, debug=True)
