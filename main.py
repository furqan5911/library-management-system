from managers.user_manager import UserManager
from managers.author_manager import AuthorManager
from managers.membership_manager import MembershipManager
from managers.book_manager import BookManager
from managers.category_manager import CategoryManager
from managers.transaction_manager import BooksTransactionManager


def initial_menu():
    """Display the initial menu for selecting the role."""
    while True:
        print("\n=== Welcome to the Library Management System ===")
        print("1. Login as Admin")
        print("2. Login as User")
        print("3. Sign Up as Admin")
        print("4. Sign Up as User")
        # Option to exit the system
        print("0. Exit")
        choice = input("Enter your choice: ")
        if choice in ["1", "2", "3", "4", "0"]:
            return choice
        else:
            print("Invalid choice. Please try again.")


def admin_dashboard(current_user, author_manager, membership_manager, book_manager, category_manager):
    """Admin-specific dashboard."""
    while True:
        print("\n=== Admin Dashboard ===")
        print("1. Manage Authors")
        print("2. Manage Membership Plans")
        print("3. Manage Books")
        print("4. Manage Categories")
        print("0. Logout")
        choice = input("Enter your choice: ")
        if choice == "1":
            author_menu(current_user, author_manager)
        elif choice == "2":
            membership_menu(current_user, membership_manager)
        elif choice == "3":
            book_menu(current_user, book_manager)
        elif choice == "4":
            category_menu(current_user, category_manager)
        elif choice == "0":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")


def user_dashboard(current_user, book_manager, membership_manager, transaction_manager):
    while True:
        print("\n=== User Dashboard ===")
        print("1. View Books")
        print("2. View Membership Plans")
        print("3. Purchase Membership Plan")
        print("4. Upgrade Membership Plan")  # New option for upgrading
        print("5. View Transaction History")
        print("6. Make a Transaction (Purchase Book)")
        print("0. Logout")
        choice = input("Enter your choice: ")
        if choice == "1":
            book_manager.list_books()
        elif choice == "2":
            membership_manager.list_plans()
        elif choice == "3":
            membership_manager.list_plans()
            plan_name = input("Enter the name of the membership plan you want to purchase: ")
            membership_manager.purchase_plan(current_user, plan_name)
        elif choice == "4":  # New upgrade functionality
            membership_manager.list_plans()
            new_plan_name = input("Enter the name of the plan you want to upgrade to: ")
            membership_manager.upgrade_plan(current_user, new_plan_name)
        elif choice == "5":
            transaction_manager.list_user_transactions(current_user)
        elif choice == "6":
            book_title = input("Enter the title of the book you want to purchase: ")
            transaction_manager.record_transaction(current_user, book_title)
        elif choice == "0":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")


def author_menu(current_user, author_manager):
    """Menu for managing authors."""
    while True:
        print("\n=== Author Management ===")
        print("1. Add Author")
        print("2. Assign Book to Author")
        print("3. Update Author")
        print("4. Remove Author")
        print("5. List Authors")
        print("0. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            first_name = input("Enter Author's First Name: ")
            last_name = input("Enter Author's Last Name: ")
            email = input("Enter Author's Email: ")
            author_manager.add_author(current_user, first_name, last_name, email)
        elif choice == "2":
            email = input("Enter Author's Email to Assign a Book: ")
            book_title = input("Enter the Book Title: ")
            author_manager.assign_book_to_author(current_user, email, book_title)
        elif choice == "3":
            email = input("Enter Author's Email to Update: ")
            updated_data = {}
            print("Enter new details (leave blank to skip):")
            first_name = input("New First Name: ")
            if first_name:
                updated_data["first_name"] = first_name
            last_name = input("New Last Name: ")
            if last_name:
                updated_data["last_name"] = last_name
            author_manager.update_author(current_user, email, updated_data)
        elif choice == "4":
            email = input("Enter Author's Email to Remove: ")
            author_manager.remove_author(current_user, email)
        elif choice == "5":
            author_manager.list_authors()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def membership_menu(current_user, membership_manager):
    """Menu for managing memberships."""
    while True:
        print("\n=== Membership Management ===")
        print("1. View Membership Plans")
        print("2. Create Membership Plan (Admin Only)")
        print("3. Update Membership Plan (Admin Only)")
        print("4. Delete Membership Plan (Admin Only)")
        print("0. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            membership_manager.list_plans()
        elif choice == "2" and current_user.is_admin():
            plan_name = input("Enter Plan Name: ")
            plan_price = float(input("Enter Plan Price: "))
            membership_manager.create_plan(current_user, plan_name, plan_price)
        elif choice == "3" and current_user.is_admin():
            plan_name = input("Enter Plan Name to Update: ")
            new_price = float(input("Enter New Plan Price: "))
            membership_manager.update_plan(current_user, plan_name, new_price)
        elif choice == "4" and current_user.is_admin():
            plan_name = input("Enter Plan Name to Delete: ")
            membership_manager.delete_plan(current_user, plan_name)
        elif choice == "0":
            break
        else:
            print("Invalid choice or restricted access. Please try again.")


def book_menu(current_user, book_manager):
    """Menu for managing books."""
    while True:
        print("\n=== Book Management ===")
        print("1. Add Book")
        print("2. Update Book")
        print("3. Remove Book")
        print("4. List Books")
        print("0. Back")
        choice = input("Enter your choice: ")
        if choice == "1" and current_user.is_admin():
            title = input("Enter Book Title: ")
            author = input("Enter Author Name: ")
            category = input("Enter Category: ")
            publication_date = input("Enter Publication Date (YYYY-MM-DD): ")
            price = float(input("Enter Price: "))
            isbn = input("Enter ISBN: ")
            book_manager.add_book(current_user, title, author, category, publication_date, price, isbn)
        elif choice == "2" and current_user.is_admin():
            isbn = input("Enter ISBN of Book to Update: ")
            updated_data = {}
            print("Enter new details (leave blank to skip):")
            title = input("New Title: ")
            if title:
                updated_data["title"] = title
            author = input("New Author: ")
            if author:
                updated_data["author"] = author
            category = input("New Category: ")
            if category:
                updated_data["category"] = category
            price = input("New Price: ")
            if price:
                updated_data["price"] = float(price)
            book_manager.update_book(current_user, isbn, updated_data)
        elif choice == "3" and current_user.is_admin():
            isbn = input("Enter ISBN of Book to Remove: ")
            book_manager.remove_book(current_user, isbn)
        elif choice == "4":
            book_manager.list_books()
        elif choice == "0":
            break
        else:
            print("Invalid choice or restricted access. Please try again.")


def category_menu(current_user, category_manager):
    """Menu for managing categories."""
    while True:
        print("\n=== Category Management ===")
        print("1. Add Category (Admin Only)")
        print("2. Update Category (Admin Only)")
        print("3. Remove Category (Admin Only)")
        print("4. List Categories")
        print("0. Back")
        choice = input("Enter your choice: ")
        if choice == "1" and current_user.is_admin():
            name = input("Enter Category Name: ")
            category_manager.add_category(current_user, name)
        elif choice == "2" and current_user.is_admin():
            old_name = input("Enter Existing Category Name: ")
            new_name = input("Enter New Category Name: ")
            category_manager.update_category(current_user, old_name, new_name)
        elif choice == "3" and current_user.is_admin():
            name = input("Enter Category Name to Remove: ")
            category_manager.remove_category(current_user, name)
        elif choice == "4":
            category_manager.list_categories()
        elif choice == "0":
            break
        else:
            print("Invalid choice or restricted access. Please try again.")


def main():
    """
    Main function to run the library management system.
    This function initializes various managers for users, authors, memberships, books, categories, and transactions.
    It loads data from disk for each manager and presents an initial menu to the user with options to login as an admin or user,
    sign up as an admin or user, or exit the system.
    The function handles the following choices:
    1. Login as Admin: Prompts for admin email and password, and if valid, navigates to the admin dashboard.
    2. Login as User: Prompts for user email and password, and if valid, navigates to the user dashboard.
    3. Sign Up as Admin: Prompts for user details and signs up a new admin.
    4. Sign Up as User: Prompts for user details and signs up a new user.
    0. Exit: Exits the system.
    Returns:
        None
    """
    user_manager = UserManager()
    author_manager = AuthorManager()
    membership_manager = MembershipManager()
    book_manager = BookManager()
    category_manager = CategoryManager()
    transaction_manager = BooksTransactionManager()

    # Load data
    user_manager.load_users_from_disk()
    author_manager.load_authors_from_disk()
    membership_manager.load_memberships_from_disk()
    book_manager.load_books_from_disk()
    category_manager.load_categories_from_disk()
    transaction_manager.load_data_from_disk()

    while True:
        choice = initial_menu()
        if choice == "1":  # Login as Admin
            email = input("Enter Admin Email: ")
            password = input("Enter Password: ")
            current_user = user_manager.login_user(email, password)
            if current_user and current_user.is_admin():
                admin_dashboard(current_user, author_manager, membership_manager, book_manager, category_manager)
        elif choice == "2":  # Login as User
            email = input("Enter User Email: ")
            password = input("Enter Password: ")
            current_user = user_manager.login_user(email, password)
            if current_user and not current_user.is_admin():
                user_dashboard(current_user, book_manager, membership_manager, transaction_manager)
        elif choice == "3":  # Sign Up as Admin
            first_name = input("Enter First Name: ")
            last_name = input("Enter Last Name: ")
            email = input("Enter Email: ")
            password = input("Enter Password: ")
            user_manager.signup_user(first_name, last_name, email, password, role="admin")
        elif choice == "4":  # Sign Up as User
            first_name = input("Enter First Name: ")
            last_name = input("Enter Last Name: ")
            email = input("Enter Email: ")
            password = input("Enter Password: ")
            user_manager.signup_user(first_name, last_name, email, password, role="user")
        elif choice == "0":  # Exit
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
