# Database connection management

import psycopg2
from psycopg2.extras import RealDictCursor
import os


class DatabaseConnectionManager:
    """
    Centralized PostgreSQL connection management.

    Attributes:
        connection_url: Database URL or configuration.
        connection: Active database connection.
    """

    def __init__(self):
        """
        Initializes the DatabaseConnectionManager with the database URL.
        Defaults to a local PostgreSQL setup if no environment variable is set.
        """
        self.connection_url = os.getenv(
            "DATABASE_URL", "postgresql://postgres:root@localhost:5432/library_management"
        )
        self.connection = None

    def connect(self):
        """
        Establishes a connection to the PostgreSQL database.
        """
        try:
            if not self.connection or self.connection.closed:
                self.connection = psycopg2.connect(
                    self.connection_url, cursor_factory=RealDictCursor
                )
                print("Connected to the PostgreSQL database successfully.")
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")
            raise

    def get_client(self):
        """
        Returns the active database connection client.
        Ensures the connection is established if not already connected.
        """
        if not self.connection:
            self.connect()
        return self.connection

    def close(self):
        """
        Closes the connection to the PostgreSQL database.
        """
        try:
            if self.connection and not self.connection.closed:
                self.connection.close()
                print("Database connection closed.")
        except psycopg2.Error as e:
            print(f"Error closing the database connection: {e}")
            raise

# db=DatabaseConnectionManager()
# db.connect()