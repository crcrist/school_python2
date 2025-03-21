from library import Library
from book import Book, EBook, AudioBook
from library_staff import LibraryStaff
from members import Member
from csv_storage import CSVStorage
from notification_system import NotificationSystem
from datetime import date, timedelta
import os


class LibraryCLI:
    """Command-line interface for the library system."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.storage = CSVStorage()
        self.notifications = NotificationSystem()
        
        # try to load existing library, or create a new one
        self.library = self.storage.load_library()
        if not self.library:
            self.library = Library("Centerton Library", "405 S Main St.")
            self._add_sample_data()
        
        self.current_user = None
        self.current_staff = None
   
    # private method as we are just calling internally to generate some fake data for demo
    def _add_sample_data(self):
        """Add sample data to the library if it's new."""
        # add some books for demo
        self.library.add_book(Book("The Great Gatsby", "F. Scott Fitzgerald", self.library.name))
        self.library.add_book(Book("To Kill a Mockingbird", "Harper Lee", self.library.name))
        self.library.add_book(EBook("Digital Marketing", "John Smith", self.library.name, "EPUB", 5.2))
        self.library.add_book(AudioBook("The Hobbit", "J.R.R. Tolkien", self.library.name, "Andy Serkis", 11.5))
        
        # add a member and staff for demo
        self.library.add_member(Member("John", "Doe", "john@example.com"))
        self.library.add_staff(LibraryStaff("Admin", "User", "admin@library.com"))
   
        # clear screen based on OS
    def clear_screen(self):
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def main_menu(self):
        """Display the main menu."""
        self.clear_screen()
        print(f"=== {self.library.name} System ===")
        print("1. Member Login")
        print("2. Staff Login")
        print("3. Sign Up as New Member")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ")
        
        if choice == '1':
            self.member_login()
        elif choice == '2':
            self.staff_login()
        elif choice == '3':
            self.member_signup()
        elif choice == '4':
            print("Saving library data...")
            self.storage.save_library(self.library)
            print("Thank you for using the library system. Goodbye!")
            exit()
        else:
            input("Invalid choice. Press Enter to continue...")
            self.main_menu()
   
        # member enters email to login, does not prompt for password but might be good feature in future
        # also might be nice to have a clock in feature
    def member_login(self):
        """Handle member login."""
        self.clear_screen()
        print("=== Member Login ===")
        email = input("Enter your email: ")
        
        # find member by email
        for member in self.library.members:
            if member.email.lower() == email.lower():
                self.current_user = member
                print(f"Welcome, {member.fname}!")
                input("Press Enter to continue...")
                self.member_menu()
                return
        
        print("Member not found.")
        input("Press Enter to return to main menu...")
        self.main_menu()
    
        # staff logs in with email same as member, potentially add password in future
        # add clock in feature in future
    def staff_login(self):
        """Handle staff login."""
        self.clear_screen()
        print("=== Staff Login ===")
        email = input("Enter your email: ")
        
        # find staff email
        for staff in self.library.staff:
            if staff.email.lower() == email.lower():
                self.current_staff = staff
                print(f"Welcome, {staff.fname}!")
                input("Press Enter to continue...")
                self.staff_menu()
                return
        
        print("Staff member not found.")
        input("Press Enter to return to main menu...")
        self.main_menu()
    
        # member signs up by providing information about themselves
    def member_signup(self):
        """Handle new member signup."""
        self.clear_screen()
        print("=== New Member Signup ===")
        
        member = Member()
        member.sign_up()
        self.library.add_member(member)
        self.storage.save_library(self.library)
        
        print(f"Welcome to the library, {member.fname}!")
        input("Press Enter to continue...")
        self.main_menu()
    
        # displays members menu options
    def member_menu(self):
        """Display the member menu."""
        while True:
            self.clear_screen()
            print(f"=== Member Menu - {self.current_user.fname} {self.current_user.lname} ===")
            print("1. Browse Books")
            print("2. Search Books")
            print("3. View My Books")
            print("4. Return a Book")
            print("5. View My Account")
            print("6. Logout")
            
            choice = input("\nEnter choice (1-6): ")
            
            if choice == '1':
                self.browse_books()
            elif choice == '2':
                self.search_books()
            elif choice == '3':
                self.view_my_books()
            elif choice == '4':
                self.return_book()
            elif choice == '5':
                self.view_account()
            elif choice == '6':
                self.current_user = None
                self.main_menu()
                return
            else:
                input("Invalid choice. Press Enter to continue...")
    
        # display all books, as well as number of members on waitlist for book
    def view_all_books(self):
        """View all books in the library."""
        self.clear_screen()
        print("=== Library Book Inventory ===")
        
        if not self.library.books:
            print("The library has no books.")
        else:
            for i, book in enumerate(self.library.books, 1):
                print(f"{i}. {book}")
                if book.waitlist:
                    print(f"   Waitlist: {len(book.waitlist)} members")
        
        input("\nPress Enter to continue...")
   
        # display all members, as well as number of checked out books per member
    def view_all_members(self):
        """View all library members."""
        self.clear_screen()
        print("=== Library Members ===")
        
        if not self.library.members:
            print("The library has no members.")
        else:
            for i, member in enumerate(self.library.members, 1):
                print(f"{i}. {member}")
                if member.checked_out_books:
                    print(f"   Books checked out: {len(member.checked_out_books)}")
        
        input("\nPress Enter to continue...")
   
        # generates overdue book report that can be generated by the admin, also can send overdue notifications to user
        # in future could add feature to update the notifications class to use smtp to send email reminder to users
    def view_overdue_books(self):
        """View all overdue books."""
        self.clear_screen()
        print("=== Overdue Books ===")
        
        overdue = self.library.check_overdue_books()
        if not overdue:
            print("No overdue books.")
        else:
            print(self.current_staff.generate_overdue_report(self.library))
            
            # Option to send notifications
            send = input("\nSend overdue notifications to members? (y/n): ")
            if send.lower() == 'y':
                for member, book in overdue:
                    self.notifications.send_overdue_notification(member, book)
                print(f"Sent {len(overdue)} notifications.")
        
        input("\nPress Enter to continue...")
    
        # staffs ability to add new books to the library
    def add_new_book(self):
        """Add a new book to the library."""
        self.clear_screen()
        print("=== Add New Book ===")
        print("1. Regular Book")
        print("2. E-Book")
        print("3. Audio Book")
        print("4. Back to Staff Menu")
        
        choice = input("\nEnter choice (1-4): ")
        
        if choice == '4':
            return
        
        title = input("Enter book title: ")
        author = input("Enter author name: ")
        
        if choice == '1':
            book = Book(title, author, self.library.name)
        elif choice == '2':
            file_format = input("Enter file format (default: PDF): ") or "PDF"
            try:
                size_mb = float(input("Enter file size in MB: "))
            except ValueError:
                size_mb = 0
            book = EBook(title, author, self.library.name, file_format, size_mb)
        elif choice == '3':
            narrator = input("Enter narrator name: ")
            try:
                duration = float(input("Enter duration in hours: "))
            except ValueError:
                duration = 0
            book = AudioBook(title, author, self.library.name, narrator, duration)
        else:
            print("Invalid choice.")
            input("Press Enter to continue...")
            return
        
        self.library.add_book(book)
        print(f"Added '{title}' by {author} to the library.")
        
        # Save changes
        self.storage.save_library(self.library)
        input("Press Enter to continue...")
   
        # staffs ability to checkout a book for a specific user
    def process_checkout(self):
        """Process book checkout as staff."""
        self.clear_screen()
        print("=== Process Book Checkout ===")
        
        # First select a member
        print("Select a member:")
        for i, member in enumerate(self.library.members, 1):
            print(f"{i}. {member}")
        
        try:
            member_choice = int(input("\nEnter member number (0 to cancel): "))
            if member_choice == 0:
                return
            
            if 1 <= member_choice <= len(self.library.members):
                member = self.library.members[member_choice - 1]
                
                # Then select a book
                print(f"\nCheckout book for {member.fname} {member.lname}:")
                available_books = self.library.find_available_books()
                
                if not available_books:
                    print("No books are currently available.")
                    input("Press Enter to continue...")
                    return
                
                for i, book in enumerate(available_books, 1):
                    print(f"{i}. {book}")
                
                book_choice = int(input("\nEnter book number (0 to cancel): "))
                if book_choice == 0:
                    return
                
                if 1 <= book_choice <= len(available_books):
                    book = available_books[book_choice - 1]
                    result = self.current_staff.process_checkout(member, book)
                    print(result)
                    
                    # Save changes
                    self.storage.save_library(self.library)
                else:
                    print("Invalid book number.")
            else:
                print("Invalid member number.")
        except ValueError:
            print("Please enter a valid number.")
        
        input("Press Enter to continue...")
   
        # staff ability to process a book returned by member
    def process_return(self):
        """Process book return as staff."""
        self.clear_screen()
        print("=== Process Book Return ===")
        
        # select a member
        print("Select a member:")
        members_with_books = [m for m in self.library.members if m.checked_out_books]
        
        if not members_with_books:
            print("No members have books checked out.")
            input("Press Enter to continue...")
            return
        
        for i, member in enumerate(members_with_books, 1):
            print(f"{i}. {member} ({len(member.checked_out_books)} books)")
        
        try:
            member_choice = int(input("\nEnter member number (0 to cancel): "))
            if member_choice == 0:
                return
            
            if 1 <= member_choice <= len(members_with_books):
                member = members_with_books[member_choice - 1]
                
                # Then select a book
                print(f"\nReturn book for {member.fname} {member.lname}:")
                for i, book in enumerate(member.checked_out_books, 1):
                    print(f"{i}. {book.title} by {book.author}")
                
                book_choice = int(input("\nEnter book number (0 to cancel): "))
                if book_choice == 0:
                    return
                
                if 1 <= book_choice <= len(member.checked_out_books):
                    book = member.checked_out_books[book_choice - 1]
                    result = self.current_staff.process_return(member, book)
                    print(result)
                    
                    # Save changes
                    self.storage.save_library(self.library)
                else:
                    print("Invalid book number.")
            else:
                print("Invalid member number.")
        except ValueError:
            print("Please enter a valid number.")
        
        input("Press Enter to continue...")
   

    def browse_books(self):
        """Display available books and allow checkout."""
        self.clear_screen()
        print("=== Available Books ===")
        
        available_books = self.library.find_available_books()
        if not available_books:
            print("No books are currently available.")
            input("Press Enter to continue...")
            return
        
        for i, book in enumerate(available_books, 1):
            print(f"{i}. {book}")
        
        try:
            choice = int(input("\nEnter book number to checkout (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(available_books):
                book = available_books[choice - 1]
                
                # need a staff member to process checkout
                staff = self.library.staff[0]  # use first staff member
                result = staff.process_checkout(self.current_user, book)
                print(result)
                
                # save changes
                self.storage.save_library(self.library)
            else:
                print("Invalid book number.")
        except ValueError:
            print("Please enter a valid number.")
        
        input("Press Enter to continue...")
    
        # search function, not currently using fuzzy match but would be a good feature in the future
    def search_books(self):
        """Search for books by title or author."""
        self.clear_screen()
        print("=== Search Books ===")
        print("1. Search by Title")
        print("2. Search by Author")
        print("3. Back to Member Menu")
        
        choice = input("\nEnter choice (1-3): ")
        
        if choice == '1':
            title = input("Enter book title: ")
            book = self.library.find_book_by_title(title)
            
            if book:
                print(f"\nFound: {book}")
                if book.available:
                    checkout = input("Would you like to checkout this book? (y/n): ")
                    if checkout.lower() == 'y':
                        staff = self.library.staff[0]  # Use first staff member
                        result = staff.process_checkout(self.current_user, book)
                        print(result)
                        self.storage.save_library(self.library)
                else:
                    waitlist = input("This book is unavailable. Would you like to join the waitlist? (y/n): ")
                    if waitlist.lower() == 'y':
                        result = book.add_to_waitlist(self.current_user)
                        print(result)
                        self.storage.save_library(self.library)
            else:
                print(f"No book found with title '{title}'.")
        
        elif choice == '2':
            author = input("Enter author name: ")
            books = self.library.find_book_by_author(author)
            
            if books:
                print(f"\nFound {len(books)} books by {author}:")
                for i, book in enumerate(books, 1):
                    print(f"{i}. {book}")
            else:
                print(f"No books found by author '{author}'.")
        
        elif choice == '3':
            return
        
        input("\nPress Enter to continue...")
        self.search_books()
   
        # users ability to view the list of their checked out books
    def view_my_books(self):
        """View books checked out by the current user."""
        self.clear_screen()
        print("=== My Checked Out Books ===")
        
        if not self.current_user.checked_out_books:
            print("You don't have any books checked out.")
        else:
            for i, book in enumerate(self.current_user.checked_out_books, 1):
                print(f"{i}. {book.title} by {book.author}")
                if book.return_date:
                    days_left = (book.return_date - date.today()).days
                    status = "OVERDUE" if days_left < 0 else f"{days_left} days left"
                    print(f"   Due: {book.return_date} ({status})")
        
        input("\nPress Enter to continue...")
   
        # users ability to return their books
    def return_book(self):
        """Return a checked out book."""
        self.clear_screen()
        print("=== Return a Book ===")
        
        if not self.current_user.checked_out_books:
            print("You don't have any books to return.")
            input("Press Enter to continue...")
            return
        
        print("Your checked out books:")
        for i, book in enumerate(self.current_user.checked_out_books, 1):
            print(f"{i}. {book.title} by {book.author}")
        
        try:
            choice = int(input("\nEnter book number to return (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(self.current_user.checked_out_books):
                book = self.current_user.checked_out_books[choice - 1]
                
                # need a staff member to process return
                staff = self.library.staff[0]  # use first staff member
                result = staff.process_return(self.current_user, book)
                print(result)
                
                # save changes
                self.storage.save_library(self.library)
            else:
                print("Invalid book number.")
        except ValueError:
            print("Please enter a valid number.")
        
        input("Press Enter to continue...")
        
        # users ability to view account info, add feature to update info in future
    def view_account(self):
        """View current user's account information."""
        self.clear_screen()
        print("=== My Account ===")
        print(f"Name: {self.current_user.fname} {self.current_user.lname}")
        print(f"Email: {self.current_user.email}")
        print(f"Phone: {self.current_user.phone_number}")
        print(f"Books currently checked out: {len(self.current_user.checked_out_books)}")
        
        input("\nPress Enter to continue...")
   
    def staff_menu(self):
        """Display the staff menu."""
        while True:
            self.clear_screen()
            print(f"=== Staff Menu - {self.current_staff.fname} {self.current_staff.lname} ===")
            print("1. Process Book Checkout")
            print("2. Process Book Return")
            print("3. View All Books")
            print("4. View All Members")
            print("5. View Overdue Books")
            print("6. Send Due Soon Reminders")
            print("7. Add New Book")
            print("8. Logout")
            
            choice = input("\nEnter choice (1-8): ")
            
            if choice == '1':
                self.process_checkout()
            elif choice == '2':
                self.process_return()
            elif choice == '3':
                self.view_all_books()
            elif choice == '4':
                self.view_all_members()
            elif choice == '5':
                self.view_overdue_books()
            elif choice == '6':
                result = self.notifications.check_and_send_due_soon_reminders(self.library)
                print(result)
                input("Press Enter to continue...")
            elif choice == '7':
                self.add_new_book()
            elif choice == '8':
                self.current_staff = None
                self.main_menu()
                return
            else:
                input("Invalid choice. Press Enter to continue...")


def main():
    """Main function to run the library system."""
    cli = LibraryCLI()
    cli.main_menu()


if __name__ == "__main__":
    main()
