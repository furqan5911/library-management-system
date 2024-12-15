# Repository for Book-related queries


from repositories.base_repository import BaseRepository
from psycopg2.errors import UniqueViolation


class BookRepository(BaseRepository):
    """
    Handles all book-related database operations.
    """

    def __init__(self, db_client):
        """
        Initialize the BookRepository with a database client and ensure the books table exists.
        """
        super().__init__(db_client, "books")
        self.create_table(self.get_book_schema())

    def get_book_schema(self):
        """
        Returns the SQL schema for the books table.
        """
        return """
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author_id INT NOT NULL,
            category_id INT NOT NULL,
            publication_date DATE NOT NULL,
            price FLOAT NOT NULL,
            isbn VARCHAR(20) UNIQUE NOT NULL,
            is_sold BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
        """

    def add_book(self, data):
        """
        Add a new book to the database.

        :param data: A dictionary containing book details.
        :return: The ID of the created book or None if the operation fails.
        """
        try:
            return self.insert(data)
        except UniqueViolation:
            print(f"Error: Book with ISBN '{data['isbn']}' already exists.")
            return None
        except Exception as e:
            print(f"Unexpected error while adding book: {e}")
            return None

    def mark_as_sold(self, book_id):
        """
        Mark a book as sold by updating its status.

        :param book_id: ID of the book to be marked as sold.
        :return: True if the operation is successful.
        """
        try:
            return self.update(book_id, {"is_sold": True})
        except Exception as e:
            print(f"Error marking book as sold: {e}")
            return False

    def list_books(self):
        """
        Retrieve all books that are not sold.

        :return: A list of dictionaries representing available books.
        """
        try:
            query = f"SELECT * FROM {self.table_name} WHERE is_sold = FALSE;"
            with self.db_client.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving available books: {e}")
            return []

    # def search_books(self, search_criteria, value):
    #     """
    #     Search books by criteria (e.g., title, author_id, or category_id).

    #     :param search_criteria: Column to search (title, author_id, category_id).
    #     :param value: Value to search for.
    #     :return: A list of dictionaries representing matching books.
    #     """
    #     try:
    #         query = f"SELECT * FROM {self.table_name} WHERE {search_criteria} ILIKE %s;"
    #         with self.db_client.cursor() as cursor:
    #             cursor.execute(query, (f"%{value}%",))
    #             return cursor.fetchall()
    #     except Exception as e:
    #         print(f"Error searching books: {e}")
    #         return []

    def search_books(self, search_criteria, value, exact_match=False):
        """
        Searches for books based on the given criteria.

        :param search_criteria: The field to search by (e.g., title, author_id, category_id).
        :param value: The value to search for.
        :param exact_match: Whether to perform an exact match (e.g., for numeric fields like 'id').
        :return: A list of books matching the criteria.
        """
        try:
            if exact_match:
                query = f"SELECT * FROM {self.table_name} WHERE {search_criteria} = %s;"
            else:
                query = f"SELECT * FROM {self.table_name} WHERE {search_criteria} ILIKE %s;"
                value = f"%{value}%"  # Add wildcards for pattern matching

            with self.db_client.cursor() as cursor:
                cursor.execute(query, (value,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error searching books by {search_criteria}: {e}")
            return []


    def list_by_category(self, category_id):
        """
        List books by category.

        :param category_id: ID of the category.
        :return: A list of dictionaries representing books in the category.
        """
        try:
            query = f"SELECT * FROM {self.table_name} WHERE category_id = %s;"
            with self.db_client.cursor() as cursor:
                cursor.execute(query, (category_id,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving books by category: {e}")
            return []

    def list_by_author(self, author_id):
        """
        List books by author.

        :param author_id: ID of the author.
        :return: A list of dictionaries representing books by the author.
        """
        try:
            query = f"SELECT * FROM {self.table_name} WHERE author_id = %s;"
            with self.db_client.cursor() as cursor:
                cursor.execute(query, (author_id,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving books by author: {e}")
            return []

    def ensure_author_and_category(self, author_repo, category_repo, author_data, category_name):
        """
        Ensure the author and category exist before adding a book.

        :param author_repo: An instance of AuthorRepository for managing authors.
        :param category_repo: An instance of CategoryRepository for managing categories.
        :param author_data: A dictionary containing author details (first_name, last_name).
        :param category_name: The name of the book's category.
        :return: A tuple containing the author_id and category_id.
        """
        try:
            # Ensure author exists
            email = f"{author_data['first_name'].lower()}.{author_data['last_name'].lower()}@example.com"
            author = author_repo.find_by_email(email)
            if not author:
                author_id = author_repo.add_author({
                    "first_name": author_data["first_name"],
                    "last_name": author_data["last_name"],
                    "email": email,
                })
            else:
                author_id = author["id"]

            # Ensure category exists
            category = category_repo.find_by_name(category_name)
            if not category:
                category_id = category_repo.add_category({"name": category_name})
            else:
                category_id = category["id"]

            return author_id, category_id

        except Exception as e:
            print(f"Error ensuring author and category: {e}")
            return None, None
