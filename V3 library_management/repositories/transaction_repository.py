# Repository for Transaction-related queries
# Repository for Transaction-related queries

from repositories.base_repository import BaseRepository


class TransactionRepository(BaseRepository):
    """
    Handles all transaction-related database operations.
    """

    def __init__(self, db_client):
        """
        Initialize the TransactionRepository with a database client and ensure the transactions table exists.
        """
        super().__init__(db_client, "transactions")
        self.create_table(self.get_transaction_schema())

    def get_transaction_schema(self):
        """
        Returns the SQL schema for the transactions table.
        """
        return """
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL,
            book_id INT NOT NULL,
            price NUMERIC(10, 2) NOT NULL,
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
        """

    def record_transaction(self, data):
        """
        Record a new transaction in the database.

        :param data: A dictionary containing transaction details.
        :return: The ID of the created transaction or None if the operation fails.
        """
        try:
            return self.insert(data)
        except Exception as e:
            print(f"Unexpected error while recording transaction: {e}")
            return None

    def list_user_transactions(self, user_id):
        """
        List all transactions for a given user.

        :param user_id: The ID of the user.
        :return: A list of dictionaries representing transactions for the user.
        """
        try:
            query = f"SELECT * FROM {self.table_name} WHERE user_id = %s;"
            with self.db_client.cursor() as cursor:
                cursor.execute(query, (user_id,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving transactions for user ID {user_id}: {e}")
            return []

    def list_all_transactions(self):
        """
        Retrieve all transactions from the database.

        :return: A list of dictionaries representing all transactions.
        """
        try:
            return self.list_all()
        except Exception as e:
            print(f"Error retrieving all transactions: {e}")
            return []

    def delete_transaction(self, transaction_id):
        """
        Delete a transaction by its ID.

        :param transaction_id: The ID of the transaction to delete.
        :return: True if the transaction was deleted successfully, False otherwise.
        """
        try:
            return self.delete(transaction_id)
        except Exception as e:
            print(f"Error deleting transaction with ID {transaction_id}: {e}")
            return False
