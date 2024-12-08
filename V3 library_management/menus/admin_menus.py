# Admin menu options
# Admin menu options

from menus.book_menus import manage_books
from menus.author_menus import manage_authors
from menus.category_menus import manage_categories
from menus.membership_menus import manage_memberships
from services.user_service import UserService
from utils.helpers import print_separator


def admin_dashboard(user_service: UserService, book_service, author_service, category_service, membership_service):
    """
    Admin dashboard for managing the library system.
    """
    while True:
        print_separator()
        print("\n=== Admin Dashboard ===")
        print("1. Manage Users")
        print("2. Manage Books")
        print("3. Manage Authors")
        print("4. Manage Categories")
        print("5. Manage Memberships")
        print("0. Logout")
        print_separator()
        choice = input("Enter your choice: ")

        if choice == "1":
            manage_users(user_service)
        elif choice == "2":
            manage_books(book_service, author_service, category_service)
        elif choice == "3":
            manage_authors(author_service)
        elif choice == "4":
            manage_categories(category_service)
        elif choice == "5":
            manage_memberships(membership_service)
        elif choice == "0":
            print("Logging out from Admin Dashboard...")
            break
        else:
            print("Invalid choice! Please try again.")


def manage_users(user_service: UserService):
    """
    Menu for managing users.
    """
    while True:
        print_separator()
        print("\n=== Manage Users ===")
        print("1. List All Users")
        print("2. Add New User")
        print("3. Delete User")
        print("0. Go Back")
        print_separator()
        choice = input("Enter your choice: ")

        if choice == "1":
            users = user_service.list_users()
            if users:
                print("\n=== Users ===")
                for user in users:
                    print(f"ID: {user['id']}, Name: {user['first_name']} {user['last_name']}, Role: {user['role']}")
            else:
                print("No users found.")
        elif choice == "2":
            first_name = input("Enter First Name: ").strip()
            last_name = input("Enter Last Name: ").strip()
            email = input("Enter Email: ").strip()
            password = input("Enter Password: ").strip()
            role = input("Enter Role (admin/user): ").strip()
            try:
                user_id = user_service.create_user(first_name, last_name, email, password, role)
                print(f"User added successfully with ID: {user_id}.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == "3":
            user_id = input("Enter User ID to delete: ").strip()
            try:
                if user_service.delete_user(int(user_id)):
                    print("User deleted successfully.")
                else:
                    print("Failed to delete user.")
            except ValueError:
                print("Invalid User ID.")
        elif choice == "0":
            print("Returning to Admin Dashboard...")
            break
        else:
            print("Invalid choice! Please try again.")
