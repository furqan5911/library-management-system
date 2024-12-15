# Service class for Book operations


from repositories.book_repository import BookRepository
from entities.book import Book
from entities.author import Author
from entities.category import Category


class BookService:
    """
    Service to manage book-related operations.
    """

    def __init__(self, db_client, author_repository, category_repository):
        self.book_repo = BookRepository(db_client)
        self.author_repository = author_repository
        self.category_repository = category_repository



    def add_book(self, data):
        """
        Adds a new book. Auto-creates author and category if they don't exist.

        :param data: Dictionary containing book details.
        :return: The created book as a dictionary or None if the operation fails.
        """
        try:
            # Ensure the author exists or add a new one
            author_data = {
                "first_name": data.get("author_first_name", "Unknown"),
                "last_name": data.get("author_last_name", "Author"),
                "email": f"{data.get('author_first_name', 'unknown').lower()}.{data.get('author_last_name', 'author').lower()}@example.com"
            }
            author = self.author_repository.add_author(author_data)

            # Adjust logic for author return type
            if isinstance(author, int):  # If an ID is returned
                author_id = author
            elif isinstance(author, dict) and "id" in author:  # If a dictionary is returned
                author_id = author["id"]
            else:
                raise ValueError(f"Failed to add or find the author. Received: {author}")

            # Ensure the category exists or add a new one
            category_data = {"name": data.get("category", "General")}
            category = self.category_repository.add_category(category_data)

            # Adjust logic for category return type
            if isinstance(category, int):  # If an ID is returned
                category_id = category
            elif isinstance(category, dict) and "id" in category:  # If a dictionary is returned
                category_id = category["id"]
            else:
                raise ValueError(f"Failed to add or find the category. Received: {category}")

            # Add the book
            book_data = {
                "title": data["title"],
                "author_id": author_id,
                "category_id": category_id,
                "publication_date": data["publication_date"],
                "price": data["price"],
                "isbn": data["isbn"],
                "is_sold": False
            }
            book_id = self.book_repo.add_book(book_data)

            return Book(
                id=book_id,
                title=book_data["title"],
                author_id=author_id,
                category_id=category_id,
                publication_date=book_data["publication_date"],
                price=book_data["price"],
                isbn=book_data["isbn"],
                is_sold=False
            ).to_dict()

        except Exception as e:
            print(f"Error adding book: {e}")
            return None


    def list_books(self):
        """
        Lists all available books.

        :return: A list of Book entities as dictionaries.
        """
        try:
            books = self.book_repo.list_books()
            return [Book.from_dict(book).to_dict() for book in books]
        except Exception as e:
            print(f"Error listing books: {e}")
            return []

    # def search_books(self, search_criteria, value):
    #     """
    #     Searches books based on the specified criteria.

    #     :param search_criteria: The field to search by (e.g., title, author_id, category_id).
    #     :param value: The value to search for.
    #     :return: A list of matching books.
    #     """
    #     try:
    #         books = self.book_repo.search_books(search_criteria, value)
    #         return [Book.from_dict(book).to_dict() for book in books]
    #     except Exception as e:
    #         print(f"Error searching books: {e}")
    #         return []

    def search_books(self, search_criteria, value):
        """
        Searches books based on the specified criteria.

        :param search_criteria: The field to search by (e.g., title, author_id, category_id).
        :param value: The value to search for.
        :return: A list of matching books.
        """
        try:
            # Handle numeric fields like 'id' with '=' instead of ILIKE
            if search_criteria == "id" and isinstance(value, int):
                books = self.book_repo.search_books(search_criteria, value, exact_match=True)
            else:
                books = self.book_repo.search_books(search_criteria, value)
            return [Book.from_dict(book).to_dict() for book in books]
        except Exception as e:
            print(f"Error searching books: {e}")
            return []


    def mark_as_sold(self, book_id):
        """
        Marks a book as sold.

        :param book_id: The ID of the book to mark as sold.
        :return: True if successful, False otherwise.
        """
        try:
            return self.book_repo.mark_as_sold(book_id)
        except Exception as e:
            print(f"Error marking book ID {book_id} as sold: {e}")
            return False

    def list_by_category(self, category_id):
        """
        Lists books by category.

        :param category_id: The ID of the category.
        :return: A list of books in the category.
        """
        try:
            books = self.book_repo.list_by_category(category_id)
            return [Book.from_dict(book).to_dict() for book in books]
        except Exception as e:
            print(f"Error listing books by category: {e}")
            return []

    def list_by_author(self, author_id):
        """
        Lists books by author.

        :param author_id: The ID of the author.
        :return: A list of books by the author.
        """
        try:
            books = self.book_repo.list_by_author(author_id)
            return [Book.from_dict(book).to_dict() for book in books]
        except Exception as e:
            print(f"Error listing books by author: {e}")
            return []
