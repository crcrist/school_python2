from datetime import date, timedelta

class Book:
    # class variables 
    # num_of_books = 0
    # constructor in other lang
    def __init__(self, title, author, library, return_address=None):
        self.title = title
        self.author = author
        self.library = library
        self.checkout_date = None
        self.return_date = None
        self.return_address = return_address
        self.waitlist = []
        self.available = True
        # Book.num_of_books += 1
        
    def reminder(self):
        days_until_return = self.return_date - self.checkout_date
        return f"your return date is: {self.return_date}, you are {days_until_return.days} days away from needing to return your book!"
    
    def checkout_book(self):
        self.checkout_date = date.today()
        self.return_date = self.checkout_date + timedelta(days = 14)
        self.available = False

class EBook(Book):
    def __init__(self, title, author, library, file_format = "PDF", size_mb = 0):
        super().__init__(title, author, library)
        self.file_format = file_format
        self.size_mb = size_mb
        self.device_compatible = []

class AudioBook(Book):
    def __init__(self, title, author, library, narrator, duration_hours):
        super().__init__(title, author, library)
        self.narrator = narrator
        self.duration_hours = duration_hours

