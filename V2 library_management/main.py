from services.user_service import UserService
from services.book_service import BookService
from services.author_service import AuthorService
from services.category_service import CategoryService
from services.membership_service import MembershipService
from services.transaction_service import TransactionService
from utils.menus import handle_admin_menu, handle_user_menu
import os


def initial_menu():
    """
    Display the initial menu for logging in or signing up.
    """
    print("\n=== Welcome to the Library Management System ===")
    print("1. Login as Admin")
    print("2. Login as User")
    print("3. Sign Up as User")
    print("0. Exit")
    return input("Enter your choice: ")


def ensure_data_files_exist():
    """
    Ensures that the `data/` directory and required JSON files exist.
    Creates them if they do not exist.
    """
    os.makedirs("data", exist_ok=True)

    files = [
        "data/users.json", "data/books.json", "data/authors.json",
        "data/categories.json", "data/memberships.json",
        "data/transactions.json", "data/user_memberships.json"
    ]

    for file in files:
        if not os.path.exists(file):
            with open(file, "w") as f:
                f.write("[]")


def main():
    ensure_data_files_exist()
    user_service = UserService("data/users.json")
    book_service = BookService("data/books.json")
    author_service = AuthorService("data/authors.json")
    category_service = CategoryService("data/categories.json")
    membership_service = MembershipService("data/memberships.json", "data/user_memberships.json")
    transaction_service = TransactionService("data/transactions.json", "data/user_memberships.json")

    while True:
        choice = initial_menu()
        if choice == "1":  # Admin Login
            email = input("Enter Admin Email: ")
            password = input("Enter Admin Password: ")
            admin = user_service.login(email, password)
            if admin and admin.is_admin():
                handle_admin_menu(admin, user_service, book_service, author_service, category_service, membership_service)
        elif choice == "2":  # User Login
            email = input("Enter User Email: ")
            password = input("Enter User Password: ")
            user = user_service.login(email, password)
            if user and not user.is_admin():
                handle_user_menu(user, book_service, membership_service, transaction_service)
        elif choice == "3":  # User Sign-Up
            first_name = input("Enter First Name: ")
            last_name = input("Enter Last Name: ")
            email = input("Enter Email: ")
            password = input("Enter Password: ")
            user_service.sign_up({
                "first_name": first_name, "last_name": last_name,
                "email": email, "password": password, "role": "user"
            })
            print("Sign-Up successful! You can now log in.")
        elif choice == "0":  # Exit
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

