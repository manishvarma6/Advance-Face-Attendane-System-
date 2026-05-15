import cv2
import os


def capture_face_images(user_id, num_images=30):

    save_path = f"face_data/raw_images/{user_id}"

    # Create folder
    os.makedirs(save_path, exist_ok=True)

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Camera not opening")
        return

    # Load face detector
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    count = 0

    print("📸 Starting Face Capture...")

    while True:

        ret, frame = cap.read()

        if not ret:
            print("❌ Failed to grab frame")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        for (x, y, w, h) in faces:

            face_img = frame[y:y+h, x:x+w]

            img_name = f"{save_path}/img_{count}.jpg"

            cv2.imwrite(img_name, face_img)

            count += 1

            # Draw rectangle
            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                (0, 255, 0),
                2
            )

        cv2.putText(
            frame,
            f"Images Captured: {count}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow("Face Capture", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if count >= num_images:
            break

    cap.release()
    cv2.destroyAllWindows()

    print(f"✅ {count} Images Captured for {user_id}")