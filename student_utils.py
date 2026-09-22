# ============================================
# SNGCE College — Face Attendance System
# Student Utility Functions
# ============================================

import csv
import os

STUDENTS_FILE = os.path.join(os.path.dirname(__file__), "students.csv")
FACES_DIR = os.path.join(os.path.dirname(__file__), "faces")


def _ensure_students_file():
    """Create students.csv with headers if it doesn't exist."""
    if not os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Class"])


def get_all_students():
    """
    Return a list of dicts: [{"ID": ..., "Name": ..., "Class": ...}, ...]
    """
    _ensure_students_file()
    students = []
    with open(STUDENTS_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("Name", "").strip():
                students.append({
                    "ID": row["ID"].strip(),
                    "Name": row["Name"].strip(),
                    "Class": row["Class"].strip(),
                })
    return students


def get_student_count():
    """Return total number of registered students."""
    return len(get_all_students())


def get_student_by_name(name):
    """Lookup a single student by name. Returns dict or None."""
    for s in get_all_students():
        if s["Name"].lower() == name.lower():
            return s
    return None


def add_student(student_id, name, student_class):
    """
    Add a new student to students.csv and create their face folder.
    Returns (True, message) on success, (False, message) on error.
    """
    _ensure_students_file()

    # Validate
    if not student_id or not name or not student_class:
        return False, "All fields are required."

    # Check for duplicates
    existing = get_all_students()
    for s in existing:
        if s["ID"] == student_id:
            return False, f"Student ID {student_id} already exists."
        if s["Name"].lower() == name.lower():
            return False, f"Student '{name}' already exists."

    # Append to CSV
    with open(STUDENTS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([student_id, name, student_class])

    # Create face directory
    os.makedirs(os.path.join(FACES_DIR, name), exist_ok=True)

    return True, f"{name} added successfully!"


def delete_student(student_id):
    """
    Remove a student from students.csv by ID.
    Returns (True, message) on success, (False, message) on error.
    """
    _ensure_students_file()
    students = get_all_students()
    found = None

    for s in students:
        if s["ID"] == student_id:
            found = s
            break

    if not found:
        return False, f"Student ID {student_id} not found."

    # Rewrite CSV without the deleted student
    remaining = [s for s in students if s["ID"] != student_id]

    with open(STUDENTS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Class"])
        for s in remaining:
            writer.writerow([s["ID"], s["Name"], s["Class"]])

    return True, f"{found['Name']} removed successfully."


def search_students(query):
    """
    Search students by name, ID, or class (case-insensitive).
    Returns list of matching student dicts.
    """
    query = query.lower().strip()
    if not query:
        return get_all_students()

    results = []
    for s in get_all_students():
        if (query in s["ID"].lower()
                or query in s["Name"].lower()
                or query in s["Class"].lower()):
            results.append(s)
    return results


def get_classes():
    """Return a sorted list of unique class names."""
    classes = set()
    for s in get_all_students():
        if s["Class"]:
            classes.add(s["Class"])
    return sorted(classes)
