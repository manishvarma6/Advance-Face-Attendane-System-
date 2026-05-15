import cv2
import os
import numpy as np
import threading
import tkinter as tk
from tkinter import ttk, messagebox

RAW_IMAGE_DIR = "face_data/raw_images"
CASCADE_PATH = "backend/utils/haarcascade_frontalface_default.xml"
MODEL_PATH = "backend/database/lbph_model.xml"


# ====================================
# TRAINING LOGIC (UNCHANGED BACKEND)
# ====================================
def train_lbph(progress_callback=None):

    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

    faces = []
    labels = []
    label_map = {}
    current_label = 0

    # count images
    total_images = 0
    for user_id in os.listdir(RAW_IMAGE_DIR):
        user_folder = os.path.join(RAW_IMAGE_DIR, user_id)
        if os.path.isdir(user_folder):
            total_images += len(os.listdir(user_folder))

    processed_images = 0

    for user_id in sorted(os.listdir(RAW_IMAGE_DIR)):

        user_folder = os.path.join(RAW_IMAGE_DIR, user_id)
        if not os.path.isdir(user_folder):
            continue

        images = os.listdir(user_folder)
        if len(images) == 0:
            continue

        label_map[current_label] = user_id

        for img_name in images:

            img_path = os.path.join(user_folder, img_name)
            img = cv2.imread(img_path)

            if img is None:
                continue

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            detected_faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=5
            )

            for (x, y, w, h) in detected_faces:
                face = gray[y:y+h, x:x+w]
                face = cv2.resize(face, (200, 200))
                faces.append(face)
                labels.append(current_label)

            # ---- progress update ----
            processed_images += 1
            if progress_callback and total_images > 0:
                percent = int((processed_images / total_images) * 100)
                progress_callback(percent)

        current_label += 1

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(labels))
    recognizer.save(MODEL_PATH)

    np.save("backend/database/label_map.npy", label_map)


# ====================================
# ⭐ SINGLE FUNCTION TO CALL FROM DASHBOARD
# ====================================



import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading


def open_train_model(parent_window=None):

    # ================= WINDOW =================
    train_window = tk.Toplevel(parent_window)
    train_window.title("Train Model")

    WIDTH = 700
    HEIGHT = 450

    train_window.geometry(f"{WIDTH}x{HEIGHT}")
    train_window.resizable(False, False)
    train_window.grab_set()
    train_window.configure(bg="black")

    # ================= BACKGROUND IMAGE =================
    bg_image = Image.open("frontend\\assets\\guimage\\trainbg .jpg")   # <-- YOUR IMAGE PATH
    bg_image = bg_image.resize((WIDTH, HEIGHT))

    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(train_window, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # ================= CONTENT FRAME =================
    content = tk.Frame(train_window, bg="#0d1b2a")
    content.place(relx=0.5, rely=0.70, anchor="center")

    # -------- Training Text --------
    tk.Label(
        content,
        text="Training in Progress...",
        font=("Segoe UI", 16, "bold"),
        fg="white",
        bg="#0d1b2a"
    ).pack(pady=(10, 10))

    # -------- Progress Bar --------
    progress = ttk.Progressbar(
        content,
        orient="horizontal",
        length=350,
        mode="determinate"
    )
    progress.pack(pady=5)

    # -------- Please Wait --------
    wait_label = tk.Label(
        content,
        text="Please wait...",
        font=("Segoe UI", 11),
        fg="white",
        bg="#0d1b2a"
    )
    wait_label.pack(pady=(5, 15))

    # ================= PROGRESS UPDATE =================
    def update_progress(value):
        progress["value"] = value
        train_window.update_idletasks()

    # ================= TRAIN THREAD =================
    def run_training():

        train_lbph(progress_callback=update_progress)

        train_window.destroy()

        messagebox.showinfo(
            "Success",
            "Training Successfully Completed ✅"
        )

    threading.Thread(target=run_training, daemon=True).start()



































# import cv2
# import os
# import numpy as np

# RAW_IMAGE_DIR = "face_data/raw_images"
# CASCADE_PATH = "backend/utils/haarcascade_frontalface_default.xml"
# MODEL_PATH = "backend/database/lbph_model.xml"

# def train_lbph():

#     print("🎯 Training LBPH Model...")

#     face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

#     faces = []
#     labels = []

#     label_map = {}
#     current_label = 0

#     users_found = 0
#     for user_id in sorted(os.listdir(RAW_IMAGE_DIR)):

#         user_folder = os.path.join(RAW_IMAGE_DIR, user_id)

#         if not os.path.isdir(user_folder):
#             continue

#         images = os.listdir(user_folder)

#         if len(images) == 0:
#             print(f"⚠️ Skipping Empty Folder: {user_id}")
#             continue

#         print(f"👤 Reading User: {user_id}")

#         label_map[current_label] = user_id
#         users_found += 1

#         face_count = 0   # NEW

#         for img_name in images:

#             img_path = os.path.join(user_folder, img_name)

#             img = cv2.imread(img_path)

#             if img is None:
#                 continue

#             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#             detected_faces = face_cascade.detectMultiScale(
#                 gray,
#                 scaleFactor=1.3,
#                 minNeighbors=5
#             )

#             for (x, y, w, h) in detected_faces:

#                 face = gray[y:y+h, x:x+w]
#                 face = cv2.resize(face, (200, 200))

#                 faces.append(face)
#                 labels.append(current_label)

#                 face_count += 1   # NEW

#         print(f"   Faces Used: {face_count}")  # NEW

#         current_label += 1

#     print("👥 Users Found:", users_found)

#     recognizer = cv2.face.LBPHFaceRecognizer_create()

#     recognizer.train(faces, np.array(labels))

#     recognizer.save(MODEL_PATH)

#     np.save(
#         "backend/database/label_map.npy",
#         label_map
#     )

#     print("✅ LBPH Model Trained Successfully")
#     print("Total Faces Used:", len(faces))