import csv

students = {}

with open("students.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        students[row["Name"]] = {
            "ID": row["ID"],
            "Class": row["Class"]
        }

print(students)