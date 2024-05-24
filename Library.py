import json
import os
from datetime import datetime

# Data Storage
DATA_FILE = 'library_data.json'

# Initialize data storage if it does not exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({"books": [], "members": [], "transactions": []}, f)

# Helper functions to load and save data
def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Book management
class Book:
    def __init__(self, title, author, isbn, book_id):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.book_id = book_id

    def to_dict(self):
        return {"title": self.title, "author": self.author, "isbn": self.isbn, "book_id": self.book_id}

    @staticmethod
    def from_dict(data):
        return Book(data['title'], data['author'], data['isbn'], data['book_id'])

# Member management
class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id

    def to_dict(self):
        return {"name": self.name, "member_id": self.member_id}

    @staticmethod
    def from_dict(data):
        return Member(data['name'], data['member_id'])

# Transaction management
class Transaction:
    def __init__(self, transaction_id, book_id, member_id, borrow_date, return_date=None):
        self.transaction_id = transaction_id
        self.book_id = book_id
        self.member_id = member_id
        self.borrow_date = borrow_date
        self.return_date = return_date

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "book_id": self.book_id,
            "member_id": self.member_id,
            "borrow_date": self.borrow_date,
            "return_date": self.return_date
        }

    @staticmethod
    def from_dict(data):
        return Transaction(data['transaction_id'], data['book_id'], data['member_id'], data['borrow_date'], data.get('return_date'))

# Main Library Management System
class LibraryManagementSystem:
    def __init__(self):
        self.data = load_data()
        self.books = [Book.from_dict(b) for b in self.data['books']]
        self.members = [Member.from_dict(m) for m in self.data['members']]
        self.transactions = [Transaction.from_dict(t) for t in self.data['transactions']]

    def save(self):
        self.data['books'] = [b.to_dict() for b in self.books]
        self.data['members'] = [m.to_dict() for m in self.members]
        self.data['transactions'] = [t.to_dict() for t in self.transactions]
        save_data(self.data)

    def add_book(self, title, author, isbn):
        book_id = len(self.books) + 1
        book = Book(title, author, isbn, book_id)
        self.books.append(book)
        self.save()
        return book

    def add_member(self, name):
        member_id = len(self.members) + 1
        member = Member(name, member_id)
        self.members.append(member)
        self.save()
        return member

    def borrow_book(self, book_id, member_id, borrow_date):
        if not any(b.book_id == book_id for b in self.books):
            raise ValueError("Book ID does not exist")
        if not any(m.member_id == member_id for m in self.members):
            raise ValueError("Member ID does not exist")
        transaction_id = len(self.transactions) + 1
        transaction = Transaction(transaction_id, book_id, member_id, borrow_date)
        self.transactions.append(transaction)
        self.save()
        return transaction

    def return_book(self, transaction_id, return_date):
        transaction = next((t for t in self.transactions if t.transaction_id == transaction_id), None)
        if not transaction:
            raise ValueError("Transaction ID does not exist")
        transaction.return_date = return_date
        self.save()
        return transaction

    def get_book_info(self, book_id):
        book = next((b for b in self.books if b.book_id == book_id), None)
        if not book:
            raise ValueError("Book not found")
        return book.to_dict()

    def get_member_info(self, member_id):
        member = next((m for m in self.members if m.member_id == member_id), None)
        if not member:
            raise ValueError("Member not found")
        return member.to_dict()

    def get_transaction_info(self, transaction_id):
        transaction = next((t for t in self.transactions if t.transaction_id == transaction_id), None)
        if not transaction:
            raise ValueError("Transaction not found")
        transaction_info = transaction.to_dict()
        transaction_info['member'] = self.get_member_info(transaction.member_id)
        transaction_info['book'] = self.get_book_info(transaction.book_id)
        return transaction_info

# Menu-driven program
def display_menu():
    print("\nLibrary Management System")
    print("1. Add Book")
    print("2. Add Member")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Get Book Info")
    print("6. Get Member Info")
    print("7. Get Transaction Info")
    print("8. Exit")

def main():
    lms = LibraryManagementSystem()
    
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        
        if choice == '1':
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            isbn = input("Enter book ISBN: ")
            book = lms.add_book(title, author, isbn)
            print(f"Added book: {book.to_dict()}")
        
        elif choice == '2':
            name = input("Enter member name: ")
            member = lms.add_member(name)
            print(f"Added member: {member.to_dict()}")
        
        elif choice == '3':
            book_id = int(input("Enter book ID: "))
            member_id = int(input("Enter member ID: "))
            borrow_date = input("Enter borrow date (YYYY-MM-DD): ")
            try:
                transaction = lms.borrow_book(book_id, member_id, borrow_date)
                print(f"Borrowed book: {transaction.to_dict()}")
            except ValueError as e:
                print(e)
        
        elif choice == '4':
            transaction_id = int(input("Enter transaction ID: "))
            return_date = input("Enter return date (YYYY-MM-DD): ")
            try:
                transaction = lms.return_book(transaction_id, return_date)
                print(f"Returned book: {transaction.to_dict()}")
            except ValueError as e:
                print(e)
        
        elif choice == '5':
            book_id = int(input("Enter book ID: "))
            try:
                book_info = lms.get_book_info(book_id)
                print(f"Book Info: {book_info}")
            except ValueError as e:
                print(e)
        
        elif choice == '6':
            member_id = int(input("Enter member ID: "))
            try:
                member_info = lms.get_member_info(member_id)
                print(f"Member Info: {member_info}")
            except ValueError as e:
                print(e)
        
        elif choice == '7':
            transaction_id = int(input("Enter transaction ID: "))
            try:
                transaction_info = lms.get_transaction_info(transaction_id)
                print(f"Transaction Info: {transaction_info}")
            except ValueError as e:
                print(e)
        
        elif choice == '8':
            print("Exiting the program.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
