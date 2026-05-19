import cv2
import sqlite3
from datetime import datetime
import os

# Create folder
if not os.path.exists("student_images"):
    os.makedirs("student_images")

# Database connection
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    date TEXT,
    time TEXT
)
""")

conn.commit()

# Input student name
student_name = input("Enter Student Name: ")

# Load face cascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    'haarcascade_frontalface_default.xml'
)

# Open webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():

    print("Cannot open webcam")
    exit()

attendance_marked = False

while True:

    ret, frame = cap.read()

    if not ret:

        print("Failed to grab frame")
        break

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=4
    )

    for (x, y, w, h) in faces:

        # Draw rectangle
        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (255, 0, 0),
            2
        )

        # Save only once
        if not attendance_marked:

            # SAVE FULL IMAGE
            image_path = f"student_images/{student_name}.jpg"

            cv2.imwrite(
                image_path,
                frame
            )

            # Date and time
            now = datetime.now()

            current_date = now.strftime("%Y-%m-%d")
            current_time = now.strftime("%H:%M:%S")

            # Insert attendance
            cursor.execute(
                """
                INSERT INTO attendance(name, date, time)
                VALUES (?, ?, ?)
                """,
                (
                    student_name,
                    current_date,
                    current_time
                )
            )

            conn.commit()

            print("Attendance Marked Successfully")
            print("Image Saved Successfully")

            attendance_marked = True

    cv2.imshow(
        "Face Attendance System",
        frame
    )

    # ESC key
    if cv2.waitKey(1) == 27:
        break

cap.release()
conn.close()

cv2.destroyAllWindows()