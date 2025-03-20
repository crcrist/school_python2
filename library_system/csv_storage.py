import csv 
import os
from datetime import datetime, date
from book import Book, EBook, AudioBook
from members import Member
from library_staff import LibraryStaff

# search add on where to add comments

class CSVStorage: 

    def __init__(self, data_dir = "data"):
        # create directory to save files if does not exist already
        self.data_dir = data_dir  # Fixed: added self.data_dir assignment
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def save_books(self, books):
        with open(f"{self.data_dir}/books.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            # write header 
            writer.writerow(['id', 'type', 'title', 'author', 'library', 'available', 'checkout_date', 'return_date', 'extra_data'])

            # write book data
            for book in books:
                # add explanation here
                book_type = book.__class__.__name__
                extra_data = ""

                if book_type == "EBook":
                    extra_data = f"{book.file_format},{book.size_mb}"
                elif book_type == "AudioBook":
                    extra_data = f"{book.narrator},{book.duration_hours}"

                checkout_date = book.checkout_date.isoformat() if book.checkout_date else ""
                return_date = book.return_date.isoformat() if book.return_date else ""

                writer.writerow([
                    book.id,
                    book_type,
                    book.title,
                    book.author,
                    book.library,
                    book.available,
                    checkout_date,
                    return_date,
                    extra_data
                ])

    def load_books(self):
        """ load books from csv file """
        books = []
        try:
            with open(f"{self.data_dir}/books.csv", 'r', newline='') as file:
                reader = csv.reader(file)
                next(reader)

                for row in reader: 
                    book_id, book_type, title, author, library, available, checkout_date, return_date, extra_data = row

                    # create appropriate book object based on type 
                    if book_type == "Book":
                        book = Book(title, author, library)
                    elif book_type == "EBook":
                        file_format, size_mb = extra_data.split(',')
                        book = EBook(title, author, library, file_format, float(size_mb))
                    elif book_type == "AudioBook":
                        narrator, duration_hours = extra_data.split(',')
                        book = AudioBook(title, author, library, narrator, float(duration_hours))

                    # set book properties
                    book.id = int(book_id)
                    book.available = available.lower() == 'true'

                    if checkout_date:
                        book.checkout_date = date.fromisoformat(checkout_date)
                    if return_date:
                        book.return_date = date.fromisoformat(return_date)

                    books.append(book)
        except FileNotFoundError:
                # if file doesnt exist, return empty list
            pass

        return books

    
    def save_members(self, members):
        """save members to csv file"""
        with open(f"{self.data_dir}/members.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            # write header
            writer.writerow(['id', 'fname', 'lname', 'email', 'phone_number', 'birthday', 'home_address', 'checked_out_book_ids'])

            # write member data
            for member in members:
                checked_out_book_ids = [str(book.id) for book in member.checked_out_books]

                writer.writerow([
                    member.id,
                    member.fname,
                    member.lname,
                    member.email,
                    member.phone_number,
                    member.birthday,
                    member.home_address,
                    ','.join(checked_out_book_ids)
                ])

    def load_members(self, books=None):
        """ load members from csv file"""
        members = []
        book_dict = {book.id: book for book in books} if books else{}

        try:
            with open(f"{self.data_dir}/members.csv", 'r', newline='') as file:
                reader = csv.reader(file)
                next(reader) # skip header
                
                for row in reader:
                    member_id, fname, lname, email, phone, birthday, address, checked_out_book_ids = row

                    member = Member(fname, lname, email, phone, birthday, "", address)
                    member.id = int(member_id)

                    # add checked out books if books were provided
                    if checked_out_book_ids and books:
                        for book_id in checked_out_book_ids.split(','):
                            if book_id and int(book_id) in book_dict:
                                member.checked_out_books.append(book_dict[int(book_id)])

                    members.append(member)
        except FileNotFoundError:
            # if file does not exist yet, pass empty list
            pass

        return members

    def save_staff(self, staff_members):
        """ save staff to csv file"""
        with open(f"{self.data_dir}/staff.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            # write header
            writer.writerow(['id', 'fname', 'lname', 'email', 'phone_number', 'birthday', 'home_address'])

            # write staff data
            for staff in staff_members:
                writer.writerow([
                    staff.id,
                    staff.fname,
                    staff.lname,
                    staff.email,
                    staff.phone_number,
                    staff.birthday,
                    staff.home_address
                ])

    def load_staff(self):
        """load staff from csv file"""
        staff_members = []

        try: 
            with open(f"{self.data_dir}/staff.csv", 'r', newline='') as file:
                reader = csv.reader(file)
                next(reader) # skip header

                for row in reader:
                    staff_id, fname, lname, email, phone, birthday, address = row

                    staff = LibraryStaff(fname, lname, email, phone, birthday, "", address)
                    staff.id = int(staff_id)

                    staff_members.append(staff)
        except FileNotFoundError:
            # if file doesn't exist yet, return empty list
            pass

        return staff_members

    def save_library(self, library):
        """save entire library state."""
        # save basic library info
        with open(f"{self.data_dir}/library_info.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'address'])
            writer.writerow([library.name, library.address])

        self.save_books(library.books)
        self.save_members(library.members)
        self.save_staff(library.staff)

        return f"Library data saved to {self.data_dir}/"

    def load_library(self):
        """load entire library state"""
        # is this necessary? 
        from library import Library

        try: 
            with open(f"{self.data_dir}/library_info.csv", 'r', newline='') as file:
                reader = csv.reader(file)
                next(reader)
                name, address = next(reader)

                library = Library(name, address)

                library.books = self.load_books()
                library.members = self.load_members(library.books)
                library.staff = self.load_staff()

                return library
        except FileNotFoundError:
            return None



# ================ TEST CODE ================
if __name__ == "__main__":
    # Initialize storage in a test directory
    test_dir = "test_data"
    storage = CSVStorage(test_dir)
    
    print("=== Simple CSVStorage Test ===")
    
    # 1. Create and save some books
    print("\n1. Creating and saving books")
    books = [
        Book("The Great Gatsby", "F. Scott Fitzgerald", "Main Library"),
        EBook("Digital Fortress", "Dan Brown", "Online Branch", "PDF", 2.5),
        AudioBook("Harry Potter", "J.K. Rowling", "Audio Collection", "Stephen Fry", 8.5)
    ]
    
    # Set some properties
    for i, book in enumerate(books):
        book.id = i + 1
        book.available = True
    
    # Save books
    storage.save_books(books)
    print(f"Saved {len(books)} books to {test_dir}/books.csv")
    
    # 2. Load books
    print("\n2. Loading books")
    loaded_books = storage.load_books()
    print(f"Loaded {len(loaded_books)} books")
    for book in loaded_books:
        print(f"  - {book.title} by {book.author} ({book.__class__.__name__})")
    
    # 3. Create and save members
    print("\n3. Creating and saving members")
    members = [
        Member("John", "Doe", "john@example.com", "555-1234", "1990-01-01", "123", "123 Main St"),
        Member("Jane", "Smith", "jane@example.com", "555-5678", "1985-05-05", "456", "456 Oak Ave")
    ]
    
    # Set IDs and assign books
    for i, member in enumerate(members):
        member.id = i + 1
        member.checked_out_books = [books[i]]  # Each member checks out one book
    
    # Save members
    storage.save_members(members)
    print(f"Saved {len(members)} members to {test_dir}/members.csv")
    
    # 4. Load members
    print("\n4. Loading members")
    loaded_members = storage.load_members(books)
    print(f"Loaded {len(loaded_members)} members")
    for member in loaded_members:
        print(f"  - {member.fname} {member.lname}, Books: {len(member.checked_out_books)}")
        for book in member.checked_out_books:
            print(f"    * {book.title}")
    
    # 5. Create and save staff
    print("\n5. Creating and saving staff")
    staff = [
        LibraryStaff("Bob", "Librarian", "bob@library.com", "555-9876", "1975-03-15", "789", "789 Library Lane")
    ]
    
    # Set IDs
    for i, s in enumerate(staff):
        s.id = i + 1
    
    # Save staff
    storage.save_staff(staff)
    print(f"Saved {len(staff)} staff members to {test_dir}/staff.csv")
    
    # 6. Load staff
    print("\n6. Loading staff")
    loaded_staff = storage.load_staff()
    print(f"Loaded {len(loaded_staff)} staff members")
    for staff_member in loaded_staff:
        print(f"  - {staff_member.fname} {staff_member.lname}")
    
    # 7. Test full library save/load
    print("\n7. Testing full library save/load")
    
    try:
        from library import Library
        
        # Create a test library
        library = Library("Community Library", "123 Library Street")
        library.books = books
        library.members = members
        library.staff = staff
        
        # Save the library
        result = storage.save_library(library)
        print(result)
        
        # Load the library
        loaded_library = storage.load_library()
        print(f"Loaded library: {loaded_library.name}")
        print(f"  - Books: {len(loaded_library.books)}")
        print(f"  - Members: {len(loaded_library.members)}")
        print(f"  - Staff: {len(loaded_library.staff)}")
        
    except ImportError:
        print("Library module not available, skipping full library test")
    
    print("\nTest completed! Files are saved in the '{test_dir}' directory.")
