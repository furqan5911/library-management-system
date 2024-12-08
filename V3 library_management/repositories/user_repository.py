# Repository for User-related queries
# Repository for User-related queries

from repositories.base_repository import BaseRepository
from psycopg2.errors import UniqueViolation


class UserRepository(BaseRepository):
    """
    Handles all user-related database operations.
    """

    def __init__(self, db_client):
        """
        Initialize the UserRepository with a database client and ensure the users table exists.
        """
        super().__init__(db_client, "users")
        self.create_table(self.get_user_schema())

    def get_user_schema(self):
        """
        Returns the SQL schema for the users table.
        """
        return """
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            role VARCHAR(50) DEFAULT 'user'
        """

    def create_user(self, data):
        """
        Add a new user to the database.

        :param data: A dictionary containing user details.
        :return: The ID of the created user or None if the operation fails.
        """
        try:
            return self.insert(data)
        except UniqueViolation:
            print(f"Error: User with email '{data['email']}' already exists.")
            return None
        except Exception as e:
            print(f"Unexpected error while creating user: {e}")
            return None

    def find_by_email(self, email):
        """
        Retrieve a user by their email.

        :param email: The user's email.
        :return: A dictionary representing the user or None if not found.
        """
        try:
            query = f"SELECT * FROM {self.table_name} WHERE email = %s;"
            with self.db_client.cursor() as cursor:
                cursor.execute(query, (email,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error finding user by email: {e}")
            return None

    def login_user(self, email, password):
        """
        Authenticate a user by email and password.

        :param email: The user's email.
        :param password: The user's password.
        :return: A dictionary representing the authenticated user or None if authentication fails.
        """
        try:
            query = f"SELECT * FROM {self.table_name} WHERE email = %s AND password = %s;"
            with self.db_client.cursor() as cursor:
                cursor.execute(query, (email, password))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return None

    def list_all_users(self):
        """
        Retrieve all users from the database.

        :return: A list of dictionaries representing all users.
        """
        try:
            return self.list_all()
        except Exception as e:
            print(f"Error retrieving all users: {e}")
            return []

    def check_admin_exists(self):
        """
        Ensure at least one admin exists in the database.
        If no admin exists, create a default admin account.

        :return: True if an admin exists or was created successfully.
        """
        try:
            query = f"SELECT COUNT(*) FROM {self.table_name} WHERE role = 'admin';"
            with self.db_client.cursor() as cursor:
                cursor.execute(query)
                admin_count = cursor.fetchone()["count"]

            if admin_count == 0:
                print("No admin found. Creating default admin...")
                self.create_user({
                    "first_name": "Default",
                    "last_name": "Admin",
                    "email": "admin@example.com",
                    "password": "adminpass",
                    "role": "admin"
                })
                print("Default admin created.")
            return True
        except Exception as e:
            print(f"Error ensuring admin existence: {e}")
            return False
