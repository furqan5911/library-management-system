# Main entry point for the Library Management System
# Main entry point for the Library Management System

from config.database import DatabaseConnectionManager
from menus.menus import main_menu
from services.user_service import UserService
from services.membership_service import MembershipService
from services.user_membership_service import UserMembershipService
from services.author_service import AuthorService
from services.category_service import CategoryService
from services.book_service import BookService
from services.transaction_service import TransactionService
from utils.constants import DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_PASSWORD
from utils.helpers import print_separator


def initialize_default_admin(user_service):
    """
    Ensures that a default admin user exists in the database.
    """
    admin = user_service.user_repository.find_by_email(DEFAULT_ADMIN_EMAIL)
    if not admin:
        user_service.create_user(
            first_name="Default",
            last_name="Admin",
            email=DEFAULT_ADMIN_EMAIL,
            password=DEFAULT_ADMIN_PASSWORD,
            role="admin"
        )
        print(f"Default admin created with email: {DEFAULT_ADMIN_EMAIL}")
    else:
        print(f"Default admin already exists: {DEFAULT_ADMIN_EMAIL}")


def main():
    """
    Entry point for the Library Management System.
    """
    print("\n=== Welcome to the Library Management System ===")

    # Initialize Database Connection
    db_manager = DatabaseConnectionManager()

    try:
        db_client = db_manager.get_client()

        # Initialize Services
        user_service = UserService(db_client)
        membership_service = MembershipService(db_client)
        user_membership_service = UserMembershipService(db_client)
        author_service = AuthorService(db_client)
        category_service = CategoryService(db_client)
        book_service = BookService(
            db_client,
            author_repository=author_service.author_repo,
            category_repository=category_service.category_repo
        )
        transaction_service = TransactionService(db_client)

        # Ensure Tables
        print_separator()
        print("Ensuring database tables exist...")
        user_service.user_repository.create_table(user_service.user_repository.get_user_schema())
        membership_service.membership_repo.create_table(membership_service.membership_repo.get_membership_schema())
        user_membership_service.user_membership_repo.create_table(user_membership_service.user_membership_repo.get_user_membership_schema())
        author_service.author_repo.create_table(author_service.author_repo.get_author_schema())
        category_service.category_repo.create_table(category_service.category_repo.get_category_schema())
        book_service.book_repo.create_table(book_service.book_repo.get_book_schema())
        transaction_service.transaction_repo.create_table(transaction_service.transaction_repo.get_transaction_schema())
        print("All tables ensured.")
        print_separator()

        # Ensure Default Admin Exists
        print("Initializing default admin...")
        initialize_default_admin(user_service)
        print_separator()

        # Launch Main Menu
        main_menu(
            user_service=user_service,
            book_service=book_service,
            author_service=author_service,
            category_service=category_service,
            membership_service=membership_service,
            transaction_service=transaction_service,
            user_membership_service=user_membership_service
        )

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db_manager.close()
        print("Database connection closed.")


if __name__ == "__main__":
    main()
