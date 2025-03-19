from library import Library
from book import Book, EBook, AudioBook
from library_staff import LibraryStaff
from members import Member
from datetime import date, timedelta

def main():
    """Main function to demonstrate the library system."""
    # Create library
    main_library = Library("City Central Library", "123 Book St")
    print(f"Created library: {main_library.name} at {main_library.address}")
    print("-" * 50)
    
    # Add some books
    book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", main_library.name)
    book2 = Book("To Kill a Mockingbird", "Harper Lee", main_library.name)
    ebook1 = EBook("Digital Marketing", "John Smith", main_library.name, "EPUB", 5.2)
    audiobook1 = AudioBook("The Hobbit", "J.R.R. Tolkien", main_library.name, "Andy Serkis", 11.5)
    
    # Add books to library
    main_library.add_book(book1)
    main_library.add_book(book2)
    main_library.add_book(ebook1)
    main_library.add_book(audiobook1)
    
    print("Added books to library:")
    for book in main_library.books:
        print(f"- {book}")
    print("-" * 50)
    
    # Add members and staff
    member1 = Member("John", "Doe", "john@example.com")
    member2 = Member("Alice", "Smith", "alice@example.com")
    staff1 = LibraryStaff("Jane", "Smith", "jane@library.com")
    
    main_library.add_member(member1)
    main_library.add_member(member2)
    main_library.add_staff(staff1)
    
    print(f"Added members: {member1} and {member2}")
    print(f"Added staff: {staff1}")
    print("-" * 50)
    
    # Demo checkout and return
    print(staff1.process_checkout(member1, book1))
    print(f"Checked out books for {member1}: {[book.title for book in member1.checked_out_books]}")
    print(f"Is '{book1.title}' available? {book1.available}")
    
    # Demo checkout of same book by another member (should fail)
    print(staff1.process_checkout(member2, book1))
    
    # Demo return
    print(staff1.process_return(member1, book1))
    print(f"Checked out books for {member1}: {[book.title for book in member1.checked_out_books]}")
    print(f"Is '{book1.title}' available? {book1.available}")
    print("-" * 50)
    
    # Demo e-book checkout (should remain available)
    print(staff1.process_checkout(member1, ebook1))
    print(f"Is '{ebook1.title}' available? {ebook1.available}")
    print("-" * 50)
    
    # Demo search functionality
    print("Searching for book by title 'The Hobbit':")
    search_result = main_library.find_book_by_title("The Hobbit")
    if search_result:
        print(f"Found: {search_result}")
    else:
        print("Book not found")
    print("-" * 50)
    
    # Demo overdue functionality
    book2_checkout = staff1.process_checkout(member1, book2)
    print(book2_checkout)
    
    # Simulate book becoming overdue by manipulating the return date
    # NOTE: In a real system, you wouldn't do this; time would naturally pass
    book2.return_date = date.today() - timedelta(days=5)
    
    print("Checking for overdue books:")
    overdue_report = staff1.generate_overdue_report(main_library)
    print(overdue_report)
    
    # Demo notifications
    print("Sending overdue notifications:")
    notifications = main_library.send_overdue_notifications()
    for notification in notifications:
        print(notification)


if __name__ == "__main__":
    main()
