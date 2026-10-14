print("=== Day 5: Functions ===")


def greet():
    print("Hello, World!")

def greet_person(name):
    print(f"Hello, {name}!")

greet_person("Alice")
greet_person("Bob")

def add(a, b):
    return a + b

result = add(3, 5)
print(result)

print(add(10, 20))
print(add(add(1, 2), add(3, 4)))

def calculate_average(numbers):
    if len(numbers) == 0:
        return 0
    return round(sum(numbers) / len(numbers), 2)

grades = [1, 2, 3, 4, 5]
print(calculate_average(grades))
print(calculate_average([5, 5, 5]))
print(calculate_average([]))

def is_valid_grade(grade):
    return 1 <= grade <= 5

print(is_valid_grade(3))
print(is_valid_grade(9))

grade = int(input("Enter a grade (1-5): "))

if is_valid_grade(grade):
    print(f"You entered a valid grade: {grade}")
else:
    print("Invalid grade. Please enter a number between 1 and 5.")

def greet_with_title(name, title="Mr./Ms."):
    print(f"Hello, {title} {name}!")

greet_with_title("Smith")
greet_with_title("Smith", " Ms.")



def get_grades():
    grades = []
    while True:
        user_input = input("Enter a grade (1-5) or 'done' to finish: ")
        if user_input == 'done':
            break
        try:
            grade = int(user_input)
            if is_valid_grade(grade):
                grades.append(grade)
                print(f"Added. Current grades: {grades}")
            else:
                print("Invalid grade. Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number or 'done'.")
    return grades

def print_summary(grades):
    if len(grades) == 0:
        print("No grades entered.")
        return
    print(f"Grades: {grades}")
    print(f"Average: {calculate_average(grades)}")
    print(f"Best: {min(grades) }")
    print(f"Worst: {max(grades)}")

collected = get_grades()
print_summary(collected)


def get_best_student(students):
    if len(students) == 0:
        return None
    
    best = students[0]
    for student in students:
        if student['grade'] > best['grade']:
            best = student

    return best

students = [
    {"name": "Alice", "grade": 4},
    {"name": "Bob", "grade": 5},
    {"name": "Charlie", "grade": 3}
]


best = get_best_student(students)
print(f"Best student: {best['name']} with grade {best['grade']}")

empty_result = get_best_student([])

if empty_result is None:
    print("No students.")
else:
    print(empty_result["name"])
    