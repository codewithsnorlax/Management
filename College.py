import json
import os

# Data Storage
DATA_FILE = 'college_data.json'

# Initialize data storage if it does not exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({"students": [], "professors": [], "courses": []}, f)

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

# Professor management
class Professor:
    def __init__(self, name, department, professor_id):
        self.name = name
        self.department = department
        self.professor_id = professor_id

    def to_dict(self):
        return {"name": self.name, "department": self.department, "professor_id": self.professor_id}

    @staticmethod
    def from_dict(data):
        return Professor(data['name'], data['department'], data['professor_id'])

# Course management
class Course:
    def __init__(self, course_name, professor_id):
        self.course_name = course_name
        self.professor_id = professor_id
        self.students = []

    def add_student(self, student_id):
        self.students.append(student_id)

    def to_dict(self):
        return {
            "course_name": self.course_name,
            "professor_id": self.professor_id,
            "students": self.students
        }

    @staticmethod
    def from_dict(data):
        course = Course(data['course_name'], data['professor_id'])
        course.students = data['students']
        return course

# Main College Management System
class CollegeManagementSystem:
    def __init__(self):
        self.data = load_data()
        self.students = [Student.from_dict(s) for s in self.data['students']]
        self.professors = [Professor.from_dict(p) for p in self.data['professors']]
        self.courses = [Course.from_dict(c) for c in self.data['courses']]

    def save(self):
        self.data['students'] = [s.to_dict() for s in self.students]
        self.data['professors'] = [p.to_dict() for p in self.professors]
        self.data['courses'] = [c.to_dict() for c in self.courses]
        save_data(self.data)

    def add_student(self, name, age):
        student_id = len(self.students) + 1
        student = Student(name, age, student_id)
        self.students.append(student)
        self.save()
        return student

    def add_professor(self, name, department):
        professor_id = len(self.professors) + 1
        professor = Professor(name, department, professor_id)
        self.professors.append(professor)
        self.save()
        return professor

    def create_course(self, course_name, professor_id):
        if not any(p.professor_id == professor_id for p in self.professors):
            raise ValueError("Professor ID does not exist")
        course = Course(course_name, professor_id)
        self.courses.append(course)
        self.save()
        return course

    def assign_student_to_course(self, student_id, course_name):
        if not any(s.student_id == student_id for s in self.students):
            raise ValueError("Student ID does not exist")
        course = next((c for c in self.courses if c.course_name == course_name), None)
        if not course:
            raise ValueError("Course does not exist")
        course.add_student(student_id)
        self.save()

    def get_student_info(self, student_id):
        student = next((s for s in self.students if s.student_id == student_id), None)
        if not student:
            raise ValueError("Student not found")
        return student.to_dict()

    def get_professor_info(self, professor_id):
        professor = next((p for p in self.professors if p.professor_id == professor_id), None)
        if not professor:
            raise ValueError("Professor not found")
        return professor.to_dict()

    def get_course_info(self, course_name):
        course = next((c for c in self.courses if c.course_name == course_name), None)
        if not course:
            raise ValueError("Course not found")
        course_info = course.to_dict()
        course_info['students'] = [self.get_student_info(sid) for sid in course_info['students']]
        return course_info

# Menu-driven program
def display_menu():
    print("\nCollege Management System")
    print("1. Add Student")
    print("2. Add Professor")
    print("3. Create Course")
    print("4. Assign Student to Course")
    print("5. Get Student Info")
    print("6. Get Professor Info")
    print("7. Get Course Info")
    print("8. Exit")

def main():
    cms = CollegeManagementSystem()
    
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        
        if choice == '1':
            name = input("Enter student name: ")
            age = int(input("Enter student age: "))
            student = cms.add_student(name, age)
            print(f"Added student: {student.to_dict()}")
        
        elif choice == '2':
            name = input("Enter professor name: ")
            department = input("Enter professor department: ")
            professor = cms.add_professor(name, department)
            print(f"Added professor: {professor.to_dict()}")
        
        elif choice == '3':
            course_name = input("Enter course name: ")
            professor_id = int(input("Enter professor ID: "))
            try:
                course = cms.create_course(course_name, professor_id)
                print(f"Created course: {course.to_dict()}")
            except ValueError as e:
                print(e)
        
        elif choice == '4':
            student_id = int(input("Enter student ID: "))
            course_name = input("Enter course name: ")
            try:
                cms.assign_student_to_course(student_id, course_name)
                print(f"Assigned student {student_id} to course {course_name}")
            except ValueError as e:
                print(e)
        
        elif choice == '5':
            student_id = int(input("Enter student ID: "))
            try:
                student_info = cms.get_student_info(student_id)
                print(f"Student Info: {student_info}")
            except ValueError as e:
                print(e)
        
        elif choice == '6':
            professor_id = int(input("Enter professor ID: "))
            try:
                professor_info = cms.get_professor_info(professor_id)
                print(f"Professor Info: {professor_info}")
            except ValueError as e:
                print(e)
        
        elif choice == '7':
            course_name = input("Enter course name: ")
            try:
                course_info = cms.get_course_info(course_name)
                print(f"Course Info: {course_info}")
            except ValueError as e:
                print(e)
        
        elif choice == '8':
            print("Exiting the program.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
