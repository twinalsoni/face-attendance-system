from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

# DATABASE CREATE
def init_db():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

init_db()

# HOME ROUTE
@app.route('/')
def home():

    return "Face Attendance Backend Running"

# MARK ATTENDANCE
@app.route('/mark-attendance', methods=['POST'])
def mark_attendance():

    data = request.get_json()

    name = data.get('name')

    now = datetime.now()

    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO attendance(name, date, time)
        VALUES (?, ?, ?)
        """,
        (name, current_date, current_time)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Attendance Marked Successfully"
    })

# GET ATTENDANCE
@app.route('/attendance', methods=['GET'])
def get_attendance():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM attendance")

    rows = cursor.fetchall()

    conn.close()

    attendance_data = []

    for row in rows:

        attendance_data.append({
            "id": row[0],
            "name": row[1],
            "date": row[2],
            "time": row[3]
        })

    return jsonify(attendance_data)

if __name__ == '__main__':

    app.run(debug=True)