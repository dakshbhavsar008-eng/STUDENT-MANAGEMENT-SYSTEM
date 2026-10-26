import json
import tkinter as tk
from tkinter import ttk, messagebox

# Student Management System
# Concepts used: Lists, Dictionaries, Functions, File Handling, Tkinter
# No MySQL or other database is required. Student records are stored in students.json.

DATA_FILE = "students.json"
students = []


def load_students():
    """Load student records from the JSON file."""
    global students
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            students = data if isinstance(data, list) else []
    except FileNotFoundError:
        students = []
    except (json.JSONDecodeError, OSError):
        students = []
        messagebox.showwarning(
            "File Notice",
            "Could not read students.json. Starting with an empty student list."
        )


def save_students():
    """Save the current student list to the JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(students, file, indent=4, ensure_ascii=False)
    except OSError as error:
        messagebox.showerror("File Error", f"Could not save student records:\n{error}")


def refresh_table(records=None):
    """Refresh the table using all students or a filtered list."""
    for item in student_table.get_children():
        student_table.delete(item)

    for student in students if records is None else records:
        student_table.insert(
            "",
            tk.END,
            values=(
                student.get("id", ""),
                student.get("name", ""),
                student.get("age", ""),
                student.get("course", ""),
                student.get("email", "")
            )
        )


def clear_fields():
    """Clear all input fields and remove the table selection."""
    student_id_entry.config(state="normal")
    student_id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

    selected = student_table.selection()
    if selected:
        student_table.selection_remove(*selected)

    student_id_entry.focus_set()


def get_form_data():
    """Validate the form and return student data as a dictionary."""
    student_id = student_id_entry.get().strip()
    name = name_entry.get().strip()
    age_text = age_entry.get().strip()
    course = course_entry.get().strip()
    email = email_entry.get().strip()

    if not all([student_id, name, age_text, course, email]):
        messagebox.showwarning("Missing Information", "Please fill in all fields.")
        return None

    try:
        age = int(age_text)
        if age <= 0 or age > 120:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Invalid Age", "Please enter a valid age between 1 and 120.")
        return None

    if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
        messagebox.showwarning("Invalid Email", "Please enter a valid email address.")
        return None

    return {
        "id": student_id,
        "name": name,
        "age": age,
        "course": course,
        "email": email
    }


def add_student():
    """Add a new student after checking for a duplicate ID."""
    student = get_form_data()
    if student is None:
        return

    if any(existing["id"].lower() == student["id"].lower() for existing in students):
        messagebox.showerror("Duplicate ID", "A student with this ID already exists.")
        return

    students.append(student)
    save_students()
    refresh_table()
    clear_fields()
    messagebox.showinfo("Success", "Student added successfully.")


def select_student(event=None):
    """Put the selected table row into the form for editing."""
    selection = student_table.selection()
    if not selection:
        return

    values = student_table.item(selection[0], "values")
    clear_fields()

    student_id_entry.insert(0, values[0])
    student_id_entry.config(state="readonly")
    name_entry.insert(0, values[1])
    age_entry.insert(0, values[2])
    course_entry.insert(0, values[3])
    email_entry.insert(0, values[4])


def update_student():
    """Update the selected student record."""
    selection = student_table.selection()
    if not selection:
        messagebox.showwarning("Select Student", "Select a student from the table first.")
        return

    original_id = student_table.item(selection[0], "values")[0]
    student = get_form_data()
    if student is None:
        return

    # The ID is kept unchanged while editing an existing record.
    student["id"] = original_id

    for index, existing in enumerate(students):
        if existing["id"] == original_id:
            students[index] = student
            break

    save_students()
    refresh_table()
    clear_fields()
    messagebox.showinfo("Success", "Student details updated successfully.")


def delete_student():
    """Delete the selected student after confirmation."""
    selection = student_table.selection()
    if not selection:
        messagebox.showwarning("Select Student", "Select a student from the table first.")
        return

    student_id = student_table.item(selection[0], "values")[0]
    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete student ID {student_id}?"
    )
    if not confirm:
        return

    students[:] = [student for student in students if student["id"] != student_id]
    save_students()
    refresh_table()
    clear_fields()
    messagebox.showinfo("Success", "Student deleted successfully.")


def search_students():
    """Search by student ID, name, course, or email."""
    query = search_entry.get().strip().lower()
    if not query:
        refresh_table()
        return

    results = [
        student for student in students
        if query in student.get("id", "").lower()
        or query in student.get("name", "").lower()
        or query in student.get("course", "").lower()
        or query in student.get("email", "").lower()
    ]
    refresh_table(results)

    if not results:
        messagebox.showinfo("No Results", "No matching students were found.")


def show_all_students():
    """Display all saved student records."""
    search_entry.delete(0, tk.END)
    refresh_table()


# -------------------- Tkinter GUI --------------------

root = tk.Tk()
root.title("Student Management System")
root.geometry("950x620")
root.minsize(800, 540)

title_label = tk.Label(
    root,
    text="STUDENT MANAGEMENT SYSTEM",
    font=("Arial", 20, "bold"),
    pady=12
)
title_label.pack()

form_frame = tk.LabelFrame(root, text="Student Details", padx=12, pady=10)
form_frame.pack(fill="x", padx=15, pady=5)

tk.Label(form_frame, text="Student ID:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
student_id_entry = tk.Entry(form_frame, width=25)
student_id_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Name:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
name_entry = tk.Entry(form_frame, width=25)
name_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Label(form_frame, text="Age:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
age_entry = tk.Entry(form_frame, width=25)
age_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Course:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
course_entry = tk.Entry(form_frame, width=25)
course_entry.grid(row=1, column=3, padx=5, pady=5)

tk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
email_entry = tk.Entry(form_frame, width=25)
email_entry.grid(row=2, column=1, padx=5, pady=5)

button_frame = tk.Frame(root)
button_frame.pack(fill="x", padx=15, pady=8)

tk.Button(button_frame, text="Add Student", width=15, command=add_student).pack(side="left", padx=5)
tk.Button(button_frame, text="Update Selected", width=15, command=update_student).pack(side="left", padx=5)
tk.Button(button_frame, text="Delete Selected", width=15, command=delete_student).pack(side="left", padx=5)
tk.Button(button_frame, text="Clear Fields", width=12, command=clear_fields).pack(side="left", padx=5)

search_frame = tk.Frame(root)
search_frame.pack(fill="x", padx=15, pady=5)

tk.Label(search_frame, text="Search (ID, name, course, email):").pack(side="left", padx=5)
search_entry = tk.Entry(search_frame, width=30)
search_entry.pack(side="left", padx=5)
tk.Button(search_frame, text="Search", command=search_students).pack(side="left", padx=5)
tk.Button(search_frame, text="Show All", command=show_all_students).pack(side="left", padx=5)

table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=15, pady=10)

columns = ("id", "name", "age", "course", "email")
student_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

student_table.heading("id", text="Student ID")
student_table.heading("name", text="Name")
student_table.heading("age", text="Age")
student_table.heading("course", text="Course")
student_table.heading("email", text="Email")

student_table.column("id", width=100, anchor="center")
student_table.column("name", width=180)
student_table.column("age", width=60, anchor="center")
student_table.column("course", width=160)
student_table.column("email", width=250)

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=student_table.yview)
student_table.configure(yscrollcommand=scrollbar.set)
student_table.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

student_table.bind("<<TreeviewSelect>>", select_student)

load_students()
refresh_table()
root.mainloop()
