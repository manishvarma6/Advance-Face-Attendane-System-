

import cv2
import numpy as np
import os
import datetime

from backend.services.attendance_service import mark_attendance
from backend.services.summary_service import show_daily_summary
from backend.services.export_service import export_today_attendance

            # 🚫 2. Blur check
        # if is_blurry(face):
        #     user_id = "Blur"
        #     color = (255, 0, 0)
        #     continue


CASCADE_PATH = "backend/utils/haarcascade_frontalface_default.xml"
MODEL_PATH = "backend/database/lbph_model.xml"



def draw_rounded_rect(img, top_left, bottom_right, radius, color, thickness=-1):

    x1, y1 = top_left
    x2, y2 = bottom_right

    if thickness < 0:
        cv2.rectangle(img, (x1+radius, y1), (x2-radius, y2), color, -1)
        cv2.rectangle(img, (x1, y1+radius), (x2, y2-radius), color, -1)

        cv2.circle(img, (x1+radius, y1+radius), radius, color, -1)
        cv2.circle(img, (x2-radius, y1+radius), radius, color, -1)
        cv2.circle(img, (x1+radius, y2-radius), radius, color, -1)
        cv2.circle(img, (x2-radius, y2-radius), radius, color, -1)

    else:
        cv2.rectangle(img, (x1+radius, y1), (x2-radius, y2), color, thickness)
        cv2.rectangle(img, (x1, y1+radius), (x2, y2-radius), color, thickness)

        cv2.circle(img, (x1+radius, y1+radius), radius, color, thickness)
        cv2.circle(img, (x2-radius, y1+radius), radius, color, thickness)
        cv2.circle(img, (x1+radius, y2-radius), radius, color, thickness)
        cv2.circle(img, (x2-radius, y2-radius), radius, color, thickness)


def draw_modern_ui(frame):

    global last_face_img, last_user, last_conf

    canvas_h = 650
    canvas_w = 1100
    panel_w = 380

    # ===== CREATE SINGLE CANVAS =====
    canvas = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)
    canvas[:] = (18, 28, 38)

    # ===== CAMERA AREA =====
    cam = cv2.resize(frame, (canvas_w - panel_w - 40, canvas_h - 40))
    canvas[20:canvas_h-20, 20:canvas_w-panel_w-20] = cam

    # ===== RIGHT PANEL =====
    cv2.rectangle(
        canvas,
        (canvas_w-panel_w, 0),
        (canvas_w, canvas_h),
        (10, 20, 30),
        -1
    )

    x = canvas_w - panel_w + 30

    # ===== FACE PREVIEW =====
    if last_face_img is not None:
        face = cv2.resize(last_face_img, (260, 260))
        canvas[40:300, x:x+260] = face

    # ===== TEXT INFO =====
    cv2.putText(canvas, "Name", (x, 340),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (160,160,160), 1)

    cv2.putText(canvas, str(last_user), (x, 375),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 2)

    cv2.putText(canvas, "Confidence", (x, 420),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (160,160,160), 1)

    cv2.putText(canvas, f"{int(last_conf)}%", (x, 455),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,120), 2)

    now = datetime.datetime.now()

    cv2.putText(canvas, "Time", (x, 510),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (160,160,160), 1)

    cv2.putText(canvas, now.strftime("%H:%M:%S"),
                (x, 540), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 2)

    cv2.putText(canvas, "Date", (x, 580),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (160,160,160), 1)

    cv2.putText(canvas, now.strftime("%d-%m-%Y"),
                (x, 610), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200,200,200), 1)

    return canvas




def recognize_lbph():
    global last_face_img, last_user, last_conf

    def is_blurry(face):
        return cv2.Laplacian(face, cv2.CV_64F).var() < 50   

    print("📷 Starting LBPH Recognition...")
    MIN_FACE_WIDTH = 130     # 👈 door face reject
    CONF_THRESHOLD = 70      # 👈 strict matching


    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(MODEL_PATH)

    label_map = np.load(
        "backend/database/label_map.npy",
        allow_pickle=True
    ).item()

    cap = cv2.VideoCapture(0)


    # 🔥 UI STATE
    last_face_img = None
    last_user = ""
    last_conf = 0
    attendance_done = False

    cv2.namedWindow("LBPH Recognition", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("LBPH Recognition", 1200, 700)


    # cv2.namedWindow("LBPH Recognition", cv2.WINDOW_NORMAL)
    # cv2.setWindowProperty(
    #     "LBPH Recognition",
    #     cv2.WND_PROP_FULLSCREEN,
    #     cv2.WINDOW_FULLSCREEN
    # )

    # 🔥 WAIT + FRAME SYSTEM
    frame_counter = {}
    REQUIRED_FRAMES = 10

    start_time = {}
    WAIT_SECONDS = 10

    last_marked_time = {}
    COOLDOWN = 30


    present_count = 0
    unknown_count = 0

    marked_users = set()

    attendance_list = []

    unknown_saved = False   # 🚨 Prevent multiple unknown saves

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        # ===== SUCCESS SCREEN =====
        if attendance_done:

            ui_frame = draw_modern_ui(frame)

            h, w, _ = ui_frame.shape

            # Green success bar
            cv2.rectangle(ui_frame, (0, h-80), (w, h), (20, 80, 40), -1)

            cv2.putText(
                ui_frame,
                "✓ Attendance Marked Successfully",
                (40, h-30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,150),
                2
            )

            cv2.imshow("LBPH Recognition", ui_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            continue


        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        # for (x, y, w, h) in faces:

        #     face = gray[y:y+h, x:x+w]

        #     face = cv2.resize(face, (200, 200))

        #     label, confidence = recognizer.predict(face)

        #     # ✅ Known Face
        #     if confidence < 95:

        #         user_id = label_map[label]

        #         if user_id not in marked_users:

        #             mark_attendance(
        #                 user_id,
        #                 confidence,
        #                 frame
        #             )

        #             marked_users.add(user_id)

        #             present_count += 1

        #             # Add to attendance list
        #             current_time = datetime.datetime.now().strftime("%H:%M:%S")

        #             record = f"{user_id}  {current_time}"

        #             attendance_list.append(record)

        #         color = (0, 255, 0)  # Green

        #     # 🚨 Unknown Face
        #     else:

        #         user_id = "Unknown"

        #         if "Unknown" not in marked_users:

        #             unknown_count += 1
        #             marked_users.add("Unknown")

        #         # Save unknown only once
        #         if not unknown_saved:

        #             unknown_dir = "face_data/unknown_faces"

        #             os.makedirs(unknown_dir, exist_ok=True)

        #             time_stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        #             file_path = os.path.join(
        #                 unknown_dir,
        #                 f"unknown_{time_stamp}.jpg"
        #             )

        #             cv2.imwrite(file_path, frame)

        #             print(f"🚨 Unknown Face Saved: {file_path}")

        #             unknown_saved = True

        #         color = (0, 0, 255)  # Red

        #     # Draw rectangle
        #     cv2.rectangle(
        #         frame,
        #         (x, y),
        #         (x+w, y+h),
        #         color,
        #         2
        #     )

        #     # Show name
        #     cv2.putText(
        #         frame,
        #         str(user_id),
        #         (x, y-10),
        #         cv2.FONT_HERSHEY_SIMPLEX,
        #         0.8,
        #         color,
        #         2
        #     )



        # 🔁 MEMORY VARIABLES (loop ke bahar hone chahiye ideally)
        if 'frame_counter' not in locals():
            frame_counter = {}
            start_time = {}
            last_marked_time = {}

        for (x, y, w, h) in faces:

            # Default values
            user_id = "Detecting..."
            color = (0, 255, 255)  # Yellow

            # 🚫 1. Distance check
            if w < MIN_FACE_WIDTH:
                user_id = "Too Far"
                color = (0, 0, 255)

            else:
                # 🎯 Face process
                face = gray[y:y+h, x:x+w]
                face = cv2.resize(face, (200, 200))

                label, confidence = recognizer.predict(face)

                # 🚫 2. Unknown
                if confidence >= CONF_THRESHOLD:
                    user_id = "Unknown"
                    color = (0, 0, 255)

                else:
                    user_id = label_map[label]

                    import time
                    now = time.time()

                    # 🔥 Start timer
                    if user_id not in start_time:
                        start_time[user_id] = now
                        frame_counter[user_id] = 0

                    elapsed = now - start_time[user_id]

                    # ⏳ WAIT PHASE
                    if elapsed < WAIT_SECONDS:
                        remaining = int(WAIT_SECONDS - elapsed)

                        user_id = f"Wait {remaining}s"
                        color = (0, 255, 255)

                    else:
                        # 🔁 FRAME COUNT
                        frame_counter[user_id] += 1

                        if frame_counter[user_id] < REQUIRED_FRAMES:
                            user_id = f"Verifying {frame_counter[user_id]}/{REQUIRED_FRAMES}"
                            color = (0, 255, 255)

                        else:
                            # 🔒 COOLDOWN
                            if user_id in last_marked_time:
                                if now - last_marked_time[user_id] < COOLDOWN:
                                    # user_id = "Cooldown..."
                                    user_id = user_id
                                    color = (255, 0, 0)
                                else:
                                    last_marked_time[user_id] = now

                            else:
                                last_marked_time[user_id] = now

                            # ✅ FINAL ATTENDANCE
                            # if user_id not in marked_users:
                            #     mark_attendance(user_id, confidence, frame)

                            #     marked_users.add(user_id)
                            #     present_count += 1

                            #     current_time = datetime.datetime.now().strftime("%H:%M:%S")
                            #     record = f"{user_id}  {current_time}"
                            #     attendance_list.append(record)

                            #     # ✅ Success Banner
                            #     cv2.rectangle(frame, (0, frame.shape[0]-80), (frame.shape[1], frame.shape[0]), (20, 60, 30), -1)

                            #     cv2.putText(
                            #         frame,
                            #         "✓ Attendance Marked Successfully",
                            #         (20, frame.shape[0]-30),
                            #         cv2.FONT_HERSHEY_SIMPLEX,
                            #         0.9,
                            #         (0, 255, 100),
                            #         2
                            #     )

                            if user_id not in marked_users and not attendance_done:

                                mark_attendance(user_id, confidence, frame)

                                marked_users.add(user_id)
                                present_count += 1

                                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                                record = f"{user_id}  {current_time}"
                                attendance_list.append(record)

                                # 🔥 SAVE FACE TO RIGHT PANEL
                                last_face_img = frame[y:y+h, x:x+w].copy()
                                last_user = user_id
                                last_conf = confidence

                                attendance_done = True   # 🚨 STOP further scanning





                            user_id = f"{user_id} ✓"
                            color = (0, 255, 0)

            # 🎯 DRAW BOX (ONLY HERE — IMPORTANT)
            # 🎯 Draw face box (modern)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

            # 🔳 Top label background
            cv2.rectangle(frame, (x, y-30), (x+w, y), color, -1)

            # 🏷 Name text
            cv2.putText(
                frame,
                str(user_id),
                (x+5, y-8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            # 🧠 Send face to UI panel
            face_color = frame[y:y+h, x:x+w]














        # 📋 Show Recent Attendance (Last 5)

        y_offset = 100

        for record in attendance_list[-5:]:

            cv2.putText(
                frame,
                record,
                (10, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2
            )

            y_offset += 25

        # 🔢 Show Counters

        cv2.putText(
            frame,
            f"Present Today: {present_count}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Unknown Today: {unknown_count}",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )


        frame = draw_modern_ui(frame)

        cv2.imshow("LBPH Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

    cv2.destroyAllWindows()

    # 📊 Show summary
    show_daily_summary()

    # 📊 Export Excel
    export_today_attendance()
























































# import cv2
# import numpy as np

# from backend.services.attendance_service import mark_attendance
# from backend.services.summary_service import show_daily_summary

# CASCADE_PATH = "backend/utils/haarcascade_frontalface_default.xml"
# MODEL_PATH = "backend/database/lbph_model.xml"


# def recognize_lbph():

#     print("📷 Starting LBPH Recognition...")

#     face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

#     recognizer = cv2.face.LBPHFaceRecognizer_create()
#     recognizer.read(MODEL_PATH)

#     label_map = np.load(
#         "backend/database/label_map.npy",
#         allow_pickle=True
#     ).item()

#     cap = cv2.VideoCapture(0)
#     present_count = 0
#     unknown_count = 0
#     marked_users = set()
#     attendance_list = []

#     while True:

#         ret, frame = cap.read()

#         if not ret:
#             break

#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         faces = face_cascade.detectMultiScale(
#             gray,
#             scaleFactor=1.3,
#             minNeighbors=5
#         )

#         for (x, y, w, h) in faces:

#             face = gray[y:y+h, x:x+w]

#             face = cv2.resize(face, (200, 200))

#             label, confidence = recognizer.predict(face)

#             if confidence < 95:

#                 user_id = label_map[label]

#                 if user_id not in marked_users:

#                     mark_attendance(
#                         user_id,
#                         confidence,
#                         frame
#                     )

#                     marked_users.add(user_id)

#                     present_count += 1

#                 # Add to attendance list
#                 import datetime

#                 current_time = datetime.datetime.now().strftime("%H:%M:%S")

#                 record = f"{user_id}  {current_time}"

#                 if record not in attendance_list:
#                     attendance_list.append(record)
                    

#             else:

#                 user_id = "Unknown"
#                 # Count unknown only once
#                 if "Unknown" not in marked_users:

#                     unknown_count += 1
#                     marked_users.add("Unknown")

#                 # 🚨 Save unknown face
#                 import os
#                 import datetime

#                 unknown_dir = "face_data/unknown_faces"

#                 os.makedirs(unknown_dir, exist_ok=True)

#                 time_stamp = datetime.datetime.now().strftime("%H-%M-%S")

#                 file_path = os.path.join(
#                     unknown_dir,
#                     f"unknown_{time_stamp}.jpg"
#                 )

#                 cv2.imwrite(file_path, frame)

#                 print(f"🚨 Unknown Face Saved: {file_path}")
                

#             # Draw rectangle
#             cv2.rectangle(
#                 frame,
#                 (x, y),
#                 (x+w, y+h),
#                 (0, 255, 0),
#                 2
#             )

#             # Show name
#             cv2.putText(
#                 frame,
#                 str(user_id),
#                 (x, y-10),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.8,
#                 (0, 255, 0),
#                 2
#             )

#         y_offset = 30

#         for record in attendance_list[-5:]:

#             cv2.putText(
#                 frame,
#                 record,
#                 (10, y_offset),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.6,
#                 (0, 255, 255),
#                 2
#             )

#             y_offset += 25
            

#         cv2.putText(
#             frame,
#             f"Present Today: {present_count}",
#             (10, 30),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             0.7,
#             (0, 255, 0),
#             2
#         )

#         cv2.putText(
#             frame,
#             f"Unknown Today: {unknown_count}",
#             (10, 60),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             0.7,
#             (0, 0, 255),
#             2
#         )

#         cv2.imshow("LBPH Recognition", frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()
#     # 📊 Show summary
#     show_daily_summary()