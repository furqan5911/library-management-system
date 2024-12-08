# Service class for Transaction operations


from repositories.transaction_repository import TransactionRepository
from repositories.book_repository import BookRepository
from repositories.user_membership_repository import UserMembershipRepository
from entities.transaction import Transaction
from services.base_service import BaseService
from datetime import datetime


class TransactionService(BaseService):
    """
    Service class for managing transactions in the library system.
    """

    def __init__(self, db_client):
        """
        Initializes the TransactionService with a database client.
        """
        super().__init__()
        self.transaction_repo = TransactionRepository(db_client)
        self.book_repo = BookRepository(db_client)
        self.user_membership_repo = UserMembershipRepository(db_client)

    def record_transaction(self, user_id, book_id, price):
        """
        Records a book purchase transaction.

        :param user_id: The ID of the user.
        :param book_id: The ID of the book being purchased.
        :param price: The price of the book.
        :return: The created transaction record or an error message.
        """
        try:
            # Check if the user has an active membership
            user_membership = self.user_membership_repo.get_membership_by_user_id(user_id)
            if not user_membership:
                return "User does not have an active membership."

            # Ensure the user has sufficient balance
            if user_membership["remaining_balance"] < price:
                return "Insufficient balance to purchase the book."

            # Check if the book is available
            book = self.book_repo.find_by_id(book_id)
            if not book or book["is_sold"]:
                return "Book is either not available or already sold."

            # Deduct the balance and update the user's membership
            new_balance = user_membership["remaining_balance"] - price
            self.user_membership_repo.update_balance(user_id, new_balance)

            # Mark the book as sold
            self.book_repo.mark_as_sold(book_id)

            # Record the transaction
            transaction_data = {
                "user_id": user_id,
                "book_id": book_id,
                "price": price,
                "transaction_date": datetime.now(),
            }
            transaction_id = self.transaction_repo.record_transaction(transaction_data)
            return Transaction(
                id=transaction_id,
                user_id=user_id,
                book_id=book_id,
                price=price,
                transaction_date=transaction_data["transaction_date"],
            ).to_dict()
        except Exception as e:
            self.handle_error("recording transaction", e)
            return None

    def list_transactions_for_user(self, user_id):
        """
        Lists all transactions made by a specific user.

        :param user_id: The ID of the user.
        :return: A list of transactions for the user.
        """
        try:
            transactions = self.transaction_repo.list_user_transactions(user_id)
            return [self.map_to_entity(Transaction, tx).to_dict() for tx in transactions]
        except Exception as e:
            self.handle_error(f"listing transactions for user ID {user_id}", e)
            return []

    def delete_transaction(self, transaction_id):
        """
        Deletes a specific transaction record.

        :param transaction_id: The ID of the transaction to delete.
        :return: True if successful, False otherwise.
        """
        try:
            return self.transaction_repo.delete(transaction_id)
        except Exception as e:
            self.handle_error(f"deleting transaction ID {transaction_id}", e)
            return False
