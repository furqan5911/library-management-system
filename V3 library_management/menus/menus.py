# Shared menu functionalities
# Shared menu functionalities

from menus.admin_menus import admin_dashboard
from menus.user_menus import user_dashboard
from services.user_service import UserService
from services.book_service import BookService
from services.author_service import AuthorService
from services.category_service import CategoryService
from services.membership_service import MembershipService
from services.transaction_service import TransactionService
from services.user_membership_service import UserMembershipService
from utils.helpers import print_separator


def main_menu(user_service: UserService, book_service: BookService, author_service: AuthorService,
              category_service: CategoryService, membership_service: MembershipService,
              transaction_service: TransactionService, user_membership_service: UserMembershipService):
    """
    Main menu for login and role-based redirection.
    """
    while True:
        print_separator()
        print("\n=== Library Management System ===")
        print("1. Login as Admin")
        print("2. Login as User")
        print("3. Sign-Up as User")
        print("4. Exit")
        print_separator()
        choice = input("Enter your choice: ")

        if choice == "1":
            handle_admin_login(user_service, book_service, author_service, category_service, membership_service)
        elif choice == "2":
            handle_user_login(user_service, book_service, transaction_service, user_membership_service, membership_service)
        elif choice == "3":
            handle_user_sign_up(user_service)
        elif choice == "4":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


def handle_admin_login(user_service: UserService, book_service: BookService, author_service: AuthorService,
                       category_service: CategoryService, membership_service: MembershipService):
    """
    Handles admin login and redirects to the admin dashboard.
    """
    print_separator()
    email = input("Enter Admin Email: ").strip()
    password = input("Enter Admin Password: ").strip()
    try:
        user = user_service.authenticate_user(email, password)
        if user.role == "admin":
            print(f"Welcome, Admin: {user.first_name} {user.last_name}")
            admin_dashboard(user_service, book_service, author_service, category_service, membership_service)
        else:
            print("Access denied. This account is not an admin.")
    except ValueError as e:
        print(f"Error during admin login: {e}")


def handle_user_login(user_service: UserService, book_service: BookService, transaction_service: TransactionService,
                      user_membership_service: UserMembershipService, membership_service: MembershipService):
    """
    Handles user login and redirects to the user dashboard.
    """
    print_separator()
    email = input("Enter User Email: ").strip()
    password = input("Enter User Password: ").strip()
    try:
        user = user_service.authenticate_user(email, password)
        if user.role == "user":
            print(f"Welcome, {user.first_name} {user.last_name}")
            user_dashboard(user.to_dict(), book_service, transaction_service, user_membership_service, membership_service)
        else:
            print("Access denied. This account is not a user.")
    except ValueError as e:
        print(f"Error during user login: {e}")



def handle_user_sign_up(user_service: UserService):
    """
    Handles user sign-up by collecting user details.
    """
    print("\n=== User Sign-Up ===")
    try:
        first_name = input("Enter First Name: ").strip()
        last_name = input("Enter Last Name: ").strip()
        email = input("Enter Email: ").strip()
        password = input("Enter Password: ").strip()

        # Perform sign-up
        result = user_service.sign_up_user(first_name, last_name, email, password)

        # Check the result and provide feedback
        if result.startswith("User created successfully"):
            print(result)
        else:
            print(f"Sign-Up Error: {result}")

    except ValueError as ve:
        print(f"Validation Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred during sign-up: {e}")
