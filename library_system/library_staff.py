from datetime import date

class LibraryStaff:
    """Class representing a library staff member."""
    
    def __init__(self, fname="", lname="", email="", phone_number="", birthday="", ssn="", home_address=""):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.phone_number = phone_number
        self.birthday = birthday
        self.ssn = ssn
        self.home_address = home_address
        self.id = id(self)  # using object id as a unique identifier
        
    def newly_hired_signup(self):
        """Interactive method to sign up a new staff member."""
        print("To become a staff member of the library, please enter the following information...")
        self.fname = input("First name: ")
        self.lname = input("Last name: ")
        self.email = input("Email: ")
        self.phone_number = input("Phone number: ")
        self.birthday = input("Birthday: ")
        self.ssn = input("Social security number: ")
        self.home_address = input("Home address: ")
        print(f"Thank you {self.fname} {self.lname}, you have been successfully hired")
        
    def process_checkout(self, member, book):
        """Process a book checkout for a member."""
        if book.available:
            result = member.checkout_book(book)
            return f"Staff {self.fname} processed: {result}"
        else:
            # If book is unavailable, offer to add member to waitlist
            if member not in book.waitlist:
                book.add_to_waitlist(member)
                return f"Staff {self.fname} could not process checkout as {book.title} is unavailable. Added {member.fname} to waitlist."
            return f"Staff {self.fname} could not process checkout as {book.title} is unavailable."
    
    def process_return(self, member, book):
        """Process a book return from a member."""
        result = member.return_book(book)
        # Check if anyone is on the waitlist
        if book.waitlist:
            next_member = book.waitlist.pop(0)
            return f"Staff {self.fname} processed: {result}. Notifying {next_member.fname} that the book is now available."
        return f"Staff {self.fname} processed: {result}"
    
    def process_extension(self, member, book, days=7):
        """Process an extension request for a book."""
        if book.waitlist:
            return f"Staff {self.fname} denied extension for {book.title} as there are members waiting for it."
        result = member.request_extension(book, days)
        return f"Staff {self.fname} processed: {result}"
    
    def generate_overdue_report(self, library):
        """Generate a report of all overdue books."""
        overdue_info = library.check_overdue_books()
        if not overdue_info:
            return "No overdue books."
        
        report = "OVERDUE BOOKS REPORT:\n"
        report += "=" * 50 + "\n"
        for member, book in overdue_info:
            days_overdue = (date.today() - book.return_date).days
            report += f"{member.fname} {member.lname} - '{book.title}' - {days_overdue} days overdue\n"
        return report
    
    def __str__(self):
        """String representation of the staff member."""
        return f"Staff: {self.fname} {self.lname} ({self.email})"
