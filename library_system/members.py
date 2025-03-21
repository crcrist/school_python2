from datetime import timedelta

class Member:
    """Class representing a library member."""
    
    def __init__(self, fname="", lname="", email="", phone_number="", birthday="", ssn="", home_address=""):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.phone_number = phone_number
        self.birthday = birthday
        self.ssn = ssn
        self.home_address = home_address
        self.checked_out_books = []
        self.id = id(self)  # using object id as a unique identifier
        
        # provide personal information to sign up as member of library
    def sign_up(self):
        """interactive method to sign up a new member."""
        print("To become a member of the library, please enter the following information...")
        self.fname = input("First name: ")
        self.lname = input("Last name: ")
        self.email = input("Email: ")
        self.phone_number = input("Phone number: ")
        self.birthday = input("Birthday: ")
        self.ssn = input("Social security number: ")
        self.home_address = input("Home address: ")
        print(f"Thank you {self.fname} {self.lname}, you have been successfully signed up")
      
        # checkout book if it is available, add to list of checked out books for member
    def checkout_book(self, book):
        """check out a book from the library."""
        if book.available:
            book.checkout_book()
            self.checked_out_books.append(book)
            return f"{self.fname} has checked out {book.title}"
        return f"{book.title} is not available"
    
        # if book is in checked out books list and user is returning, make book available to be checked out, and remove from members checked out books list
    def return_book(self, book):
        """return a book to the library."""
        if book in self.checked_out_books:
            book.available = True
            book.checkout_date = None
            book.return_date = None
            self.checked_out_books.remove(book)
            return f"{self.fname} has returned {book.title}"
        return f"{self.fname} has not checked out {book.title}"

    def get_overdue_books(self):
        """get a list of the member's overdue books."""
        return [book for book in self.checked_out_books if book.is_overdue()]
    
        # extend the deadline for return by 7 days
    def request_extension(self, book, days=7):
        """Request an extension on the return date for a book."""
        if book in self.checked_out_books:
            book.return_date += timedelta(days=days)
            return f"Return date for {book.title} extended to {book.return_date}"
        return f"You don't have {book.title} checked out"
    
    def __str__(self):
        """String representation of the member."""
        return f"{self.fname} {self.lname} ({self.email})"
