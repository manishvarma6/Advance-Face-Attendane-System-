import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from backend.controllers.register_controller import register_user
from backend.services.lbph_train_service import train_lbph
from backend.services.excel_export_service import export_attendance_to_excel
from backend.services.summary_service import show_daily_summary
from frontend.gui.attendance_view_gui import open_attendance_view
from backend.services.admin_service import change_password
from frontend.gui.register_user_gui import open_register_window
from backend.services.lbph_train_service import open_train_model

from tkinter import messagebox

from frontend.gui.register_user_gui import open_register_window



def open_admin_panel():
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

        
# def open_admin_panel():

#     win = tk.Toplevel()
#     win.title("Admin Panel")
#     win.geometry("450x500")
#     win.configure(bg="#34495e")


#     # ✅ LOGOUT FUNCTION YAHAN SHIFT KARO
#     def logout():

#         from frontend.gui.admin_login import open_login_window

#         confirm = messagebox.askyesno("Logout", "Are you sure?")

#         if confirm:
#             win.destroy()
#             open_login_window()
            
#     # ---------- TITLE ----------
#     tk.Label(
#         win,
#         text="Admin Panel",
#         font=("Arial", 16, "bold"),
#         bg="#34495e",
#         fg="white"
#     ).pack(pady=15)

#     # ---------- USER INPUT ----------
#     tk.Label(win, text="User ID", bg="#34495e", fg="white").pack()
#     entry_id = tk.Entry(win)
#     entry_id.pack(pady=5)

#     tk.Label(win, text="Name", bg="#34495e", fg="white").pack()
#     entry_name = tk.Entry(win)
#     entry_name.pack(pady=5)

#     tk.Label(win, text="Department", bg="#34495e", fg="white").pack()
#     dept = ttk.Combobox(win, values=["IT", "HR", "Sales", "Admin"], state="readonly")
#     dept.pack(pady=5)
#     dept.set("IT")

#     # ---------- FUNCTIONS ----------
#     def register():
#         try:
#             register_user(entry_id.get(), entry_name.get(), dept.get())
#             messagebox.showinfo("Success", "User Registered")
#         except Exception as e:
#             messagebox.showerror("Error", str(e))

#     def train():
#         train_lbph()
#         messagebox.showinfo("Success", "Model Trained")

#     def view_excel():
#         export_attendance_to_excel()
#         messagebox.showinfo("Done", "Excel Opened")

#     def show_summary():
#         show_daily_summary()

#     # ---------- BUTTONS ----------
#     tk.Button(win, text="Register User", command=register, bg="#27ae60", fg="white").pack(pady=10)

#     tk.Button(win, text="Train Model", command=train, bg="#f39c12", fg="white").pack(pady=10)

#     tk.Button(win, text="View Attendance Excel", command=view_excel, bg="#2980b9", fg="white").pack(pady=10)

#     tk.Button(win, text="Show Summary", command=show_summary, bg="#8e44ad", fg="white").pack(pady=10)

#     tk.Button(
#         win,
#         text="📊 View Attendance Table",
#         command=open_attendance_view,
#         bg="#16a085",
#         fg="white"
#     ).pack(pady=10)


#     tk.Button(
#         win,
#         text="🔑 Change Password",
#         command=open_change_password,
#         bg="#9b59b6",
#         fg="white",
#         width=25
#     ).pack(pady=10)

#     tk.Button(
#         win,
#         text="🚪 Logout",
#         command=logout,
#         bg="red",
#         fg="white",
#         width=25
#     ).pack(pady=10)

#     # ---------- LIVE COUNT ----------
#     tk.Label(win, text="Live Summary", bg="#34495e", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

#     summary_label = tk.Label(win, text="", bg="#34495e", fg="yellow")
#     summary_label.pack()

#     def update_summary():
#         from backend.services.summary_service import get_today_summary

#         present, unknown = get_today_summary()
#         summary_label.config(text=f"Present: {present} | Unknown: {unknown}")
#         win.after(3000, update_summary)

#     update_summary()



# def open_change_password():

#     cp_window = tk.Toplevel()
#     cp_window.title("Change Password")
#     cp_window.geometry("300x250")

#     tk.Label(cp_window, text="Username").pack(pady=5)
#     entry_user = tk.Entry(cp_window)
#     entry_user.pack()

#     tk.Label(cp_window, text="Old Password").pack(pady=5)
#     entry_old = tk.Entry(cp_window, show="*")
#     entry_old.pack()

#     tk.Label(cp_window, text="New Password").pack(pady=5)
#     entry_new = tk.Entry(cp_window, show="*")
#     entry_new.pack()

#     def update_pass():
#         if change_password(
#             entry_user.get(),
#             entry_old.get(),
#             entry_new.get()
#         ):
#             messagebox.showinfo("Success", "Password Changed")
#             cp_window.destroy()
#         else:
#             messagebox.showerror("Error", "Wrong Old Password")

#     tk.Button(
#         cp_window,
#         text="Update Password",
#         command=update_pass,
#         bg="blue",
#         fg="white"
#     ).pack(pady=15)


    