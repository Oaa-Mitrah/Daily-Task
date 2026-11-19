from flask import Flask, render_template, request, jsonify
from database import get_connection, create_table 
from datetime import datetime 
from zoneinfo import ZoneInfo  

app = Flask(__name__)

# India ka aaj ka date 
def get_today():
    return datetime.now(ZoneInfo("Asia/Kolkata")).date()

# Website ka home page 
@app.route("/")
def home():
    return render_template("index.html")

# 1. Aaj ke tasks data base se lena 
@app.route("/api/tasks", methods=["GET"])
def get_all_tasks():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT id, task_name, task_date, is_completed
            FROM tasks WHERE task_date = %s ORDER BY id DESC """, (get_today(),))
            tasks = cursor.fetchall()
            return jsonify(tasks)
    finally:
        connection.close()

# 2. NAYA TASK ADD KARNA 
@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json(silent=True) or {}
    task_name = data.get("task_name")
    if not isinstance(task_name, str) or not task_name.strip():
        return jsonify({"error": "Task name is required"}), 400
    task_name = task_name.strip()
    if len(task_name) > 255:
        return jsonify({"error": "Task is too long"}), 400
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
            INSERT INTO tasks (task_name, task_date, is_completed)
            VALUES (%s, %s, %s) """, (task_name, get_today(), False))
            task_id = cursor.lastrowoid
        connection.commit()
        return jsonify({"message": "Task added successfully",
        "id": task_id,
        "task_name": task_name,
        "is_completed": False }), 201
    finally:
        connection.close()

# 3. TASK COMPLETE / INCOMPLETE 
@app.route("/api/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    data = request.get_json(silent=True) or {}
    completed = data.get("is_completed")

    if not isinstance(completed, bool):
        return jsonify({"error": "is_completed must be true or false"}), 400
    
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Check karta hai ki task database me hai yaa nahi 
            cursor.execute("""
            SELECT id FROM tasks WHERE id = %s AND task_date = %s """, (task_id, get_today()))
            task = cursor.fetchall()
            if task is None:
                return jsonify({"error": "Task not found"}), 404
            
            cursor.execute("""
            UPDATE tasks SET is_completed = %s 
            WHERE id = %s """, (completed, task_id))
        connection.commit()
        return jsonify({"message": "Task updated successfully",
        "is_completed": completed})
    finally:
        connection.close()

if __name__ == "__main__":
    create_table()
    app.run(debug=True)
    # /add-task \-H "Content-Type: application/json" \-d '{"task": "Read 10 Paages of a book !"}'
