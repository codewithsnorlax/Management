import json
import os

# Data Storage
DATA_FILE = 'hotel_data.json'

# Initialize data storage if it does not exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({"rooms": [], "guests": [], "reservations": []}, f)

# Helper functions to load and save data
def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Room management
class Room:
    def __init__(self, room_number, room_type, price_per_night):
        self.room_number = room_number
        self.room_type = room_type
        self.price_per_night = price_per_night

    def to_dict(self):
        return {"room_number": self.room_number, "room_type": self.room_type, "price_per_night": self.price_per_night}

    @staticmethod
    def from_dict(data):
        return Room(data['room_number'], data['room_type'], data['price_per_night'])

# Guest management
class Guest:
    def __init__(self, name, age, guest_id):
        self.name = name
        self.age = age
        self.guest_id = guest_id

    def to_dict(self):
        return {"name": self.name, "age": self.age, "guest_id": self.guest_id}

    @staticmethod
    def from_dict(data):
        return Guest(data['name'], data['age'], data['guest_id'])

# Reservation management
class Reservation:
    def __init__(self, reservation_id, room_number, guest_id, check_in_date, check_out_date):
        self.reservation_id = reservation_id
        self.room_number = room_number
        self.guest_id = guest_id
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date

    def to_dict(self):
        return {
            "reservation_id": self.reservation_id,
            "room_number": self.room_number,
            "guest_id": self.guest_id,
            "check_in_date": self.check_in_date,
            "check_out_date": self.check_out_date
        }

    @staticmethod
    def from_dict(data):
        return Reservation(data['reservation_id'], data['room_number'], data['guest_id'], data['check_in_date'], data['check_out_date'])

# Main Hotel Management System
class HotelManagementSystem:
    def __init__(self):
        self.data = load_data()
        self.rooms = [Room.from_dict(r) for r in self.data['rooms']]
        self.guests = [Guest.from_dict(g) for g in self.data['guests']]
        self.reservations = [Reservation.from_dict(r) for r in self.data['reservations']]

    def save(self):
        self.data['rooms'] = [r.to_dict() for r in self.rooms]
        self.data['guests'] = [g.to_dict() for g in self.guests]
        self.data['reservations'] = [r.to_dict() for r in self.reservations]
        save_data(self.data)

    def add_room(self, room_number, room_type, price_per_night):
        room = Room(room_number, room_type, price_per_night)
        self.rooms.append(room)
        self.save()
        return room

    def add_guest(self, name, age):
        guest_id = len(self.guests) + 1
        guest = Guest(name, age, guest_id)
        self.guests.append(guest)
        self.save()
        return guest

    def create_reservation(self, room_number, guest_id, check_in_date, check_out_date):
        reservation_id = len(self.reservations) + 1
        if not any(r.room_number == room_number for r in self.rooms):
            raise ValueError("Room number does not exist")
        if not any(g.guest_id == guest_id for g in self.guests):
            raise ValueError("Guest ID does not exist")
        reservation = Reservation(reservation_id, room_number, guest_id, check_in_date, check_out_date)
        self.reservations.append(reservation)
        self.save()
        return reservation

    def get_room_info(self, room_number):
        room = next((r for r in self.rooms if r.room_number == room_number), None)
        if not room:
            raise ValueError("Room not found")
        return room.to_dict()

    def get_guest_info(self, guest_id):
        guest = next((g for g in self.guests if g.guest_id == guest_id), None)
        if not guest:
            raise ValueError("Guest not found")
        return guest.to_dict()

    def get_reservation_info(self, reservation_id):
        reservation = next((r for r in self.reservations if r.reservation_id == reservation_id), None)
        if not reservation:
            raise ValueError("Reservation not found")
        reservation_info = reservation.to_dict()
        reservation_info['guest'] = self.get_guest_info(reservation.guest_id)
        reservation_info['room'] = self.get_room_info(reservation.room_number)
        return reservation_info

# Menu-driven program
def display_menu():
    print("\nHotel Management System")
    print("1. Add Room")
    print("2. Add Guest")
    print("3. Create Reservation")
    print("4. Get Room Info")
    print("5. Get Guest Info")
    print("6. Get Reservation Info")
    print("7. Exit")

def main():
    hms = HotelManagementSystem()
    
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        
        if choice == '1':
            room_number = input("Enter room number: ")
            room_type = input("Enter room type: ")
            price_per_night = float(input("Enter price per night: "))
            room = hms.add_room(room_number, room_type, price_per_night)
            print(f"Added room: {room.to_dict()}")
        
        elif choice == '2':
            name = input("Enter guest name: ")
            age = int(input("Enter guest age: "))
            guest = hms.add_guest(name, age)
            print(f"Added guest: {guest.to_dict()}")
        
        elif choice == '3':
            room_number = input("Enter room number: ")
            guest_id = int(input("Enter guest ID: "))
            check_in_date = input("Enter check-in date (YYYY-MM-DD): ")
            check_out_date = input("Enter check-out date (YYYY-MM-DD): ")
            try:
                reservation = hms.create_reservation(room_number, guest_id, check_in_date, check_out_date)
                print(f"Created reservation: {reservation.to_dict()}")
            except ValueError as e:
                print(e)
        
        elif choice == '4':
            room_number = input("Enter room number: ")
            try:
                room_info = hms.get_room_info(room_number)
                print(f"Room Info: {room_info}")
            except ValueError as e:
                print(e)
        
        elif choice == '5':
            guest_id = int(input("Enter guest ID: "))
            try:
                guest_info = hms.get_guest_info(guest_id)
                print(f"Guest Info: {guest_info}")
            except ValueError as e:
                print(e)
        
        elif choice == '6':
            reservation_id = int(input("Enter reservation ID: "))
            try:
                reservation_info = hms.get_reservation_info(reservation_id)
                print(f"Reservation Info: {reservation_info}")
            except ValueError as e:
                print(e)
        
        elif choice == '7':
            print("Exiting the program.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
