import tkinter as tk
from tkinter import messagebox
import csv
import os

def add_student():

    student_id = entry_id.get().strip()
    student_name = entry_name.get().strip()
    student_class = entry_class.get().strip()

    if not student_id or not student_name or not student_class:
        messagebox.showerror(
            "Error",
            "Please fill all fields"
        )
        return

    # Add to students.csv
    with open(
        "students.csv",
        "a",
        newline="",
	encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            student_id,
            student_name,
            student_class
        ])

    # Create face folder
    os.makedirs(
        f"faces/{student_name}",
        exist_ok=True
    )

    messagebox.showinfo(
        "Success",
        f"{student_name} added successfully!"
    )

    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_class.delete(0, tk.END)

root = tk.Tk()

root.title("Add Student")
root.geometry("350x250")

tk.Label(
    root,
    text="Student ID"
).pack(pady=5)

entry_id = tk.Entry(root)
entry_id.pack()

tk.Label(
    root,
    text="Student Name"
).pack(pady=5)

entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(
    root,
    text="Class"
).pack(pady=5)

entry_class = tk.Entry(root)
entry_class.pack()

tk.Button(
    root,
    text="Add Student",
    command=add_student
).pack(pady=20)

root.mainloop()