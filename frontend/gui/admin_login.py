import tkinter as tk
from tkinter import messagebox

from backend.services.admin_service import validate_admin
from frontend.gui.admin_panel import open_admin_panel


def login():

    username = entry_user.get()
    password = entry_pass.get()

    if validate_admin(username, password):
        messagebox.showinfo("Success", "Login Successful")
        root.destroy()
        open_admin_panel()

    else:
        messagebox.showerror("Error", "Invalid Credentials")


def open_login_window():

    global root, entry_user, entry_pass

    root = tk.Tk()
    root.title("Admin Login")
    root.geometry("300x250")

    tk.Label(root, text="Admin Login", font=("Arial", 16)).pack(pady=20)

    tk.Label(root, text="Username").pack()
    entry_user = tk.Entry(root)
    entry_user.pack()

    tk.Label(root, text="Password").pack()
    entry_pass = tk.Entry(root, show="*")
    entry_pass.pack()

    tk.Button(
        root,
        text="Login",
        command=login,
        bg="green",
        fg="white"
    ).pack(pady=20)

    root.mainloop()