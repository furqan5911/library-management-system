# BookService class
from abstract_classes.base_service import BaseService
from entities.book import Book

class BookService(BaseService):
    """
    Handles book-related functionality such as adding, updating, deleting, and searching books.

    Methods:
        add_book(current_user, book_data): Adds a new book (Admin-only).
        update_book(current_user, book_id, updated_data): Updates book details (Admin-only).
        delete_book(current_user, book_id): Deletes a book (Admin-only).
        list_books(): Lists all available books (Accessible to all users).
        search_books(search_criteria, search_value): Searches books by name, author, or publication date.
        list_books_by_category(category): Lists books filtered by a specific category.
    """
    def __init__(self, file_path):
        super().__init__(file_path)
        self.books = self.load()

    def add_book(self, current_user, book_data):
        """
        Adds a new book to the library (Admin-only).

        :param current_user: The admin user adding the book.
        :param book_data: Dictionary containing book information.
        :return: The created Book object.
        """
        if not current_user.is_admin():
            raise PermissionError("Only admins can add books.")
        return self.create(book_data)

    def update_book(self, current_user, book_id, updated_data):
        """
        Updates book details (Admin-only).

        :param current_user: The admin user updating the book.
        :param book_id: ID of the book to update.
        :param updated_data: Dictionary containing updated book details.
        :return: The updated Book object.
        """
        if not current_user.is_admin():
            raise PermissionError("Only admins can update books.")
        return self.update(book_id, updated_data)

    def delete_book(self, current_user, book_id):
        """
        Deletes a book from the library (Admin-only).

        :param current_user: The admin user deleting the book.
        :param book_id: ID of the book to delete.
        :return: True if deletion was successful.
        """
        if not current_user.is_admin():
            raise PermissionError("Only admins can delete books.")
        return self.delete(book_id)

    def list_books(self):
        """
        Lists all available books.

        :return: List of all books.
        """
        return [Book.from_dict(book) for book in self.books]

    def search_books(self, search_criteria, search_value):
        """
        Searches books by name, author, or publication date.

        :param search_criteria: The criteria to search by (e.g., 'title', 'author').
        :param search_value: The value to search for.
        :return: List of matching books.
        """
        if search_criteria not in ["title", "author", "publication_date"]:
            raise ValueError("Invalid search criteria.")
        return [
            Book.from_dict(book)
            for book in self.books
            if search_value.lower() in book[search_criteria].lower()
        ]

    def list_books_by_category(self, category):
        """
        Lists books filtered by a specific category.

        :param category: The category to filter by.
        :return: List of books in the specified category.
        """
        return [
            Book.from_dict(book)
            for book in self.books
            if book["category"].lower() == category.lower()
        ]
    
    def find_book_by_id(self, book_id):
        """
        Finds a book by its ID.

        :param book_id: ID of the book.
        :return: The book if found, otherwise None.
        """
        return self.find_by_id(book_id)

    def mark_as_sold(self, book_id):
        """
        Marks a book as sold by removing it from the available books.

        :param book_id: ID of the book to mark as sold.
        """
        self.delete(book_id)
