# Author entity
from datetime import datetime

class Author:
    """
    Represents an Author entity in the system.

    Attributes:
        id (int): Unique identifier for the author.
        first_name (str): First name of the author.
        last_name (str): Last name of the author.
        email (str): Email address of the author.
        joined_date (str): Date and time when the author was added.
        books (list): List of book IDs associated with the author.
    """
    def __init__(self, id, first_name, last_name, email):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.joined_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.books = []

    def to_dict(self):
        """
        Converts the Author object into a dictionary for JSON storage.

        :return: Dictionary representation of the Author object.
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "joined_date": self.joined_date,
            "books": self.books,
        }

    @staticmethod
    def from_dict(data):
        """
        Creates an Author object from a dictionary.

        :param data: Dictionary containing author data.
        :return: Author object created from the dictionary data.
        """
        author = Author(
            id=data["id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
        )
        author.books = data.get("books", [])
        return author
