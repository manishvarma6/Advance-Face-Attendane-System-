import cv2
import pickle
import numpy as np

ENCODINGS_PATH = "backend/database/encodings.pkl"
CASCADE_PATH = "backend/utils/haarcascade_frontalface_default.xml"

def recognize_faces():

    print("📷 Starting Face Recognition...")

    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

    with open(ENCODINGS_PATH, "rb") as f:
        data = pickle.load(f)

    known_encodings = data["encodings"]
    known_user_ids = data["user_ids"]

    THRESHOLD = 12000

    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        for (x, y, w, h) in faces:

            face = gray[y:y+h, x:x+w]

            face = cv2.resize(face, (100, 100))

            face_encoding = face.flatten()

            distances = []

            for enc in known_encodings:
                dist = np.linalg.norm(enc - face_encoding)
                distances.append(dist)

            label = "Unknown"

            if len(distances) > 0:

                min_dist = min(distances)
                print("Distance:", min_dist)

                if min_dist < THRESHOLD:

                    index = distances.index(min_dist)
                    label = known_user_ids[index]

            # Draw box
            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                label,
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()