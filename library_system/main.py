from library import Library
from book import Book, EBook, AudioBook
from library_staff import LibraryStaff
from members import Members

def main():
    # Create library
    main_library = Library("City Central Library", "123 Book St")
    
    # Add some books
    book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", main_library.name)
    ebook1 = EBook("Digital Marketing", "John Smith", main_library.name, "EPUB", 5.2)
    audiobook1 = AudioBook("The Hobbit", "J.R.R. Tolkien", main_library.name, "Andy Serkis", 11.5)
    
    main_library.add_book(book1)
    main_library.add_book(ebook1)
    main_library.add_book(audiobook1)
    
    # Add a member and staff
    member1 = Members("John", "Doe", "john@example.com")
    staff1 = LibraryStaff("Jane", "Smith", "jane@library.com")
    
    main_library.add_member(member1)
    main_library.add_staff(staff1)
    
    # Demo checkout and return
    print(staff1.process_checkout(member1, book1))
    print(member1.checked_out_books)  # Should show the book
    print(book1.available)  # Should be False
    print(staff1.process_return(member1, book1))
    print(member1.checked_out_books)  # Should be empty
    print(book1.available)  # Should be True

if __name__ == "__main__":
    main()
