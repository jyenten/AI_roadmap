print("\n === Day: 3 Lists === \n")
# Lists are a collection of items in a particular order. They are mutable, meaning you can change their content without changing their identity.

# Creating a list
numbers = [10, 20, 30, 40]

print(numbers)

print(numbers[0])  # Accessing the first element
print(numbers[1])
print(numbers[-1])

numbers[0] = 99

print(numbers)

numbers.append(50)

print(numbers)

numbers.remove(30)

print(numbers)

print(len(numbers))  # Length of the list

total = 0

for number in numbers:
    total += number
    
    
print(f"Sum of list is: {total}")
print(f"Sum using sum: {sum(numbers)}")
print(f"Minimum value: {min(numbers)}")
print(f"Maximum value: {max(numbers)}")

average = sum(numbers) / len(numbers)
print(f"Average: {round(average, 2)}")

names = ["Jan", "Petr", "Lucie", "Anna"]

print(names)
print(f"First name: {names[0]}")
print(f"Last name: {names[-1]}")

for name in names:
    print(f"Hello, {name}!")

names.append("Martin")
print(names)

names.remove("Petr")
print(names)

if "Anna" in names:
    print("Anna is in the list.")
else:    
    print("Anna is not in the list.")

if "Petr" in names:
    print("Petr is in the list.")
else:
    print("Petr is not in the list.")

print(f"Number of names: {len(names)}")

names.sort(reverse=True)
print(names)

grades  = [1, 2, 3, 1, 4, 2]

print(grades)

print(f"Number of grades: {len(grades)}")
print(f"Average grade: {round(sum(grades) / len(grades), 2)}")
print(f"Best grade: {max(grades)}")
print(f"Worst grade: {min(grades)}")


grade_1_count = 0
grade_2_count = 0
grade_3_count = 0
grade_4_count = 0
grade_5_count = 0


for grade in grades:
    if grade == 1:
        grade_1_count += 1
    elif grade == 2:
        grade_2_count += 1
    elif grade == 3:
        grade_3_count += 1
    elif grade == 4:
        grade_4_count += 1
    elif grade == 5:
        grade_5_count += 1

print(f"Number of 1s: {grade_1_count}")
print(f"Number of 2s: {grade_2_count}")
print(f"Number of 3s: {grade_3_count}")
print(f"Number of 4s: {grade_4_count}")
print(f"Number of 5s: {grade_5_count}")

average_grade = sum(grades) / len(grades)

if average_grade >= 1.5:
    print("Average grade is good.")
elif average_grade <= 2.5:
    print("Average grade is average.")
elif average_grade <= 3.5:
    print("Average grade is bad.")
else:
    print("Weak results.")

print("Counts using count():")
print(f"Number of 1s: {grades.count(1)}")
print(f"Number of 2s: {grades.count(2)}")
print(f"Number of 3s: {grades.count(3)}")
print(f"Number of 4s: {grades.count(4)}")
print(f"Number of 5s: {grades.count(5)}")


new_grades = []

new_grades.append(1)
new_grades.append(2)
new_grades.append(1)

print(new_grades)


student_grades = []

while True:
    user_input = input("Enter a grade 1-5  or type done: ")

    if user_input == "done":
        break

    try:
        grade = int(user_input)

        if 1 <= grade <= 5:
            student_grades.append(grade)
            print(f"Current grades: {student_grades}")
        else:
            print("Invalid grade. Please enter a number between 1 and 5.")

    except ValueError:
        print("Invalid input. Please enter a valid integer.")
