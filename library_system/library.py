class Library:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.books = []
        self.members = []
        self.staff = []
    
    def add_book(self, book):
        self.books.append(book)
    
    def add_member(self, member):
        self.members.append(member)
    
    def add_staff(self, staff):
        self.staff.append(staff)
        
    def find_book_by_title(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None
