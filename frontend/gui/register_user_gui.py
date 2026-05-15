import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2

from backend.controllers.register_controller import register_user


# ==================================================
# REGISTER WINDOW WITH LIVE CAMERA
# ==================================================
def open_register_window():

    reg_window = tk.Toplevel()
    reg_window.title("Register New User")
    reg_window.geometry("1200x720")
    reg_window.resizable(False, False)
    reg_window.configure(bg="#06162d")

    camera = None
    current_frame = None
    captured_image = None

    # ==========================================
    # TITLE
    # ==========================================
    tk.Label(
        reg_window,
        text="REGISTER NEW USER",
        font=("Arial", 30, "bold"),
        fg="white",
        bg="#06162d"
    ).place(x=45, y=55)

    # ==========================================
    # STYLES
    # ==========================================
    label_style = {
        "font": ("Arial", 18, "bold"),
        "fg": "white",
        "bg": "#06162d"
    }

    entry_style = {
        "font": ("Arial", 18),
        "bg": "#08111f",
        "fg": "white",
        "insertbackground": "white",
        "bd": 0
    }

    # ==========================================
    # FORM
    # ==========================================
    tk.Label(reg_window, text="User ID", **label_style).place(x=50, y=170)
    entry_user_id = tk.Entry(reg_window, **entry_style)
    entry_user_id.place(x=230, y=165, width=380, height=55)

    tk.Label(reg_window, text="Name", **label_style).place(x=50, y=275)
    entry_name = tk.Entry(reg_window, **entry_style)
    entry_name.place(x=230, y=270, width=380, height=55)

    tk.Label(reg_window, text="Department", **label_style).place(x=50, y=380)

    dept_dropdown = ttk.Combobox(
        reg_window,
        values=["IT", "HR", "Sales", "Admin", "BCA"],
        state="readonly",
        font=("Arial", 18)
    )
    dept_dropdown.place(x=230, y=375, width=380, height=55)
    dept_dropdown.set("IT")

    tk.Label(reg_window, text="Roll Number", **label_style).place(x=50, y=485)
    entry_roll = tk.Entry(reg_window, **entry_style)
    entry_roll.place(x=230, y=480, width=380, height=55)

    # ==========================================
    # PHOTO PREVIEW BOX
    # ==========================================
    preview = tk.Label(reg_window, bg="white")
    preview.place(x=680, y=95, width=390, height=390)

    # ==========================================
    # CAMERA FUNCTIONS
    # ==========================================
    def start_camera():
        nonlocal camera
        camera = cv2.VideoCapture(0)
        update_camera()

    def update_camera():
        nonlocal current_frame

        if camera and camera.isOpened():
            ret, frame = camera.read()

            if ret:
                current_frame = frame.copy()

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (390, 390))

                img = Image.fromarray(frame)
                img_tk = ImageTk.PhotoImage(img)

                preview.imgtk = img_tk
                preview.configure(image=img_tk)

        reg_window.after(30, update_camera)

# ===== REPLACE ONLY capture_images() FUNCTION WITH THIS =====

    def capture_images():
        nonlocal captured_image, camera, current_frame

        if current_frame is not None:

            # freeze current frame
            captured_image = current_frame.copy()

            frame = cv2.cvtColor(captured_image, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (390, 390))

            img = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(img)

            # show captured image in preview box
            preview.imgtk = img_tk
            preview.configure(image=img_tk)

            # stop live camera after capture
            if camera:
                camera.release()
                camera = None

    # ==========================================
    # REGISTER
    # ==========================================
    def register():

        user_id = entry_user_id.get().strip()
        name = entry_name.get().strip()
        department = dept_dropdown.get().strip()

        if not user_id or not name or not department:
            messagebox.showerror("Error", "Enter all details")
            return

        try:
            register_user(user_id, name, department)

            if camera:
                camera.release()

            reg_window.destroy()

            messagebox.showinfo(
                "Success",
                "User saved & Images Captured"
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ==========================================
    # BUTTONS
    # ==========================================
    tk.Button(
        reg_window,
        text="📷 Capture Images",
        command=capture_images,
        bg="#22c55e",
        fg="white",
        font=("Arial", 20, "bold"),
        bd=0
    ).place(x=680, y=515, width=390, height=75)

    tk.Button(
        reg_window,
        text="💾 Save User",
        command=register,
        bg="#1e73ff",
        fg="white",
        font=("Arial", 20, "bold"),
        bd=0
    ).place(x=680, y=615, width=390, height=75)

    # ==========================================
    # START CAMERA AFTER 10 SEC
    # ==========================================
    reg_window.after(5000, start_camera)

























# import tkinter as tk
# from tkinter import messagebox
# from tkinter import ttk

# # Backend imports (tumhare existing files se)
# from backend.controllers.register_controller import register_user


# def open_register_window():

#     reg_window = tk.Toplevel()
#     reg_window.title("Register User")
#     reg_window.geometry("350x350")
#     reg_window.configure(bg="#34495e")

#     # ---------------- TITLE ----------------
#     label_title = tk.Label(
#         reg_window,
#         text="Register New User",
#         font=("Arial", 16, "bold"),
#         bg="#34495e",
#         fg="white"
#     )
#     label_title.pack(pady=20)

#     # ---------------- USER ID ----------------
#     label_user_id = tk.Label(
#         reg_window,
#         text="Enter User ID:",
#         font=("Arial", 12),
#         bg="#34495e",
#         fg="white"
#     )
#     label_user_id.pack()

#     entry_user_id = tk.Entry(
#         reg_window,
#         width=25,
#         font=("Arial", 12)
#     )
#     entry_user_id.pack(pady=5)

#     # ---------------- NAME ----------------
#     label_name = tk.Label(
#         reg_window,
#         text="Enter Name:",
#         font=("Arial", 12),
#         bg="#34495e",
#         fg="white"
#     )
#     label_name.pack()

#     entry_name = tk.Entry(
#         reg_window,
#         width=25,
#         font=("Arial", 12)
#     )
#     entry_name.pack(pady=5)

#     # ---------------- DEPARTMENT ----------------
#     label_dept = tk.Label(
#         reg_window,
#         text="Select Department:",
#         font=("Arial", 12),
#         bg="#34495e",
#         fg="white"
#     )
#     label_dept.pack()

#     dept_dropdown = ttk.Combobox(
#         reg_window,
#         values=["IT", "HR", "Sales", "Admin"],
#         state="readonly",
#         width=22,
#         font=("Arial", 12)
#     )
#     dept_dropdown.pack(pady=5)

#     dept_dropdown.set("IT")  # default value

#     # ---------------- REGISTER FUNCTION ----------------
#     def register():

#         user_id = entry_user_id.get().strip()
#         name = entry_name.get().strip()
#         department = dept_dropdown.get().strip()

#         if not user_id or not name or not department:
#             messagebox.showerror("Error", "Enter all details")
#             return

#         try:
#             register_user(user_id, name, department)
#             messagebox.showinfo(
#                 "Success",
#                 "User Registered & Images Captured"
#             )
#             reg_window.destroy()

#         except Exception as e:
#             messagebox.showerror("Error", str(e))

#     # ---------------- BUTTON ----------------
#     btn_register = tk.Button(
#         reg_window,
#         text="Register User",
#         command=register,
#         bg="#27ae60",
#         fg="white",
#         font=("Arial", 12, "bold"),
#         width=20
#     )
#     btn_register.pack(pady=20)