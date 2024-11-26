# Transaction file
from datetime import datetime

class BooksTransaction:
    def __init__(self, user_email, book_title, transaction_date=None, price=0):
        """
        Initialize a new BooksTransaction instance.

        :param user_email: Email of the user who purchased the book
        :param book_title: Title of the book purchased
        :param transaction_date: Date and time of the transaction (optional, defaults to current date and time)
        :param price: Price of the book purchased (optional, defaults to 0)
        """
        self.user_email = user_email  # Email of the user who purchased the book
        self.book_title = book_title  # Title of the book purchased
        self.transaction_date = transaction_date if transaction_date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Date and time of the transaction
        self.price = price  # Price of the book purchased

    def to_dict(self):
        """
        Convert the transaction object to a dictionary.

        :return: A dictionary representation of the transaction
        """
        return {
            "user_email": self.user_email,
            "book_title": self.book_title,
            "transaction_date": self.transaction_date,
            "price": self.price,
        }

    @staticmethod
    def from_dict(data):
        """
        Create a BooksTransaction object from a dictionary.

        :param data: A dictionary containing transaction data
        :return: A BooksTransaction instance
        """
        return BooksTransaction(
            user_email=data["user_email"],
            book_title=data["book_title"],
            transaction_date=data["transaction_date"],
            price=data["price"],
        )
