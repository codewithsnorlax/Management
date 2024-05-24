import datetime

class Hospital:
    def __init__(self):
        self.patients = []
        self.doctors = []

    def add_patient(self):
        name = input("Enter patient name: ")
        age = int(input("Enter patient age: "))
        gender = input("Enter patient gender: ")
        contact = input("Enter patient contact number: ")
        patient = Patient(name, age, gender, contact)
        self.patients.append(patient)
        print(f"Patient {name} added successfully.\n")

    def add_doctor(self):
        name = input("Enter doctor name: ")
        specialization = input("Enter doctor specialization: ")
        contact = input("Enter doctor contact number: ")
        doctor = Doctor(name, specialization, contact)
        self.doctors.append(doctor)
        print(f"Doctor {name} added successfully.\n")

    def assign_doctor_to_patient(self):
        patient_id = int(input("Enter patient ID: "))
        doctor_id = int(input("Enter doctor ID: "))
        patient = self.find_patient_by_id(patient_id)
        doctor = self.find_doctor_by_id(doctor_id)
        if patient and doctor:
            patient.assign_doctor(doctor)
            print(f"Doctor {doctor.name} assigned to patient {patient.name}.\n")
        else:
            print("Invalid patient ID or doctor ID.\n")

    def schedule_appointment(self):
        patient_id = int(input("Enter patient ID: "))
        doctor_id = int(input("Enter doctor ID: "))
        date = input("Enter appointment date (YYYY-MM-DD): ")
        patient = self.find_patient_by_id(patient_id)
        doctor = self.find_doctor_by_id(doctor_id)
        if patient and doctor:
            appointment = Appointment(patient, doctor, date)
            patient.add_appointment(appointment)
            doctor.add_appointment(appointment)
            print(f"Appointment scheduled for patient {patient.name} with doctor {doctor.name} on {date}.\n")
        else:
            print("Invalid patient ID or doctor ID.\n")

    def view_patients(self):
        if self.patients:
            print("Patients List:")
            for patient in self.patients:
                print(patient)
        else:
            print("No patients found.\n")

    def view_doctors(self):
        if self.doctors:
            print("Doctors List:")
            for doctor in self.doctors:
                print(doctor)
        else:
            print("No doctors found.\n")

    def view_appointments(self):
        patient_id = int(input("Enter patient ID: "))
        patient = self.find_patient_by_id(patient_id)
        if patient:
            print(f"Appointments for patient {patient.name}:")
            for appointment in patient.appointments:
                print(appointment)
        else:
            print("Invalid patient ID.\n")

    def find_patient_by_id(self, patient_id):
        for patient in self.patients:
            if patient.patient_id == patient_id:
                return patient
        return None

    def find_doctor_by_id(self, doctor_id):
        for doctor in self.doctors:
            if doctor.doctor_id == doctor_id:
                return doctor
        return None

class Patient:
    _id_counter = 1

    def __init__(self, name, age, gender, contact):
        self.patient_id = Patient._id_counter
        self.name = name
        self.age = age
        self.gender = gender
        self.contact = contact
        self.doctor = None
        self.appointments = []
        Patient._id_counter += 1

    def assign_doctor(self, doctor):
        self.doctor = doctor

    def add_appointment(self, appointment):
        self.appointments.append(appointment)

    def __str__(self):
        return f"ID: {self.patient_id}, Name: {self.name}, Age: {self.age}, Gender: {self.gender}, Contact: {self.contact}, Doctor: {self.doctor.name if self.doctor else 'None'}"

class Doctor:
    _id_counter = 1

    def __init__(self, name, specialization, contact):
        self.doctor_id = Doctor._id_counter
        self.name = name
        self.specialization = specialization
        self.contact = contact
        self.patients = []
        self.appointments = []
        Doctor._id_counter += 1

    def add_patient(self, patient):
        self.patients.append(patient)

    def add_appointment(self, appointment):
        self.appointments.append(appointment)

    def __str__(self):
        return f"ID: {self.doctor_id}, Name: {self.name}, Specialization: {self.specialization}, Contact: {self.contact}"

class Appointment:
    def __init__(self, patient, doctor, date):
        self.patient = patient
        self.doctor = doctor
        self.date = datetime.datetime.strptime(date, '%Y-%m-%d')

    def __str__(self):
        return f"Patient: {self.patient.name}, Doctor: {self.doctor.name}, Date: {self.date.strftime('%Y-%m-%d')}"

def main():
    hospital = Hospital()
    while True:
        print("Hospital Management System")
        print("1. Add Patient")
        print("2. Add Doctor")
        print("3. Assign Doctor to Patient")
        print("4. Schedule Appointment")
        print("5. View Patients")
        print("6. View Doctors")
        print("7. View Appointments")
        print("8. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            hospital.add_patient()
        elif choice == '2':
            hospital.add_doctor()
        elif choice == '3':
            hospital.assign_doctor_to_patient()
        elif choice == '4':
            hospital.schedule_appointment()
        elif choice == '5':
            hospital.view_patients()
        elif choice == '6':
            hospital.view_doctors()
        elif choice == '7':
            hospital.view_appointments()
        elif choice == '8':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()
