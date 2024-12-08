# Author menu options

from services.author_service import AuthorService
from utils.helpers import print_separator


def manage_authors(author_service: AuthorService):
    """
    Menu for managing authors.
    """
    while True:
        print_separator()
        print("\n=== Manage Authors ===")
        print("1. List All Authors")
        print("2. Delete Author")
        print("0. Go Back")
        print_separator()
        choice = input("Enter your choice: ")

        if choice == "1":
            list_authors(author_service)
        elif choice == "2":
            delete_author(author_service)
        elif choice == "0":
            print("Returning to Admin Dashboard...")
            break
        else:
            print("Invalid choice! Please try again.")


def list_authors(author_service: AuthorService):
    """
    Lists all authors in the system.
    """
    authors = author_service.list_authors()
    if authors:
        print("\n=== All Authors ===")
        for author in authors:
            print(f"ID: {author['id']}, Name: {author['first_name']} {author['last_name']}")
    else:
        print("No authors found.")


def delete_author(author_service: AuthorService):
    """
    Deletes an author by their ID.
    """
    author_id = input("Enter Author ID to delete: ").strip()
    try:
        author_id = int(author_id)
        if author_service.delete_author(author_id):
            print("Author deleted successfully.")
        else:
            print("Failed to delete author.")
    except ValueError:
        print("Invalid Author ID.")
