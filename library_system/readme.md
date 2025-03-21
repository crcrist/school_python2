# Library Management System

## Project Overview
This project simulates a library management system in Python. The system allows libraries to manage their book inventory, member accounts, and staff operations through an interactive command-line interface.

## Features

### Core Features
- **Book Management:** Add, search, and track different types of books (regular books, e-books, audiobooks)
- **Member Management:** Sign up new members, track checked-out books, and manage returns
- **Staff Operations:** Process checkouts/returns, manage overdue books, add new inventory
- **Persistent Storage:** Save and load library data using CSV files
- **Notification System:** Send reminders for books due soon and overdue notices

### Book Types
The system supports multiple book types through inheritance:
- **Regular Books:** Traditional physical books with standard checkout policies
- **E-Books:** Digital books with file format and size information
- **Audiobooks:** Audio recordings with narrator and duration information

### User Interfaces
- **Member Interface:** Browse books, search by title/author, view checked-out books, return books
- **Staff Interface:** Process checkouts/returns, view library inventory, manage overdue books, send notifications

## Design Choices

### Class Structure
- **Library:** Central class that maintains books, members, and staff collections
- **Book (Base class):** Contains common properties for all book types
  - **EBook:** Extends Book with digital-specific properties
  - **AudioBook:** Extends Book with audio-specific properties
- **Member:** Represents library members with personal information and checked-out books
- **LibraryStaff:** Represents staff with permissions to process library operations
- **NotificationSystem:** Handles communication with members about their books
- **CSVStorage:** Manages data persistence through CSV files
- **LibraryCLI:** Provides the command-line user interface

### Key Design Decisions
1. **Inheritance for Book Types:** Used inheritance to implement different book types while maintaining common functionality
2. **Separation of Concerns:** Split functionality into discrete classes with specific responsibilities
3. **Waitlist System:** Implemented a waitlist for books that are checked out
4. **Data Persistence:** Used CSV files for simple data storage and retrieval
5. **Notification System:** Created a separate system for handling various types of member notifications

## How to Use the System

### Installation
No additional libraries are required. The system uses Python's standard libraries.


git clone <repository-url>
cd library-management-system
python main.py

### Running the System
Execute `main.py` to start the system:

python main.py

### Main Menu Options
The system presents the following main menu:
1. Member Login
2. Staff Login
3. Sign Up as New Member
4. Exit

### Member Functions
After logging in as a member, you can:
- Browse available books
- Search for books by title or author
- View your checked-out books
- Return books
- View your account information

### Staff Functions
After logging in as staff, you can:
- Process book checkouts for members
- Process book returns
- View all books in the library
- View all library members
- View and manage overdue books
- Send due-soon reminders
- Add new books to the library

## Sample Workflow

### As a Member
1. Sign up as a new member (option 3 from main menu)
2. Login with your email (option 1)
3. Browse books (option 1 from member menu)
4. Checkout a book by entering its number
5. View your checked-out books (option 3)
6. Return a book when finished (option 4)

### As Staff
1. Login with staff email (option 2 from main menu)
2. Process checkouts for members (option 1 from staff menu)
3. View overdue books and send notifications (option 5)
4. Add new books to the inventory (option 7)

## Future Enhancements
- Password authentication for members and staff
- More sophisticated search with fuzzy matching
- Email integration for actual notification delivery
- Web-based user interface

## Project Structure
- `main.py`: Entry point and CLI implementation
- `library.py`: Core library class
- `book.py`: Book classes (base and specialized types)
- `members.py`: Member class implementation
- `library_staff.py`: Staff functionality
- `notification_system.py`: Notification handling
- `csv_storage.py`: Data persistence



