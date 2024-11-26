# Book entity
from datetime import datetime

class Book:
    """
    Represents a Book entity in the system.

    Attributes:
        id (int): Unique identifier for the book.
        title (str): Title of the book.
        author (str): Author of the book.
        category (str): Category of the book.
        publication_date (str): Date when the book was published.
        price (float): Price of the book.
        isbn (str): ISBN number of the book.
    """
    def __init__(self, id, title, author, category, publication_date, price, isbn):
        self.id = id
        self.title = title
        self.author = author
        self.category = category
        self.publication_date = publication_date
        self.price = price
        self.isbn = isbn
        self.added_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """
        Converts the Book object into a dictionary for JSON storage.

        :return: Dictionary representation of the Book object.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "category": self.category,
            "publication_date": self.publication_date,
            "price": self.price,
            "isbn": self.isbn,
            "added_date": self.added_date,
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Book object from a dictionary.

        :param data: Dictionary containing book data.
        :return: Book object created from the dictionary data.
        """
        return Book(
            id=data["id"],
            title=data["title"],
            author=data["author"],
            category=data["category"],
            publication_date=data["publication_date"],
            price=data["price"],
            isbn=data["isbn"],
        )
