import json
import os

# Data Storage
DATA_FILE = 'school_data.json'

# Initialize data storage if it does not exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({"students": [], "teachers": [], "classes": []}, f)

# Helper functions to load and save data
def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Student management
class Student:
    def __init__(self, name, age, student_id):
        self.name = name
        self.age = age
        self.student_id = student_id

    def to_dict(self):
        return {"name": self.name, "age": self.age, "student_id": self.student_id}

    @staticmethod
    def from_dict(data):
        return Student(data['name'], data['age'], data['student_id'])

# Teacher management
class Teacher:
    def __init__(self, name, subject, teacher_id):
        self.name = name
        self.subject = subject
        self.teacher_id = teacher_id

    def to_dict(self):
        return {"name": self.name, "subject": self.subject, "teacher_id": self.teacher_id}

    @staticmethod
    def from_dict(data):
        return Teacher(data['name'], data['subject'], data['teacher_id'])

# Class management
class SchoolClass:
    def __init__(self, class_name, teacher_id):
        self.class_name = class_name
        self.teacher_id = teacher_id
        self.students = []

    def add_student(self, student_id):
        self.students.append(student_id)

    def to_dict(self):
        return {
            "class_name": self.class_name,
            "teacher_id": self.teacher_id,
            "students": self.students
        }

    @staticmethod
    def from_dict(data):
        school_class = SchoolClass(data['class_name'], data['teacher_id'])
        school_class.students = data['students']
        return school_class

# Main School Management System
class SchoolManagementSystem:
    def __init__(self):
        self.data = load_data()
        self.students = [Student.from_dict(s) for s in self.data['students']]
        self.teachers = [Teacher.from_dict(t) for t in self.data['teachers']]
        self.classes = [SchoolClass.from_dict(c) for c in self.data['classes']]

    def save(self):
        self.data['students'] = [s.to_dict() for s in self.students]
        self.data['teachers'] = [t.to_dict() for t in self.teachers]
        self.data['classes'] = [c.to_dict() for c in self.classes]
        save_data(self.data)

    def add_student(self, name, age):
        student_id = len(self.students) + 1
        student = Student(name, age, student_id)
        self.students.append(student)
        self.save()
        return student

    def add_teacher(self, name, subject):
        teacher_id = len(self.teachers) + 1
        teacher = Teacher(name, subject, teacher_id)
        self.teachers.append(teacher)
        self.save()
        return teacher

    def create_class(self, class_name, teacher_id):
        if not any(t.teacher_id == teacher_id for t in self.teachers):
            raise ValueError("Teacher ID does not exist")
        school_class = SchoolClass(class_name, teacher_id)
        self.classes.append(school_class)
        self.save()
        return school_class

    def assign_student_to_class(self, student_id, class_name):
        if not any(s.student_id == student_id for s in self.students):
            raise ValueError("Student ID does not exist")
        school_class = next((c for c in self.classes if c.class_name == class_name), None)
        if not school_class:
            raise ValueError("Class does not exist")
        school_class.add_student(student_id)
        self.save()

    def get_student_info(self, student_id):
        student = next((s for s in self.students if s.student_id == student_id), None)
        if not student:
            raise ValueError("Student not found")
        return student.to_dict()

    def get_teacher_info(self, teacher_id):
        teacher = next((t for t in self.teachers if t.teacher_id == teacher_id), None)
        if not teacher:
            raise ValueError("Teacher not found")
        return teacher.to_dict()

    def get_class_info(self, class_name):
        school_class = next((c for c in self.classes if c.class_name == class_name), None)
        if not school_class:
            raise ValueError("Class not found")
        class_info = school_class.to_dict()
        class_info['students'] = [self.get_student_info(sid) for sid in class_info['students']]
        return class_info

# Menu-driven program
def display_menu():
    print("\nSchool Management System")
    print("1. Add Student")
    print("2. Add Teacher")
    print("3. Create Class")
    print("4. Assign Student to Class")
    print("5. Get Student Info")
    print("6. Get Teacher Info")
    print("7. Get Class Info")
    print("8. Exit")

def main():
    sms = SchoolManagementSystem()
    
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        
        if choice == '1':
            name = input("Enter student name: ")
            age = int(input("Enter student age: "))
            student = sms.add_student(name, age)
            print(f"Added student: {student.to_dict()}")
        
        elif choice == '2':
            name = input("Enter teacher name: ")
            subject = input("Enter teacher subject: ")
            teacher = sms.add_teacher(name, subject)
            print(f"Added teacher: {teacher.to_dict()}")
        
        elif choice == '3':
            class_name = input("Enter class name: ")
            teacher_id = int(input("Enter teacher ID: "))
            try:
                school_class = sms.create_class(class_name, teacher_id)
                print(f"Created class: {school_class.to_dict()}")
            except ValueError as e:
                print(e)
        
        elif choice == '4':
            student_id = int(input("Enter student ID: "))
            class_name = input("Enter class name: ")
            try:
                sms.assign_student_to_class(student_id, class_name)
                print(f"Assigned student {student_id} to class {class_name}")
            except ValueError as e:
                print(e)
        
        elif choice == '5':
            student_id = int(input("Enter student ID: "))
            try:
                student_info = sms.get_student_info(student_id)
                print(f"Student Info: {student_info}")
            except ValueError as e:
                print(e)
        
        elif choice == '6':
            teacher_id = int(input("Enter teacher ID: "))
            try:
                teacher_info = sms.get_teacher_info(teacher_id)
                print(f"Teacher Info: {teacher_info}")
            except ValueError as e:
                print(e)
        
        elif choice == '7':
            class_name = input("Enter class name: ")
            try:
                class_info = sms.get_class_info(class_name)
                print(f"Class Info: {class_info}")
            except ValueError as e:
                print(e)
        
        elif choice == '8':
            print("Exiting the program.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
