import cv2
import os
import time

name = input("Enter student name: ")

folder = f"faces/{name}"
os.makedirs(folder, exist_ok=True)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

count = 0
max_images = 100

last_capture = time.time()

while True:

    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100, 100)
    )

    for (x, y, w, h) in faces:

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"{count}/{max_images}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2
        )

        # Save one image every 0.3 seconds
        if time.time() - last_capture > 0.3 and count < max_images:

            face = frame[y:y+h, x:x+w]

            face = cv2.resize(face, (200, 200))

            cv2.imwrite(
                f"{folder}/{count}.jpg",
                face
            )

            count += 1
            last_capture = time.time()

    cv2.imshow("Register Face", frame)

    if count >= max_images:
        print("Registration Complete!")
        break

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()