 # TransactionService class
from abstract_classes.base_service import BaseService
from entities.transaction import Transaction
from datetime import datetime
import json

class TransactionService(BaseService):
    """
    Handles transaction-related functionality such as recording and viewing transactions.

    Methods:
        record_transaction(user_id, user_email, book_id, price): Records a new transaction and deletes the purchased book.
        list_user_transactions(user_identifier): Lists all transactions for a given user.
    """
    def __init__(self, file_path, user_membership_file, book_service):
        super().__init__(file_path)
        self.user_membership_file = user_membership_file
        self.book_service = book_service  # Inject BookService for book management

    def load_user_memberships(self):
        """Loads user-specific membership data from the file."""
        try:
            with open(self.user_membership_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Error: User membership file not found. Starting with empty data.")
            return []
        except Exception as e:
            print(f"Unexpected error while loading user memberships: {e}")
            return []

    def save_user_memberships(self, user_memberships):
        """Saves user-specific membership data to the file."""
        try:
            with open(self.user_membership_file, "w") as file:
                json.dump(user_memberships, file, indent=4)
                print("User memberships saved successfully!")
        except Exception as e:
            print(f"Error while saving user memberships: {e}")

    def record_transaction(self, user_id, user_email, book_id, price):
        """
        Records a transaction, deducts the user's membership balance, 
        and marks the purchased book as sold.

        :param user_id: ID of the user.
        :param user_email: Email of the user.
        :param book_id: ID of the book being purchased.
        :param price: Price of the book.
        :return: The created Transaction object.
        """
        try:
            # Load user memberships
            user_memberships = self.load_user_memberships()

            # Find the user in the list
            user_membership = next(
                (m for m in user_memberships if m["user_id"] == user_id or m.get("email") == user_email),
                None
            )

            if not user_membership:
                print(f"Error: User with ID {user_id} or Email {user_email} does not have an active membership plan.")
                return None

            # Check if the user has enough balance
            if user_membership["remaining_balance"] < price:
                print("Error: Insufficient balance to purchase this book.")
                return None

            # Deduct the balance
            user_membership["remaining_balance"] -= price
            self.save_user_memberships(user_memberships)

            # Record the transaction
            transaction_data = {
                "user_id": user_id,
                "email": user_email,
                "book_id": book_id,
                "price": price,
                "transaction_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            created_transaction = self.create(transaction_data)

            # Mark the book as sold
            book = self.book_service.find_book_by_id(book_id)
            if not book:
                print(f"Error: Book with ID {book_id} not found.")
                return None
            self.book_service.mark_as_sold(book_id)
            print(f"Book with ID {book_id} has been marked as sold and removed from the catalog.")

            print(f"Transaction recorded: Book ID {book_id} purchased for ${price}.")
            return created_transaction
        except ValueError as e:
            print(f"Validation error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error while recording transaction: {e}")
            return None

    def list_user_transactions(self, user_identifier):
        """
        Lists all transactions for a given user.

        :param user_identifier: Can be user ID (int) or email (str).
        :return: List of transactions for the user.
        """
        try:
            all_transactions = self.load()
            print(f"Loaded transactions: {all_transactions}")
            print(f"Filtering transactions for user identifier: {user_identifier}")
            
            user_transactions = [
                Transaction.from_dict(tx)
                for tx in all_transactions
                if tx.get("user_id") == user_identifier or tx.get("email") == user_identifier
            ]

            print(f"Filtered user transactions: {user_transactions}")
            return user_transactions
        except Exception as e:
            print(f"Error while listing transactions: {e}")
            return []


