import tkinter as tk
from tkinter import ttk
import sqlite3


DB_PATH = "backend/database/attendance.db"


def open_attendance_view():

    win = tk.Toplevel()
    win.title("Attendance Viewer")
    win.geometry("700x500")

    # ---------------- DATE FILTER ----------------
    tk.Label(win, text="Enter Date (YYYY-MM-DD):").pack(pady=5)

    entry_date = tk.Entry(win)
    entry_date.pack(pady=5)

    # ---------------- TABLE ----------------
    columns = ("User ID", "Date", "Time", "Status")

    tree = ttk.Treeview(win, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.pack(fill="both", expand=True, pady=10)

    # ---------------- SUMMARY ----------------
    summary_label = tk.Label(win, text="", font=("Arial", 12, "bold"))
    summary_label.pack(pady=5)

    # ---------------- LOAD DATA ----------------
    def load_data():

        for row in tree.get_children():
            tree.delete(row)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        selected_date = entry_date.get().strip()

        if selected_date:
            cursor.execute(
                "SELECT user_id, date, time, status FROM attendance WHERE date=?",
                (selected_date,)
            )
        else:
            cursor.execute(
                "SELECT user_id, date, time, status FROM attendance"
            )

        rows = cursor.fetchall()

        for row in rows:
            tree.insert("", "end", values=row)

        # ----------- COUNT -----------
        unique_users = set([r[0] for r in rows if r[0] != "Unknown"])
        total_present = len(unique_users)

        summary_label.config(text=f"Total Present: {total_present}")

        conn.close()

    # ---------------- BUTTON ----------------
    tk.Button(
        win,
        text="Load Data",
        command=load_data,
        bg="#3498db",
        fg="white"
    ).pack(pady=5)