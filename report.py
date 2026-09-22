import csv

students = []
present = []

# Load all students
with open("students.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        students.append(row["Name"])

# Load attendance
with open("attendance.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        present.append(row["Name"])

print("\n===== ATTENDANCE REPORT =====\n")

print(f"Total Students : {len(students)}")
print(f"Present        : {len(present)}")
print(f"Absent         : {len(students)-len(present)}")

print("\nPresent Students:")

for name in present:
    print("✓", name)

print("\nAbsent Students:")

for name in students:
    if name not in present:
        print("✗", name)