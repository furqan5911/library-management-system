# Book file
from datetime import datetime


class Book:
    """
    A class used to represent a Book.
    Attributes
    ----------
    title : str
        The title of the book.
    author : str
        The author of the book. Should match an Author's name or ID.
    category : str
        The category of the book. Should match a Category name.
    publication_date : str
        The publication date of the book.
    price : float
        The price of the book.
    isbn : str
        The unique identifier for the book.
    Methods
    -------
    to_dict():
        Converts the Book instance to a dictionary.
    from_dict(data):
        Creates a Book instance from a dictionary.
    """
    """
        Parameters
        ----------
        title : str
            The title of the book.
        author : str
            The author of the book. Should match an Author's name or ID.
        category : str
            The category of the book. Should match a Category name.
        publication_date : str
            The publication date of the book.
        price : float
            The price of the book.
        isbn : str
            The unique identifier for the book.
        """
       
        # Creation code here
    def __init__(self, title, author, category, publication_date, price, isbn):
        self.title = title
        self.author = author  # Should match an Author's name or ID
        self.category = category  # Should match a Category name
        self.publication_date = publication_date
        self.price = price
        self.isbn = isbn  # Unique identifier for the book

    def to_dict(self):
        """
        Converts the Book instance to a dictionary.
        Returns
        -------
        dict
            A dictionary representation of the Book instance.
        """
        return {
            "title": self.title,
            "author": self.author,
            "category": self.category,
            "publication_date": self.publication_date,
            "price": self.price,
            "isbn": self.isbn,
        }

    @staticmethod
    def from_dict(data):
    # Conversion code here
        """
        Creates a Book instance from a dictionary.
        Parameters
        ----------
        data : dict
            A dictionary containing the book data.
        Returns
        -------
        Book
            A Book instance created from the dictionary data.
        """
        return Book(
            data["title"],
            data["author"],
            data["category"],
            data["publication_date"],
            data["price"],
            data["isbn"],
        )