# Transaction entity
from datetime import datetime

class Transaction:
    """
    Represents a Transaction entity in the system.

    Attributes:
        id (int): Unique identifier for the transaction.
        user_email (str): Email of the user performing the transaction.
        book_id (int): ID of the book being purchased.
        transaction_date (str): Date and time of the transaction.
        price (float): Price of the transaction.
    """
    def __init__(self, id, user_email, book_id, price):
        self.id = id
        self.user_email = user_email
        self.book_id = book_id
        self.transaction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.price = price

    def to_dict(self):
        """
        Converts the Transaction object into a dictionary for JSON storage.

        :return: Dictionary representation of the Transaction object.
        """
        return {
            "id": self.id,
            "user_email": self.user_email,
            "book_id": self.book_id,
            "transaction_date": self.transaction_date,
            "price": self.price,
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Transaction object from a dictionary.

        :param data: Dictionary containing transaction data.
        :return: Transaction object created from the dictionary data.
        """
        return Transaction(
            id=data["id"],
            user_email=data["user_email"],
            book_id=data["book_id"],
            price=data["price"],
        )
