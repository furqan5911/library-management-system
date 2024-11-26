# TransactionService class
from abstract_classes.base_service import BaseService
from entities.transaction import Transaction
import json

class TransactionService(BaseService):
    """
    Handles transaction-related functionality such as recording and viewing transactions.

    Methods:
        record_transaction(user_id, book_id, price): Records a new transaction.
        list_user_transactions(user_id): Lists all transactions for a given user.
    """
    def __init__(self, file_path, user_membership_file):
        super().__init__(file_path)
        self.user_membership_file = user_membership_file

    def load_user_memberships(self):
        """
        Loads user-specific membership data from the file.
        """
        try:
            with open(self.user_membership_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_user_memberships(self, user_memberships):
        """
        Saves user-specific membership data to the file.
        """
        with open(self.user_membership_file, "w") as file:
            json.dump(user_memberships, file, indent=4)

    def record_transaction(self, user_id, book_id, price):
        """
        Records a transaction and deducts the balance from the user's membership plan.

        :param user_id: ID of the user.
        :param book_id: ID of the book being purchased.
        :param price: Price of the book.
        :return: The created Transaction object.
        """
        # Load user memberships
        user_memberships = self.load_user_memberships()
        user_membership = user_memberships.get(user_id)

        if not user_membership:
            raise ValueError("User does not have an active membership plan.")

        # Check if the user has enough balance
        if user_membership["remaining_balance"] < price:
            raise ValueError("Insufficient balance to purchase this book.")

        # Deduct the balance
        user_membership["remaining_balance"] -= price
        user_memberships[user_id] = user_membership
        self.save_user_memberships(user_memberships)

        # Record the transaction
        transaction_data = {
            "user_id": user_id,
            "book_id": book_id,
            "price": price
        }
        created_transaction = self.create(transaction_data)

        print(f"Transaction recorded: Book ID {book_id} purchased for ${price}.")
        return created_transaction

    def list_user_transactions(self, user_id):
        """
        Lists all transactions for a given user.

        :param user_id: ID of the user.
        :return: List of transactions for the user.
        """
        all_transactions = self.load()
        user_transactions = [Transaction.from_dict(tx) for tx in all_transactions if tx["user_id"] == user_id]
        return user_transactions
