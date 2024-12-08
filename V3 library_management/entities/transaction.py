# Transaction entity
# Transaction entity

from datetime import datetime


class Transaction:
    """
    Represents a transaction in the library system.

    Attributes:
        id (int): Unique identifier for the transaction.
        user_id (int): The ID of the user who made the transaction.
        book_id (int): The ID of the purchased book.
        price (float): The price of the book at the time of purchase.
        transaction_date (datetime): The date and time when the transaction occurred.
    """

    def __init__(self, id, user_id, book_id, price, transaction_date=None):
        self.id = id
        self.user_id = user_id
        self.book_id = book_id
        self.price = price
        self.transaction_date = transaction_date or datetime.now()

    def to_dict(self):
        """
        Converts the Transaction object into a dictionary.
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "price": self.price,
            "transaction_date": self.transaction_date.strftime("%Y-%m-%d %H:%M:%S"),
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Transaction object from a dictionary.
        """
        return Transaction(
            id=data.get("id"),
            user_id=data.get("user_id"),
            book_id=data.get("book_id"),
            price=data.get("price"),
            transaction_date=data.get("transaction_date"),
        )
