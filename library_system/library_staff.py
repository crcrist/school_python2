from datetime import date, timedelta

class LibraryStaff:
    # class variables 
    # num_of_books = 0
    # constructor in other lang
    def __init__(self,  fname = "", lname = "", email = "", phone_number = "", birthday = "", ssn = "", home_address = ""):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.phone_number = phone_number
        self.birthday = birthday
        self.ssn = ssn
        self.home_address = home_address
        
    def newly_hired_signup(self):
        print("to become a member of the library, please enter the following information...")

        self.fname = input("first name: ")
        self.lname = input("last name: ")
        self.email = input("email: ")
        self.phone_number = input("phone number: ")
        self.birthday = input("birthday: ")
        self.ssn = input("social security number: ")
        self.home_address = input("home_address: ")

        print("thank you {self.fname} {self.lname}, you have been successfully hired")

    def process_checkout(self, member, book):
        if book.available:
            result = member.checkout_book(book)
            return f"Staff {self.fname} processed: {result}"
        else:
            return f"Staff {self.fname} could not process checkout as {book.title} is unavailable"

    def process_return(self, member, book):
        result = member.return_book(book)
        return f"Staff {self.fname} processed: {result}"


