print("==== Day 6: OOP ====")

class Student:

    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def print_info(self):
        print(f"Student: {self.name}, Grade: {self.grade}")

    def is_passing(self):
        return self.grade <= 3
    
    def update_grade(self, new_grade):
        if 1 <= new_grade <= 5:
            self.grade = new_grade
            print(f"Grade updated to {self.grade}.")
        else:
            print("Invalid grade. Grade must be between 1 and 5.")
    
    def __str__(self):
        return f"Student({self.name}, grade= {self.grade})"

    



student1 = Student("John", 1)
student1.print_info()
student1.update_grade(3)
student2 = Student("Anna", 5) 
student2.print_info()
student2.update_grade(9) # Invalid grade


print(student1.is_passing())
print(student2.is_passing())

for student in [student1, student2]:
    if student.is_passing():
        print(f"{student.name} is passing.")
    else:
        print(f"{student.name} is not passing.")

students = [
    Student("Alice", 2),
    Student("Bob", 4),
    Student("Charlie", 3)
]

for student in students:
    student.print_info()


class Classroom: 

    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)
        print(f"{student.name} has been added to the classroom.")

    def print_all(self):
        for student in self.students:
            student.print_info()

    def get_average(self):
        if len(self.students) == 0:
            return None
        total = sum(s.grade for s in self.students)
        return round(total / len(self.students), 2)
    
    def get_best_student(self):
        if len(self.students) == 0:
            return None
        best = self.students[0]
        for student in self.students:
            if student.grade < best.grade:
                best = student
        return best
    
    def get_failing_students(self):
        failing = []
        for student in self.students:
            if not student.is_passing():
                failing.append(student)
        return failing
    
    
    

classroom = Classroom()
classroom.add_student(Student("David", 1))
classroom.add_student(Student("Eve", 4))
classroom.add_student(Student("Frank", 2))

classroom.print_all()

best = classroom.get_best_student()
if best is not None:
    print(f"Best student: {best.name} with grade {best.grade}")

print(f"Class average: {classroom.get_average()}")


failing = classroom.get_failing_students()
print(f"failing students: {len(failing)}")
for student in failing:
    print(f"{student.name}: {student.grade}")

student = Student("Grace", 3)
print(student)