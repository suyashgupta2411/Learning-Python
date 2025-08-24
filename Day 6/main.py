import json
from datetime import datetime, timedelta
import os

DATA_FILE = "library_data.json"


# -------------------- Book Class --------------------
class Book:
    def __init__(self, book_id, title, author, is_available=True):
        self.__book_id = book_id
        self.__title = title
        self.__author = author
        self.__is_available = is_available

    def checkout(self):
        if self.__is_available:
            self.__is_available = False
            return True
        return False

    def return_book(self):
        self.__is_available = True

    def is_available(self):
        return self.__is_available

    def get_details(self):
        return f"[{self.__book_id}] {self.__title} by {self.__author} | {'Available' if self.__is_available else 'Checked out'}"

    def get_id(self):
        return self.__book_id

    def to_dict(self):
        return {
            "book_id": self.__book_id,
            "title": self.__title,
            "author": self.__author,
            "is_available": self.__is_available
        }


# -------------------- Member Class --------------------
class Member:
    def __init__(self, member_id, name, borrowed_books=None, fine=0):
        self.__member_id = member_id
        self.__name = name
        self.__borrowed_books = borrowed_books or {}  # book_id -> due_date string
        self.__fine = fine

    def borrow_book(self, book: Book):
        if book.checkout():
            due_date = datetime.now() + timedelta(days=14)
            self.__borrowed_books[book.get_id()] = due_date.strftime("%Y-%m-%d")
            print(f"\n✅ {self.__name} borrowed '{book.get_details()}' | Due: {due_date.date()}")
        else:
            print(f"\n❌ Sorry, '{book.get_details()}' is not available.")

    def return_book(self, book: Book):
        if book.get_id() in self.__borrowed_books:
            due_date_str = self.__borrowed_books.pop(book.get_id())
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
            book.return_book()
            today = datetime.now()

            if today > due_date:
                days_overdue = (today - due_date).days
                fine_amount = days_overdue * 5
                self.__fine += fine_amount
                print(f"\n⚠️ {self.__name} returned late. Fine added: ₹{fine_amount}")
            else:
                print(f"\n✅ {self.__name} returned on time.")
        else:
            print("\n❌ This book was not borrowed by the member.")

    def get_fine(self):
        return self.__fine

    def pay_fine(self, amount):
        if amount >= self.__fine:
            print(f"\n💰 {self.__name} paid ₹{self.__fine}. No dues left.")
            self.__fine = 0
        else:
            self.__fine -= amount
            print(f"\n💰 {self.__name} paid ₹{amount}. Remaining fine: ₹{self.__fine}")

    def get_details(self):
        return f"Member[{self.__member_id}] {self.__name} | Fine: ₹{self.__fine}"

    def get_id(self):
        return self.__member_id

    def to_dict(self):
        return {
            "member_id": self.__member_id,
            "name": self.__name,
            "borrowed_books": self.__borrowed_books,
            "fine": self.__fine
        }


# -------------------- Library Class --------------------
class Library:
    def __init__(self, name):
        self.__name = name
        self.__books = {}
        self.__members = {}
        self.load_data()

    def add_book(self, book: Book):
        self.__books[book.get_id()] = book
        self.save_data()
        print(f"\n📘 Added {book.get_details()}")

    def add_member(self, member: Member):
        self.__members[member.get_id()] = member
        self.save_data()
        print(f"\n👤 Added {member.get_details()}")

    def get_book(self, book_id):
        return self.__books.get(book_id, None)

    def get_member(self, member_id):
        return self.__members.get(member_id, None)

    def show_books(self):
        print("\n📚 Library Books:")
        if not self.__books:
            print("No books in the library yet.")
        for book in self.__books.values():
            print(book.get_details())

    def show_members(self):
        print("\n👥 Library Members:")
        if not self.__members:
            print("No members registered yet.")
        for member in self.__members.values():
            print(member.get_details())

    # -------------------- Persistence --------------------
    def save_data(self):
        data = {
            "books": {bid: b.to_dict() for bid, b in self.__books.items()},
            "members": {mid: m.to_dict() for mid, m in self.__members.items()}
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            return
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        for bid, bdata in data.get("books", {}).items():
            self.__books[int(bid)] = Book(
                bdata["book_id"], bdata["title"], bdata["author"], bdata["is_available"]
            )

        for mid, mdata in data.get("members", {}).items():
            self.__members[int(mid)] = Member(
                mdata["member_id"], mdata["name"], mdata["borrowed_books"], mdata["fine"]
            )


# -------------------- Main Interactive Program --------------------
def main():
    library = Library("City Library")

    while True:
        print("\n======= 📖 Library Management System =======")
        print("1. Add Book")
        print("2. Add Member")
        print("3. Show Books")
        print("4. Show Members")
        print("5. Borrow Book")
        print("6. Return Book")
        print("7. Pay Fine")
        print("8. Exit")
        choice = input("Enter your choice (1-8): ")

        if choice == "1":
            book_id = int(input("Enter Book ID: "))
            title = input("Enter Book Title: ")
            author = input("Enter Book Author: ")
            library.add_book(Book(book_id, title, author))

        elif choice == "2":
            member_id = int(input("Enter Member ID: "))
            name = input("Enter Member Name: ")
            library.add_member(Member(member_id, name))

        elif choice == "3":
            library.show_books()

        elif choice == "4":
            library.show_members()

        elif choice == "5":
            member_id = int(input("Enter Member ID: "))
            book_id = int(input("Enter Book ID: "))
            member = library.get_member(member_id)
            book = library.get_book(book_id)
            if member and book:
                member.borrow_book(book)
                library.save_data()
            else:
                print("\n❌ Invalid Member ID or Book ID")

        elif choice == "6":
            member_id = int(input("Enter Member ID: "))
            book_id = int(input("Enter Book ID: "))
            member = library.get_member(member_id)
            book = library.get_book(book_id)
            if member and book:
                member.return_book(book)
                library.save_data()
            else:
                print("\n❌ Invalid Member ID or Book ID")

        elif choice == "7":
            member_id = int(input("Enter Member ID: "))
            member = library.get_member(member_id)
            if member:
                print(f"Current fine: ₹{member.get_fine()}")
                amount = int(input("Enter amount to pay: "))
                member.pay_fine(amount)
                library.save_data()
            else:
                print("\n❌ Invalid Member ID")

        elif choice == "8":
            print("\n👋 Exiting Library System. Goodbye!")
            break

        else:
            print("\n❌ Invalid choice, try again.")


if __name__ == "__main__":
    main()
