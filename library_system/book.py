
# book.py
from datetime import date, timedelta

class Book:
    """Base class for all types of books in the library system."""
    
    def __init__(self, title, author, library, return_address=None):
        self.title = title
        self.author = author
        self.library = library
        self.checkout_date = None
        self.return_date = None
        self.return_address = return_address
        self.waitlist = []
        self.available = True
        self.id = id(self)  # using object id as a unique identifier
        
    def reminder(self):
        """Generate a reminder message about when the book is due."""
        if self.return_date:
            days_until_return = (self.return_date - date.today()).days
            return f"Your return date is: {self.return_date}, you are {days_until_return} days away from needing to return your book!"
        return "This book is not checked out."
    
    def checkout_book(self):
        """Mark the book as checked out and set return date."""
        self.checkout_date = date.today()
        self.return_date = self.checkout_date + timedelta(days=14)
        self.available = False
        
    def is_overdue(self):
        """Check if the book is overdue."""
        if self.return_date and not self.available:
            return date.today() > self.return_date
        return False
    
    def add_to_waitlist(self, member):
        """Add a member to the book's waitlist."""
        if member not in self.waitlist:
            self.waitlist.append(member)
            return f"{member.fname} {member.lname} added to waitlist for {self.title}"
        return f"{member.fname} {member.lname} is already on the waitlist for {self.title}"
    
    def __str__(self):
        """String representation of the book."""
        status = "Available" if self.available else "Checked Out"
        return f"{self.title} by {self.author} - {status}"


class EBook(Book):
    """Class representing electronic books."""
    
    def __init__(self, title, author, library, file_format="PDF", size_mb=0):
        super().__init__(title, author, library)
        self.file_format = file_format
        self.size_mb = size_mb
        self.device_compatible = ["Kindle", "iPad", "Android tablet", "Computer"]
        
    def checkout_book(self):
        """Override checkout_book for EBooks (they remain available)."""
        self.checkout_date = date.today()
        self.return_date = self.checkout_date + timedelta(days=14)
        # E-books remain available even after checkout
        
    def add_device_compatibility(self, device):
        """Add a compatible device for this ebook."""
        if device not in self.device_compatible:
            self.device_compatible.append(device)
            
    def __str__(self):
        """String representation of the ebook."""
        return f"{self.title} by {self.author} - EBook ({self.file_format}, {self.size_mb} MB)"


class AudioBook(Book):
    """Class representing audio books."""
    
    def __init__(self, title, author, library, narrator, duration_hours):
        super().__init__(title, author, library)
        self.narrator = narrator
        self.duration_hours = duration_hours
        self.format = "MP3"
        
    def set_format(self, format_type):
        """Set the audio format of this audiobook."""
        self.format = format_type
        
    def __str__(self):
        """String representation of the audiobook."""
        return f"{self.title} by {self.author} - AudioBook (Narrator: {self.narrator}, Duration: {self.duration_hours} hours)"

