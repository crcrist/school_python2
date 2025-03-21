# notification_system.py
from datetime import date, timedelta

class NotificationSystem:
    """Class to handle notifications for the library system."""
    
    def __init__(self):
        """Initialize the notification system."""
        pass
    
    def send_notification(self, member, subject, message):
        """Send a notification to a specific member (simulated).
        
        In a real system, this would send an email or SMS,
        but for this project we'll just print to console.
        """
        print(f"\nNOTIFICATION TO: {member.fname} {member.lname} ({member.email})")
        print(f"SUBJECT: {subject}")
        print(f"MESSAGE: {message}\n")
        return True
    
    def send_overdue_notification(self, member, book):
        """Send an overdue book notification."""
        subject = f"Overdue Book: {book.title}"
        days_overdue = (date.today() - book.return_date).days
        
        message = f"""
Hello {member.fname} {member.lname},

Our records indicate that the following book is {days_overdue} days overdue:

Title: {book.title}
Author: {book.author}
Due Date: {book.return_date}

Please return this book to {book.library} at your earliest convenience.

Thank you,
Library Staff
"""
        
        return self.send_notification(member, subject, message)
    
    def send_due_soon_reminder(self, member, book):
        """Send a reminder for books due soon."""
        days_until_due = (book.return_date - date.today()).days
        subject = f"Reminder: Book Due Soon - {book.title}"
        
        message = f"""
Hello {member.fname} {member.lname},

This is a friendly reminder that the following book is due in {days_until_due} days:

Title: {book.title}
Author: {book.author}
Due Date: {book.return_date}

Please return this book to {book.library} before the due date to avoid late fees.

Thank you,
Library Staff
"""
        
        return self.send_notification(member, subject, message)
    
    def send_book_available_notification(self, member, book):
        """Send notification that a waitlisted book is now available."""
        subject = f"Book Now Available: {book.title}"
        
        message = f"""
Hello {member.fname} {member.lname},

Good news! A book you've been waiting for is now available:

Title: {book.title}
Author: {book.author}

This book will be held for you for the next 3 days. Please visit {book.library} to check it out.

Thank you,
Library Staff
"""
        
        return self.send_notification(member, subject, message)
    
    def check_and_send_due_soon_reminders(self, library):
        """Check all checked out books and send reminders for those due in 3 days."""
        reminders_sent = 0
        
        for member in library.members:
            for book in member.checked_out_books:
                if book.return_date:
                    days_until_due = (book.return_date - date.today()).days
                    if days_until_due == 3:
                        if self.send_due_soon_reminder(member, book):
                            reminders_sent += 1
        
        return f"Sent {reminders_sent} due soon reminders"
