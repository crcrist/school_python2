from datetime import date, timedelta

class Members:
    # class variables 
    # num_of_books = 0
    # constructor in other lang
    def __init__(self, fname = "", lname = "", email = "", phone_number = "", birthday = "", ssn = "", home_address = ""):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.phone_number = phone_number
        self.birthday = birthday
        self.ssn = ssn
        self.home_address = home_address
        self.checked_out_books = []
        # Book.num_of_books += 1
        
    def sign_up(self):
        print("to become a member of the library, please enter the following information...")

        self.fname = input("first name: ")
        self.lname = input("last name: ")
        self.email = input("email: ")
        self.phone_number = input("phone number: ")
        self.birthday = input("birthday: ")
        self.ssn = input("social security number: ")
        self.home_address = input("home_address: ")

        print("thank you {self.fname} {self.lname}, you have been successfully signed up")


    def checkout_book(self, book):
        if book.available:
            book.checkout_book()
            self.checked_out_books.append(book)
            return f"{self.fname} has checked out {book.title}"
        return f"{book.title} is not available"

    def return_book(self, book):
        if book in self.checked_out_books:
            book.available = True
            book.checkout_date = None
            book.return_date = None
            self.checked_out_books.remove(book)
            return f"{self.fname} has returned {book.title}"
        return f"{self.fname} has not checked out {book.title}"



