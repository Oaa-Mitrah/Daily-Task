import pymysql
import os
from dotenv import load_dotenv
load_dotenv()

def get_connection():
  connection = pymysql.connect(host=os.getenv("DB-HOST")
  post=int(os.getenv("DB_PORT")),
  user=os.getenv("DB_USER"),
  password=os.getenv("DB_PASSWORD"),
  database=os.getenv("DB_NAME"),
  charset="utf8mb4",
  cursorclass=pymysql.cursors.DictCursor,
  ssl={}
  )
  return coonnection

def create_table():
  connection = get_connection()
  try:
    with connection.cursor() as cursor:
      cursor.execute("""
      CREATE TABLE IF NOT EXISTS tasks (
      id INT AUTO_INCREMENT PRIMARY KEY,
      task_name VARCHAR(255) NOT NULL,
      task_date DATE NOT NULL,
      is_completed BOOLEAN DEFAULT FALSE,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
      """)
    connection.commit()
  finally:
    connection.close()

def save_task(task_name, task_date, is_completed):
  connection = get_connection()
  try:
    with connection.cursor() as cursor:
      cursor.execute("""
      INSERT INTO tasks (task_name, task_date, is_completed)
      VALUES (%s, %s, %s)""",
                    (task_name, task_date, is_completed))
    connection.commit()
  finally:
    coonnection.close()

# DATA FETCHING FROM SQL DATABASE 
def get_tasks():
  connection = get_connection()
  try:
    with connection.cursor() as cursor:
      cursor.execute("""
      SELECT * FROM tasks ORDER BY task_date DESC, id DESC
      """)
      tasks = cursor.fetchall()
      return tasks
  finally:
    connection.close()
    
