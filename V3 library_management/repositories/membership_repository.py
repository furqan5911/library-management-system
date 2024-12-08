# Repository for Membership-related queries
# Repository for Membership-related queries

from repositories.base_repository import BaseRepository


class MembershipRepository(BaseRepository):
    """
    Handles all membership-related database operations.
    """

    def __init__(self, db_client):
        """
        Initialize the MembershipRepository with a database client and ensure the memberships table exists.
        """
        super().__init__(db_client, "memberships")
        self.create_table(self.get_membership_schema())

    def get_membership_schema(self):
        """
        Returns the SQL schema for the memberships table.
        """
        return """
            id SERIAL PRIMARY KEY,
            plan_name VARCHAR(100) UNIQUE NOT NULL,
            plan_price NUMERIC(10, 2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        """

    def add_membership(self, data):
        """
        Add a new membership plan to the database.

        :param data: A dictionary containing membership plan details.
        :return: The ID of the created membership or None if the operation fails.
        """
        try:
            return self.insert(data)
        except Exception as e:
            print(f"Unexpected error while adding membership: {e}")
            return None

    def list_memberships(self):
        """
        Retrieve all membership plans.

        :return: A list of dictionaries representing all memberships.
        """
        try:
            return self.list_all()
        except Exception as e:
            print(f"Error retrieving memberships: {e}")
            return []

    def update_membership(self, membership_id, data):
        """
        Update an existing membership plan.

        :param membership_id: The ID of the membership to update.
        :param data: A dictionary containing updated membership details.
        :return: True if the update was successful, False otherwise.
        """
        try:
            return self.update(membership_id, data)
        except Exception as e:
            print(f"Error updating membership with ID {membership_id}: {e}")
            return False

    def find_by_name(self, plan_name):
        """
        Retrieve a membership plan by its name.

        :param plan_name: The name of the membership plan.
        :return: A dictionary representing the membership, or None if not found.
        """
        try:
            query = f"SELECT * FROM {self.table_name} WHERE plan_name = %s;"
            with self.db_client.cursor() as cursor:
                cursor.execute(query, (plan_name,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving membership by plan name: {e}")
            return None