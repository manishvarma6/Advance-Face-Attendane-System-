import tkinter as tk
from tkinter import ttk, messagebox
   
from frontend.gui.register_user_gui import open_register_window
from backend.services.lbph_train_service import open_train_model

# ==============================
# DUMMY FUNCTIONS (replace yours)
# ==============================
def register():
    open_register_window()

def train():
    open_train_model()


def view_excel():
    messagebox.showinfo("Excel", "Attendance Opened")

def show_summary():
    messagebox.showinfo("Summary", "Today's Summary Opened")

def open_attendance_view():
    messagebox.showinfo("Attendance", "Attendance Window Opened")

def open_change_password():
    messagebox.showinfo("Password", "Change Password Window")

def logout():
    ask = messagebox.askyesno("Logout", "Are you sure?")
    if ask:
        win.destroy()


# ==============================
# MAIN WINDOW
# ==============================
win = tk.Tk()
win.title("Admin Panel")
win.geometry("1200x720")
win.resizable(False, False)
win.configure(bg="#06162d")   # dark blue


# ==============================
# SIDEBAR
# ==============================
sidebar = tk.Frame(win, bg="#08111f")
sidebar.place(x=0, y=0, width=270, height=720)

topbar = tk.Frame(win, bg="#071a33")
topbar.place(x=270, y=0, width=930, height=70)


# ==============================
# TITLE
# ==============================
tk.Label(
    win,
    text="📊 DASHBOARD",
    font=("Arial", 28, "bold"),
    fg="white",
    bg="#071a33"
).place(x=310, y=16)


# ==============================
# SIDEBAR MENU
# ==============================
menu_style = {
    "font": ("Arial", 14, "bold"),
    "fg": "white",
    "bg": "#08111f",
    "activebackground": "#0d47a1",
    "activeforeground": "white",
    "bd": 0,
    "width": 22,
    "anchor": "w",
    "cursor": "hand2"
}

tk.Button(win, text="📊 Dashboard", **menu_style).place(x=10, y=90, height=48)
tk.Button(win, text="👤 Register User", command=register, **menu_style).place(x=10, y=145, height=48)
tk.Button(win, text="🧠 Train Model", command=train, **menu_style).place(x=10, y=200, height=48)
tk.Button(win, text="✅ Mark Attendance", command=open_attendance_view, **menu_style).place(x=10, y=255, height=48)
tk.Button(win, text="📄 View Attendance", command=view_excel, **menu_style).place(x=10, y=310, height=48)
tk.Button(win, text="📈 Summary", command=show_summary, **menu_style).place(x=10, y=365, height=48)
tk.Button(win, text="📤 Export Excel", command=view_excel, **menu_style).place(x=10, y=420, height=48)
tk.Button(win, text="🔑 Change Password", command=open_change_password, **menu_style).place(x=10, y=475, height=48)
tk.Button(win, text="🚪 Logout", command=logout, **menu_style).place(x=10, y=530, height=48)


# ==============================
# DASHBOARD CARDS
# ==============================
def card(x, y, title, number, icon, color):
    frame = tk.Frame(win, bg="white")
    frame.place(x=x, y=y, width=280, height=120)

    tk.Label(
        frame,
        text=title,
        font=("Arial", 14, "bold"),
        fg="#333",
        bg="white"
    ).place(x=20, y=15)

    tk.Label(
        frame,
        text=number,
        font=("Arial", 34, "bold"),
        fg="black",
        bg="white"
    ).place(x=20, y=52)

    tk.Label(
        frame,
        text=icon,
        font=("Arial", 34),
        fg=color,
        bg="white"
    ).place(x=215, y=52)


card(305, 100, "Total Users", "25", "👥", "#3b82f6")
card(610, 100, "Today's Attendance", "18", "✅", "#22c55e")
card(915, 100, "Unknown Faces", "3", "🚫", "#ef4444")





# ==============================
# CHART AREA
# ==============================
chart = tk.Frame(win, bg="white")
chart.place(x=305, y=400, width=890, height=280)

tk.Label(
    chart,
    text="📈 Today's Attendance Chart",
    font=("Arial", 16, "bold"),
    bg="white"
).place(x=20, y=15)

bars = [14, 10, 14, 19, 20, 15, 20, 16]
labels = ["9 AM", "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM", "4 PM"]

base_y = 240
x = 50

for i, h in enumerate(bars):
    tk.Frame(chart, bg="#4f8df7").place(
        x=x,
        y=base_y - h * 8,
        width=35,
        height=h * 8
    )

    tk.Label(
        chart,
        text=labels[i],
        bg="white",
        font=("Arial", 9)
    ).place(x=x - 5, y=245)

    x += 95


# ==============================
# RUN
# ==============================
win.mainloop()