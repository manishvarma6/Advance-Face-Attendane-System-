import cv2
import os
import pickle
import numpy as np

RAW_IMAGE_DIR = "face_data/raw_images"
ENCODINGS_PATH = "backend/database/encodings.pkl"

CASCADE_PATH = "backend/utils/haarcascade_frontalface_default.xml"

def encode_faces():

    print("🔄 Starting Face Encoding...")

    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

    known_encodings = []
    known_user_ids = []

    for user_id in os.listdir(RAW_IMAGE_DIR):

        user_folder = os.path.join(RAW_IMAGE_DIR, user_id)

        if not os.path.isdir(user_folder):
            continue

        for image_name in os.listdir(user_folder):

            image_path = os.path.join(user_folder, image_name)

            img = cv2.imread(image_path)

            if img is None:
                continue

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=5
            )

            for (x, y, w, h) in faces:

                face = gray[y:y+h, x:x+w]

                face = cv2.resize(face, (100, 100))

                face_encoding = face.flatten()

                known_encodings.append(face_encoding)
                known_user_ids.append(user_id)

    print("✅ Total Encodings Created:", len(known_encodings))

    data = {
        "encodings": known_encodings,
        "user_ids": known_user_ids
    }

    with open(ENCODINGS_PATH, "wb") as f:
        pickle.dump(data, f)

    print("✅ Face Encodings Saved Successfully")