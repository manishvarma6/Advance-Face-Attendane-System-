import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime

import customtkinter as ctk
from datetime import datetime

from frontend.gui.admin_login import open_login_window
from backend.services.lbph_recognition_service import recognize_lbph
from PIL import Image




# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("Face Recognition Attendance System")
root.geometry("1080x603")
root.resizable(False, False)

# ---------------- BACKGROUND IMAGE ----------------
img = Image.open("frontend\\assets\\guimage\\main_bg.jpg")
img = img.resize((1080, 603))
bg = ImageTk.PhotoImage(img)

canvas = tk.Canvas(root, width=1080, height=603, highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg, anchor="nw")

#--------funcation -------------------
def open_student_attendance():
    recognize_lbph()



# ---------------- BUTTONS ----------------
btn1 = tk.Button(
    root,
    text="👤  STUDENT ATTENDANCE",
    font=("Arial", 18, "bold"),
    fg="white",
    bg="#1e73ff",
    activebackground="#125ee8",
    bd=0,
    cursor="hand2",
    command=open_student_attendance
    
)

btn2 = tk.Button(
    root,
    text="🛡  ADMIN PANEL",
    font=("Arial", 18, "bold"),
    fg="white",
    bg="#2bbf59",
    activebackground="#20a54a",
    bd=0,
    cursor="hand2",
    command=open_login_window
)

canvas.create_window(690, 286, window=btn1, width=480, height=78)
canvas.create_window(690, 440, window=btn2, width=480, height=78)

# ---------------- DATE + TIME ----------------
time_label = tk.Label(
    root,
    text="",
    font=("Arial", 14, "bold"),
    fg="white",
    bg="#021a35"
)

canvas.create_window(690, 540, window=time_label)

def update_time():
    now = datetime.now().strftime("Today: %d %B %Y   |   Time: %I:%M:%S %p")
    time_label.config(text=now)
    root.after(1000, update_time)

update_time()

# ---------------- RUN ----------------
root.mainloop()