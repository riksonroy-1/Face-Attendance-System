# ============================================
# SNGCE College — Face Attendance System
# Attendance Analytics Utilities
# ============================================

import csv
import os
from datetime import datetime, timedelta
from collections import defaultdict

ATTENDANCE_FILE = os.path.join(os.path.dirname(__file__), "attendance.csv")
STUDENTS_FILE = os.path.join(os.path.dirname(__file__), "students.csv")


def _ensure_attendance_file():
    """Create attendance.csv with headers if it doesn't exist."""
    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Time", "ID", "Name", "Class", "Status"])


def _load_all_attendance():
    """Load every attendance row as a list of dicts."""
    _ensure_attendance_file()
    records = []
    with open(ATTENDANCE_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("Name", "").strip():
                records.append({
                    "Date": row["Date"].strip(),
                    "Time": row["Time"].strip(),
                    "ID": row["ID"].strip(),
                    "Name": row["Name"].strip(),
                    "Class": row.get("Class", "").strip(),
                    "Status": row.get("Status", "Present").strip(),
                })
    return records


def _load_all_students():
    """Load all students from students.csv."""
    students = []
    if not os.path.exists(STUDENTS_FILE):
        return students
    with open(STUDENTS_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("Name", "").strip():
                students.append({
                    "ID": row["ID"].strip(),
                    "Name": row["Name"].strip(),
                    "Class": row.get("Class", "").strip(),
                })
    return students


# ── Today's Data ────────────────────────────

def get_today_str():
    """Return today's date as YYYY-MM-DD string."""
    return datetime.now().strftime("%Y-%m-%d")


def get_today_attendance():
    """
    Return list of attendance records for today.
    Deduplicates by Name (keeps earliest entry per person).
    """
    today = get_today_str()
    seen = set()
    result = []
    for rec in _load_all_attendance():
        if rec["Date"] == today and rec["Name"] not in seen:
            seen.add(rec["Name"])
            result.append(rec)
    return result


def get_today_present_count():
    """Number of unique students marked present today."""
    return len(get_today_attendance())


def get_today_absent_students():
    """
    Return list of student dicts who are NOT present today.
    """
    today_names = {r["Name"] for r in get_today_attendance()}
    all_students = _load_all_students()
    return [s for s in all_students if s["Name"] not in today_names]


def get_today_absent_count():
    """Number of students absent today."""
    return len(get_today_absent_students())


def get_attendance_rate():
    """
    Today's attendance rate as a float 0–100.
    Returns 0.0 if there are no students.
    """
    total = len(_load_all_students())
    if total == 0:
        return 0.0
    present = get_today_present_count()
    return round((present / total) * 100, 1)


# ── Historical / Filtered ──────────────────

def get_attendance_by_date(date_str):
    """
    Return deduplicated attendance for a specific date (YYYY-MM-DD).
    """
    seen = set()
    result = []
    for rec in _load_all_attendance():
        if rec["Date"] == date_str and rec["Name"] not in seen:
            seen.add(rec["Name"])
            result.append(rec)
    return result


def get_all_attendance():
    """Return every attendance record (not deduplicated)."""
    return _load_all_attendance()


def get_weekly_summary():
    """
    Return a dict mapping each of the last 7 dates (YYYY-MM-DD)
    to the number of unique students present.
    Sorted oldest → newest.
    """
    today = datetime.now().date()
    dates = [(today - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]

    # Pre-process attendance by date
    by_date = defaultdict(set)
    for rec in _load_all_attendance():
        by_date[rec["Date"]].add(rec["Name"])

    summary = {}
    for d in dates:
        summary[d] = len(by_date.get(d, set()))

    return summary


def get_monthly_summary():
    """
    Return a dict mapping each of the last 30 dates (YYYY-MM-DD)
    to the number of unique students present.
    """
    today = datetime.now().date()
    dates = [(today - timedelta(days=i)).isoformat() for i in range(29, -1, -1)]

    by_date = defaultdict(set)
    for rec in _load_all_attendance():
        by_date[rec["Date"]].add(rec["Name"])

    summary = {}
    for d in dates:
        summary[d] = len(by_date.get(d, set()))

    return summary


def get_unique_dates():
    """Return sorted list of all unique dates in attendance."""
    dates = set()
    for rec in _load_all_attendance():
        dates.add(rec["Date"])
    return sorted(dates, reverse=True)


def search_attendance(query):
    """
    Search attendance records by name, ID, class, or date.
    """
    query = query.lower().strip()
    if not query:
        return _load_all_attendance()

    results = []
    for rec in _load_all_attendance():
        if (query in rec["Name"].lower()
                or query in rec["ID"].lower()
                or query in rec["Class"].lower()
                or query in rec["Date"]):
            results.append(rec)
    return results


def get_student_attendance_history(student_name):
    """
    Return all attendance records for a specific student, newest first.
    """
    records = []
    for rec in _load_all_attendance():
        if rec["Name"].lower() == student_name.lower():
            records.append(rec)
    return list(reversed(records))
