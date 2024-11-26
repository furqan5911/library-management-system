# Author file
from datetime import datetime


class Author:
    """
    A class to represent an author.
    Attributes
    ----------
    first_name : str
        The first name of the author.
    last_name : str
        The last name of the author.
    email : str
        The email address of the author.
    joined_date : str, optional
        The date the author joined, defaults to the current date and time if not provided.
    book_title : str, optional
        The title of the book assigned to the author.
    Methods
    -------
    assign_book(book_title):
        Assigns a book to the author.
    to_dict():
        Converts the author object to a dictionary for JSON storage.
    from_dict(data):
        Creates an Author object from a dictionary.
    """
    def __init__(self, first_name, last_name, email, joined_date=None, book_title=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.joined_date = joined_date if joined_date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.book_title = book_title  # Title of the book assigned to the author

    def assign_book(self, book_title):
        """Assign a book to the author."""
        self.book_title = book_title

    def to_dict(self):
        """Convert the author object to a dictionary for JSON storage."""
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "joined_date": self.joined_date,
            "book_title": self.book_title,
        }

    @staticmethod
    def from_dict(data):
        """Create an Author object from a dictionary."""
        return Author(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            joined_date=data.get("joined_date"),
            book_title=data.get("book_title"),
        )
