# Book menu options

from services.book_service import BookService
from services.author_service import AuthorService
from services.category_service import CategoryService
from utils.helpers import print_separator


def manage_books(book_service: BookService, author_service: AuthorService, category_service: CategoryService):
    """
    Menu for managing books.
    """
    while True:
        print_separator()
        print("\n=== Manage Books ===")
        print("1. Add Book")
        print("2. List All Books")
        print("3. Delete Book")
        print("0. Go Back")
        print_separator()
        choice = input("Enter your choice: ")

        if choice == "1":
            add_book(book_service, author_service, category_service)
        elif choice == "2":
            list_books(book_service)
        elif choice == "3":
            delete_book(book_service)
        elif choice == "0":
            print("Returning to Admin Dashboard...")
            break
        else:
            print("Invalid choice! Please try again.")


def add_book(book_service: BookService, author_service: AuthorService, category_service: CategoryService):
    """
    Adds a new book with associated author and category.
    """
    title = input("Enter Book Title: ").strip()
    author_name = input("Enter Author Name: ").strip()
    category_name = input("Enter Category Name: ").strip()
    price = float(input("Enter Price: ").strip())
    publication_date = input("Enter Publication Date (YYYY-MM-DD): ").strip()
    isbn = input("Enter ISBN: ").strip()

    book_data = {
        "title": title,
        "author_first_name": author_name.split()[0],
        "author_last_name": " ".join(author_name.split()[1:]) if len(author_name.split()) > 1 else "",
        "category": category_name,
        "price": price,
        "publication_date": publication_date,
        "isbn": isbn,
    }
    book = book_service.add_book(book_data)
    if book:
        print(f"Book '{title}' added successfully.")
    else:
        print("Failed to add book.")


def list_books(book_service: BookService):
    """
    Lists all books in the system.
    """
    books = book_service.list_books()
    if books:
        print("\n=== All Books ===")
        for book in books:
            print(f"ID: {book['id']}, Title: {book['title']}, Price: ${book['price']}, Status: {'Sold' if book['is_sold'] else 'Available'}")
    else:
        print("No books found.")


def delete_book(book_service: BookService):
    """
    Deletes a book by its ID.
    """
    book_id = input("Enter Book ID to delete: ").strip()
    try:
        book_id = int(book_id)
        if book_service.delete_book(book_id):
            print("Book deleted successfully.")
        else:
            print("Failed to delete book.")
    except ValueError:
        print("Invalid Book ID.")
