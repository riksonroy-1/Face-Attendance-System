import cv2
import os
import numpy as np

faces_dir = "faces"

face_samples = []
ids = []

names = {}
current_id = 0

for person in os.listdir(faces_dir):

    person_path = os.path.join(faces_dir, person)

    if not os.path.isdir(person_path):
        continue

    names[current_id] = person

    for image_name in os.listdir(person_path):

        image_path = os.path.join(
            person_path,
            image_name
        )

        image = cv2.imread(
            image_path,
            cv2.IMREAD_GRAYSCALE
        )

        face_samples.append(image)
        ids.append(current_id)

    current_id += 1

recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.train(
    face_samples,
    np.array(ids)
)

recognizer.save("trainer.yml")

with open("names.txt", "w") as f:
    for id_num, name in names.items():
        f.write(f"{id_num}:{name}\n")

print("Training complete!")