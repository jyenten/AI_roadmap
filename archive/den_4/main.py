print("=== Day 4: Dictionaries ===")

student = { "name": "John", "age": 25, "grade": 1 }

print(student)

print(student["name"])
print(student["age"])

student["age"] = 26
student["city"] = "Ostrava"
print(student)

student.pop("grade")
print(student)

if "name" in student:
    print("Key name exists")
if "grade"  in student:
    print("Key grade exists")
else:
    print("Key grade does not exist")

for key in student:
    print(key)

for key, value in student.items():
    print(f"{key}: {value}")

students = [
    { "name": "John", "age": 25, "grade": 1 },
    { "name": "Alice", "age": 22, "grade": 2 },
    { "name": "Bob", "age": 24, "grade": 1 }
]

for student in students:
    print(student["name"], student["grade"])

best_student = None
best_grade = 6

for student in students:
    if student["grade"] < best_grade:
        best_grade = student["grade"]
        best_student = student["name"]

print(f"Best student: {best_student} with grade {best_grade}")

total = 0

for student in students:
    total += student["grade"]

average = total / len(students)
print(f"Average grade: {average}")

print( "Students with grade better than 2: ")

for student in students:
    if student["grade"] <= 2:
        print(student["name"])

try:

    new_name = input("Enter new name: ")
    new_grade = int(input("Enter student grade (1-5): "))

    if new_grade <= 5:
        students.append({ "name": new_name, "grade": new_grade })
        print(f"Student {new_name} added.")
        print(students)
    else:
        print("Invalid grade.")

except ValueError:
    print("Invalid input. Grade must be a number.")

print("\nAll students:")
for student in students:
    print(f"{student['name']}: {student['grade']}")


students.sort(key=lambda s: s['grade'])

print("\nStudents sorted by grade:")
for student in students:
    print(f"{student['name']}: {student['grade']}")