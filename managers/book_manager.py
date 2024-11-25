# Book_manager file
import json
from entities.book import Book

class BookManager:
    """
    A class to manage a collection of books, including loading from and saving to a JSON file,
    as well as adding, updating, removing, and listing books.
    Attributes:
    -----------
    books_file : str
        The path to the JSON file where books are stored.
    books_list : list
        A list to store the book objects.
    Methods:
    --------
    load_books_from_disk():
        Load books from a JSON file on disk.
    save_books_to_disk():
        Save the current list of books to a JSON file on disk.
    add_book(current_user, title, author, category, publication_date, price, isbn):
        Add a new book to the collection (Admin-only).
    update_book(current_user, isbn, updated_data):
        Update an existing book's details (Admin-only).
    remove_book(current_user, isbn):
        Remove a book from the collection by its ISBN (Admin-only).
    list_books():
        List all available books.
    """
    def __init__(self, books_file="books.json"):
        self.books_file = books_file
        self.books_list = []

    def load_books_from_disk(self):
        """Load books from a JSON file."""
        try:
            with open(self.books_file, "r") as file:
                data = json.load(file)
                self.books_list = [Book.from_dict(book) for book in data]
                print("Books loaded successfully!")
        except FileNotFoundError:
            self.books_list = []
            print("No books found. Starting fresh.")

    def save_books_to_disk(self):
        """Save the current books list to a JSON file."""
        with open(self.books_file, "w") as file:
            data = [book.to_dict() for book in self.books_list]
            json.dump(data, file, indent=4)
            print("Books saved successfully!")

    def add_book(self, current_user, title, author, category, publication_date, price, isbn):
        """Add a new book (Admin-only)."""
        if not current_user.is_admin():
            print("Error: Only admins can add books.")
            return False
        if any(book.isbn == isbn for book in self.books_list):
            print(f"Error: Book with ISBN '{isbn}' already exists!")
            return False
        new_book = Book(title, author, category, publication_date, price, isbn)
        self.books_list.append(new_book)
        self.save_books_to_disk()
        print(f"Book '{title}' added successfully!")
        return True

    def update_book(self, current_user, isbn, updated_data):
        """Update an existing book (Admin-only)."""
        if not current_user.is_admin():
            print("Error: Only admins can update books.")
            return False
        for book in self.books_list:
            if book.isbn == isbn:
                for key, value in updated_data.items():
                    setattr(book, key, value)
                self.save_books_to_disk()
                print(f"Book with ISBN '{isbn}' updated successfully!")
                return True
        print(f"Book with ISBN '{isbn}' not found.")
        return False

    def remove_book(self, current_user, isbn):
        """Remove a book by ISBN (Admin-only)."""
        if not current_user.is_admin():
            print("Error: Only admins can remove books.")
            return False
        self.books_list = [book for book in self.books_list if book.isbn != isbn]
        self.save_books_to_disk()
        print(f"Book with ISBN '{isbn}' removed successfully!")
        return True

    def list_books(self):
        """List all available books (Accessible to all users)."""
        if not self.books_list:
            print("No books available!")
        else:
            print("\n=== Available Books ===")
            for book in self.books_list:
                print(f"- {book.title} by {book.author} (Category: {book.category})")
                print(f"  Published: {book.publication_date} | ISBN: {book.isbn} | Price: ${book.price}")
