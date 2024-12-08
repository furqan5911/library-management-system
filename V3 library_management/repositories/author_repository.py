# Repository for Author-related queries


from repositories.base_repository import BaseRepository


class AuthorRepository(BaseRepository):
    """
    Handles all author-related database operations.
    """

    def __init__(self, db_client):
        """
        Initialize the AuthorRepository with a database client and ensure the authors table exists.
        """
        super().__init__(db_client, "authors")
        self.create_table(self.get_author_schema())

    def get_author_schema(self):
        """
        Returns the SQL schema for the authors table.
        """
        return """
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        """

    def add_author(self, data):
        """
        Add a new author to the database.

        :param data: A dictionary containing author details.
        :return: The ID of the created author or None if the operation fails.
        """
        try:
            return self.insert(data)
        except Exception as e:
            print(f"Unexpected error while adding author: {e}")
            return None

    def list_authors(self):
        """
        Retrieve all authors.

        :return: A list of dictionaries representing all authors.
        """
        try:
            return self.list_all()
        except Exception as e:
            print(f"Error retrieving authors: {e}")
            return []

    def find_by_email(self, email):
        """
        Retrieve an author by their email address.

        :param email: The email of the author.
        :return: A dictionary representing the author, or None if not found.
        """
        try:
            query = f"SELECT * FROM {self.table_name} WHERE email = %s;"
            with self.db_client.cursor() as cursor:
                cursor.execute(query, (email,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving author by email: {e}")
            return None
