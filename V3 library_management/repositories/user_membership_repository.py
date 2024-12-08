# Repository for User-Membership-related queries
# Repository for User-Membership-related queries

from repositories.base_repository import BaseRepository


class UserMembershipRepository(BaseRepository):
    """
    Handles all user membership-related database operations.
    """

    def __init__(self, db_client):
        """
        Initialize the UserMembershipRepository with a database client and ensure the user_memberships table exists.
        """
        super().__init__(db_client, "user_memberships")
        self.create_table(self.get_user_membership_schema())

    def get_user_membership_schema(self):
        """
        Returns the SQL schema for the user_memberships table.
        """
        return """
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL,
            membership_id INT NOT NULL,
            remaining_balance NUMERIC(10, 2) DEFAULT 0.00,
            joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (membership_id) REFERENCES memberships(id) ON DELETE CASCADE
        """

    def get_membership_by_user_id(self, user_id):
        """
        Retrieve membership details for a specific user by their ID.

        :param user_id: The ID of the user.
        :return: A dictionary containing the user's membership details or None if not found.
        """
        try:
            query = f"SELECT * FROM {self.table_name} WHERE user_id = %s;"
            with self.db_client.cursor() as cursor:
                cursor.execute(query, (user_id,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving membership for user ID {user_id}: {e}")
            return None

    def update_balance(self, user_id, new_balance):
        """
        Update the remaining balance for a user's membership.

        :param user_id: The ID of the user.
        :param new_balance: The new balance to set.
        :return: True if the balance was updated successfully, False otherwise.
        """
        try:
            query = f"UPDATE {self.table_name} SET remaining_balance = %s WHERE user_id = %s;"
            with self.db_client.cursor() as cursor:
                cursor.execute(query, (new_balance, user_id))
                self.db_client.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating balance for user ID {user_id}: {e}")
            return False

    def add_user_membership(self, data):
        """
        Add a new user membership to the database.

        :param data: A dictionary containing user membership details.
        :return: The ID of the created user membership or None if the operation fails.
        """
        try:
            return self.insert(data)
        except Exception as e:
            print(f"Error adding user membership: {e}")
            return None

    def list_all_user_memberships(self):
        """
        Retrieve all user memberships from the database.

        :return: A list of dictionaries representing all user memberships.
        """
        try:
            return self.list_all()
        except Exception as e:
            print(f"Error retrieving all user memberships: {e}")
            return []
