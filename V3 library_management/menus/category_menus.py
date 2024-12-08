# Category menu options

from services.category_service import CategoryService
from utils.helpers import print_separator


def manage_categories(category_service: CategoryService):
    """
    Menu for managing categories.
    """
    while True:
        print_separator()
        print("\n=== Manage Categories ===")
        print("1. List All Categories")
        print("2. Delete Category")
        print("0. Go Back")
        print_separator()
        choice = input("Enter your choice: ")

        if choice == "1":
            list_categories(category_service)
        elif choice == "2":
            delete_category(category_service)
        elif choice == "0":
            print("Returning to Admin Dashboard...")
            break
        else:
            print("Invalid choice! Please try again.")


def list_categories(category_service: CategoryService):
    """
    Lists all categories in the system.
    """
    categories = category_service.list_categories()
    if categories:
        print("\n=== All Categories ===")
        for category in categories:
            print(f"ID: {category['id']}, Name: {category['name']}")
    else:
        print("No categories found.")


def delete_category(category_service: CategoryService):
    """
    Deletes a category by its ID.
    """
    category_id = input("Enter Category ID to delete: ").strip()
    try:
        category_id = int(category_id)
        if category_service.delete_category(category_id):
            print("Category deleted successfully.")
        else:
            print("Failed to delete category.")
    except ValueError:
        print("Invalid Category ID.")
