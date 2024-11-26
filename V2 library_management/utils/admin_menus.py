from utils.book_menus import book_menu
from utils.author_menus import author_menu
from utils.category_menus import category_menu
from utils.membership_menus import membership_menu


def admin_dashboard(admin, user_service, book_service, author_service, category_service, membership_service):
    """
    Display the admin dashboard with admin functionalities.
    """
    while True:
        print("\n=== Admin Dashboard ===")
        print("1. Manage Books")
        print("2. Manage Authors")
        print("3. Manage Categories")
        print("4. Manage Membership Plans")
        print("5. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            book_menu(admin, book_service)
        elif choice == "2":
            author_menu(admin, author_service)
        elif choice == "3":
            category_menu(admin, category_service)
        elif choice == "4":
            membership_menu(admin, membership_service)
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")
