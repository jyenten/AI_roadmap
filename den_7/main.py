print("=== Student Management System ===")

class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
    
    def is_passing(self):
        return self.grade <= 3
    
    def __str__(self):
        status = "passing" if self.is_passing() else "failing"
        return f"{self.name} (grade: {self.grade}, {status})"
    
class Classroom:
    def __init__(self):
        self.students = []
    
    def add_student(self, name, student):
        student = Student(name, grade)
        self.students.append(student)
        print(f"Student {name} added.")

    def remove_student(self, name):
        for student in self.students:
            if student.name == name:
                self.students.remove(student)
                print(f"Student {name} removed.")
                return
        print(f"Student {name} not found.")
    
    def print_all(self):
        if len(self.students) == 0:
            print("No students in the classroom.")
            return
        for student in self.students:
            print(student)
            
    
    def get_average(self):
        if len(self.students) == 0:
            return 0
        return round(sum(s.grade for s in self.students) / len(self.students), 2)
    
    def get_best_student(self):
        if len(self.students) == 0:
            return None
        return min(self.students, key=lambda s: s.grade)
    
def print_menu():
        print("\n=== MENU ===")
        print("1. Add student")
        print("2. Show all students")
        print("3. Show class average")
        print("4. Show best student")
        print("5. Remove student")
        print("6. Exit")


classroom = Classroom()

while True:
    print_menu()
    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Enter student name: ")
        try:
            grade = int(input("Enter grade (1/5): "))
            if 1  <= grade <= 5:
                classroom.add_student(name, grade)
            else:
                print("Invalid grade.")
        except ValueError:
            print("Invalid input.")
    
    elif choice == "2":
        classroom.print_all()

    elif choice == "3":
        avg = classroom.get_average()
        print(f"Class average: {avg}")

    elif choice == "4":
        best = classroom.get_best_student()
        if best is None:
            print("No students")
        else:
           print(f"Best student: {best}")

    elif choice == "5":
        name = input("Enter student name to remove: ")
        classroom.remove_student(name)
      
    elif choice == "6":
        print("Exiting...")
        break

    else:
        print("Invalid choice. Please try again.")



