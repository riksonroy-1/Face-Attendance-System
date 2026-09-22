import cv2
import csv
import os
from datetime import datetime

# =========================
# Load Student Database
# =========================

students = {}

with open("students.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        students[row["Name"]] = {
            "ID": row["ID"],
            "Class": row["Class"]
        }

# =========================
# Create Attendance File
# =========================

if not os.path.exists("attendance.csv"):
    with open("attendance.csv", "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Date",
            "Time",
            "ID",
            "Name",
            "Class",
            "Status"
        ])

# =========================
# Load Face Recognizer
# =========================

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

# =========================
# Load Names
# =========================

names = {}

with open("names.txt", "r") as f:
    for line in f:
        id_num, name = line.strip().split(":")
        names[int(id_num)] = name

# =========================
# Face Detector
# =========================

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# =========================
# Track Attendance
# =========================

attendance_marked = set()

# =========================
# Recognition Stabilization
# =========================

recognition_history = {}

# =========================
# Start Camera
# =========================

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100, 100)
    )

    for (x, y, w, h) in faces:

        face = gray[y:y+h, x:x+w]

        try:
            id_num, confidence = recognizer.predict(face)
        except:
            continue

        name = "Unknown"

        if confidence < 60:

            detected_name = names.get(
                id_num,
                "Unknown"
            )

            recognition_history.setdefault(
                detected_name,
                0
            )

            recognition_history[
                detected_name
            ] += 1

            # Confirm after 3 detections
            if recognition_history[
                detected_name
            ] >= 3:

                name = detected_name

                # Mark attendance once
                if name not in attendance_marked:

                    now = datetime.now()

                    student = students.get(name)

                    with open(
                        "attendance.csv",
                        "a",
                        newline=""
                    ) as file:

                        writer = csv.writer(file)

                        if student:

                            writer.writerow([
                                now.date(),
                                now.strftime("%H:%M:%S"),
                                student["ID"],
                                name,
                                student["Class"],
                                "Present"
                            ])

                        else:

                            writer.writerow([
                                now.date(),
                                now.strftime("%H:%M:%S"),
                                "N/A",
                                name,
                                "N/A",
                                "Present"
                            ])

                    attendance_marked.add(name)

                    print(
                        f"{name} marked present"
                    )

            else:

                name = "Checking..."

        else:

            name = "Unknown"

        # Draw Box

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        # Show Name

        cv2.putText(
            frame,
            name,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    cv2.imshow(
        "AI Attendance System",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()