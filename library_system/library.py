from datetime import date

class Library:
    """Class representing a library with books, members, and staff."""
    
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.books = []
        self.members = []
        self.staff = []
        
    def add_book(self, book):
        """Add a book to the library."""
        self.books.append(book)
        return f"Added {book.title} to {self.name} library"
        
    def add_member(self, member):
        """Add a member to the library."""
        self.members.append(member)
        return f"Added {member.fname} {member.lname} as a member"
        
    def add_staff(self, staff):
        """Add a staff member to the library."""
        self.staff.append(staff)
        return f"Added {staff.fname} {staff.lname} as staff"
        
    def find_book_by_title(self, title):
        """Find a book by its title."""
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None
    
    def find_book_by_author(self, author):
        """Find books by a particular author."""
        results = []
        for book in self.books:
            if book.author.lower() == author.lower():
                results.append(book)
        return results
    
    def find_available_books(self):
        """Find all available books."""
        return [book for book in self.books if book.available]
    
    def check_overdue_books(self):
        """Find all overdue books."""
        overdue_books = []
        for member in self.members:
            for book in member.checked_out_books:
                if book.is_overdue():
                    overdue_books.append((member, book))
        return overdue_books
    
    def send_overdue_notifications(self):
        """Send notifications for overdue books."""
        overdue_info = self.check_overdue_books()
        notifications = []
        for member, book in overdue_info:
            days_overdue = (date.today() - book.return_date).days
            notifications.append(f"NOTIFICATION: {member.fname} {member.lname}, your book '{book.title}' is {days_overdue} days overdue.")
        return notifications
    
