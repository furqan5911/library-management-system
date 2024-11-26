import json
from entities.book import Book

class BookManager:
    """
    Attributes:
        books_file (str): The path to the JSON file where books are stored.
        books_list (list): A list to store the collection of books.
    Methods:
        load_books_from_disk():
            Load books from a JSON file.
        save_books_to_disk():
            Save the current books list to a JSON file.
        add_book(current_user, title, author, category, publication_date, price, isbn):
            Add a new book (Admin-only).
        update_book(current_user, isbn, updated_data):
            Update an existing book (Admin-only).
        remove_book(current_user, isbn):
            Remove a book by ISBN (Admin-only).
        list_books():
            List all available books (Accessible to all users).
        list_books_by_category(category):
            List books filtered by a specific category.
        search_books(search_criteria, search_value):"""
    """
    A class to manage a collection of books, including loading from and saving to a JSON file,
    as well as adding, updating, removing, and listing books.
    """
    def __init__(self, books_file="books.json"):
        self.books_file = books_file
        # Initialize an empty list to store the collection of books
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

    def list_books_by_category(self, category):
        """List books filtered by a specific category."""
        filtered_books = [book for book in self.books_list if book.category.lower() == category.lower()]
        if not filtered_books:
            print(f"No books found in the category '{category}'.")
            return
        print(f"\n=== Books in Category: {category} ===")
        for book in filtered_books:
            print(f"- {book.title} by {book.author} (Price: ${book.price})")
            print(f"  Published: {book.publication_date} | ISBN: {book.isbn}")

    def search_books(self, search_criteria, search_value):
        """
        Search books by name, author, or publication date.
        :param search_criteria: The field to search (e.g., 'name', 'author', 'publication_date').
        :param search_value: The value to search for.
        """
        if search_criteria.lower() == "name":
            filtered_books = [book for book in self.books_list if search_value.lower() in book.title.lower()]
        elif search_criteria.lower() == "author":
            filtered_books = [book for book in self.books_list if search_value.lower() in book.author.lower()]
        elif search_criteria.lower() == "publication_date":
            filtered_books = [book for book in self.books_list if search_value in book.publication_date]
        else:
            print(f"Invalid search criteria: {search_criteria}. Please use 'name', 'author', or 'publication_date'.")
            return

        if not filtered_books:
            print(f"No books found for {search_criteria} matching '{search_value}'.")
        else:
            print(f"\n=== Search Results for {search_criteria}: {search_value} ===")
            for book in filtered_books:
                print(f"- {book.title} by {book.author} (Category: {book.category})")
                print(f"  Published: {book.publication_date} | ISBN: {book.isbn} | Price: ${book.price}")
