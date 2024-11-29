# BookService class
from abstract_classes.base_service import BaseService
from entities.book import Book
from entities.author import Author
from entities.category import Category
from services.author_service import AuthorService
from services.category_service import CategoryService
import json

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
        find_book_by_id(book_id): Finds a book by its ID.
        mark_as_sold(book_id): Marks a book as sold by removing it from the available books.
    """
    def __init__(self, file_path, author_file_path, category_file_path):
        super().__init__(file_path)
        try:
            self.books = self.load()
        except Exception as e:
            print(f"Error loading books: {e}")
            self.books = []
        
        self.author_file_path = author_file_path
        self.category_file_path = category_file_path
        self.author_service = AuthorService(author_file_path)
        self.category_service = CategoryService(category_file_path)

    def add_book(self, current_user, book_data):
        """
        Adds a new book to the library (Admin-only).
        """
        try:
            if not current_user.is_admin():
                raise PermissionError("Only admins can add books.")

            # Add or update Author in authors.json
            author_name = book_data["author"]
            if len(author_name.split()) < 2:
                raise ValueError("Author name must contain both first and last name.")
            
            author_data = {
                "first_name": author_name.split()[0],
                "last_name": author_name.split()[1],
                "email": "example@example.com"  # Can be customized later
            }
            
            author = self.author_service.add_author(current_user, author_data, source="book_menu")

            # Add or update Category in categories.json
            category_name = book_data["category"]
            self.add_or_update_category(category_name)

            # Create the book and save
            return self.create(book_data)
        
        except PermissionError as e:
            print(f"Error: {e}")
            return None
        except ValueError as e:
            print(f"Error: {e}")  # For the case of missing first or last name
            return None
        except Exception as e:
            print(f"Unexpected error while adding book: {e}")
            return None


    def add_or_update_category(self, category_name):
        """Adds a new category if not already present in categories.json"""
        try:
            categories = self.load_data(self.category_file_path)
            if not any(category["name"] == category_name for category in categories):
                new_category = Category(id=self.get_next_id(categories), name=category_name)
                categories.append(new_category.to_dict())
                self.save_data(self.category_file_path, categories)
                print(f"Category '{category_name}' added successfully!")
            else:
                print(f"Category '{category_name}' already exists.")
        except Exception as e:
            print(f"Error while adding/updating category: {e}")

    def load_data(self, file_path):
        """Helper method to load data from a JSON file."""
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_data(self, file_path, data):
        """Helper method to save data to a JSON file."""
        try:
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def get_next_id(self, data):
        """ Helper function to get the next available category ID. """
        if data:
            return max(item["id"] for item in data) + 1
        return 1

    def list_books(self):
        """
        Lists all available books.
        """
        try:
            return [Book.from_dict(book) for book in self.books]
        except Exception as e:
            print(f"Error while listing books: {e}")
            return []

    def search_books(self, search_criteria, search_value):
        """
        Searches books by name, author, or publication date.
        """
        try:
            if search_criteria not in ["title", "author", "publication_date"]:
                raise ValueError("Invalid search criteria.")
            return [
                Book.from_dict(book)
                for book in self.books
                if search_value.lower() in book[search_criteria].lower()
            ]
        except ValueError as e:
            print(f"Error: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error while searching books: {e}")
            return []

    def list_books_by_category(self, category):
        """
        Lists books filtered by a specific category.
        """
        try:
            return [
                Book.from_dict(book)
                for book in self.books
                if book["category"].lower() == category.lower()
            ]
        except Exception as e:
            print(f"Error while filtering books by category: {e}")
            return []

    def find_book_by_id(self, book_id):
        """
        Finds a book by its ID.
        """
        try:
            return self.find_by_id(book_id)
        except ValueError as e:
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error while finding book: {e}")
            return None

    def mark_as_sold(self, book_id):
        """
        Marks a book as sold by removing it from the available books.
        """
        try:
            self.delete(book_id)
            print(f"Book with ID {book_id} marked as sold.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error while marking book as sold: {e}")



