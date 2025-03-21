from datetime import date, timedelta

class NotificationSystem:
    """class to handle notifications for the library system."""

        # since the class does not rely on state it is static, the methods also do not rely on state so will be static as well
    
    @staticmethod
    def send_notification(member, subject, message):
        """Send a notification to a specific member (simulated)."""
        print(f"\nNOTIFICATION TO: {member.fname} {member.lname} ({member.email})")
        print(f"SUBJECT: {subject}")
        print(f"MESSAGE: {message}\n")
        return True
    
    @staticmethod
    def send_overdue_notification(member, book):
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
        
        return NotificationSystem.send_notification(member, subject, message)
    
    @staticmethod
    def send_due_soon_reminder(member, book):
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
        
        return NotificationSystem.send_notification(member, subject, message)
    
    @staticmethod
    def send_book_available_notification(member, book):
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
        
        return NotificationSystem.send_notification(member, subject, message)
    
    @staticmethod
    def check_and_send_due_soon_reminders(library):
        """Check all checked out books and send reminders for those due in 3 days."""
        reminders_sent = 0
        
        for member in library.members:
            for book in member.checked_out_books:
                if book.return_date:
                    days_until_due = (book.return_date - date.today()).days
                    if days_until_due == 3:
                        if NotificationSystem.send_due_soon_reminder(member, book):
                            reminders_sent += 1
        
        return f"Sent {reminders_sent} due soon reminders"
