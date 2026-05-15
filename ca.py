import cv2

print("Searching for cameras...")

for i in range(6):  # Try indexes 0–5
    print(f"Trying camera index {i}...")

    cap = cv2.VideoCapture(i)

    if cap.isOpened():
        print(f"✅ Camera FOUND at index {i}")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Frame not received")
                break

            cv2.imshow("Camera Test", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        break

    cap.release()

else:
    print("❌ No camera detected")