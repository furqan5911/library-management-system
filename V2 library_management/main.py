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





# from services.user_service import UserService
# from services.book_service import BookService
# from services.author_service import AuthorService
# from services.category_service import CategoryService
# from services.membership_service import MembershipService
# from services.transaction_service import TransactionService
# import os


# def initial_menu():
#     """
#     Display the initial menu for logging in or signing up.
#     """
#     print("\n=== Welcome to the Library Management System ===")
#     print("1. Login as Admin")
#     print("2. Login as User")
#     print("3. Sign Up as User")
#     print("0. Exit")
#     choice = input("Enter your choice: ")
#     return choice


# def admin_dashboard(admin, user_service, book_service, author_service, category_service, membership_service):
#     """
#     Display the admin dashboard with admin functionalities.
#     """
#     while True:
#         print("\n=== Admin Dashboard ===")
#         print("1. Manage Books")
#         print("2. Manage Authors")
#         print("3. Manage Categories")
#         print("4. Manage Membership Plans")
#         print("5. Logout")
#         choice = input("Enter your choice: ")

#         if choice == "1":
#             book_menu(admin, book_service)
#         elif choice == "2":
#             author_menu(admin, author_service)
#         elif choice == "3":
#             category_menu(admin, category_service)
#         elif choice == "4":
#             membership_menu(admin, membership_service)
#         elif choice == "5":
#             print("Logging out...")
#             break
#         else:
#             print("Invalid choice. Please try again.")


# def user_dashboard(user, book_service, membership_service, transaction_service):
#     """
#     Display the user dashboard with user functionalities.
#     """
#     while True:
#         print("\n=== User Dashboard ===")
#         print("1. View Books")
#         print("2. Search Books")
#         print("3. Filter Books by Category")
#         print("4. View Membership Plans")
#         print("5. Purchase Membership Plan")
#         print("6. Upgrade Membership Plan")
#         print("7. View Transactions")
#         print("8. Purchase Book")
#         print("9. Logout")
#         choice = input("Enter your choice: ")

#         if choice == "1":
#             books = book_service.list_books()
#             print("\n=== Available Books ===")
#             for book in books:
#                 print(f"- {book.title} by {book.author} (${book.price})")
#         elif choice == "2":
#             search_key = input("Search by (title/author/publication_date): ").strip()
#             search_value = input("Enter the search value: ").strip()
#             try:
#                 results = book_service.search_books(search_key, search_value)
#                 print("\n=== Search Results ===")
#                 for book in results:
#                     print(f"- {book.title} by {book.author} (${book.price})")
#             except ValueError as e:
#                 print(e)
#         elif choice == "3":
#             category = input("Enter category name: ").strip()
#             results = book_service.list_books_by_category(category)
#             print("\n=== Books in Category ===")
#             for book in results:
#                 print(f"- {book.title} by {book.author} (${book.price})")
#         elif choice == "4":
#             plans = membership_service.list_plans()
#             print("\n=== Membership Plans ===")
#             for plan in plans:
#                 print(f"- {plan.plan_name}: ${plan.plan_price}")
#         elif choice == "5":
#             plan_id = int(input("Enter the plan ID to purchase: "))
#             try:
#                 membership_service.purchase_plan(user.id, plan_id)
#                 print("Membership plan purchased successfully!")
#             except ValueError as e:
#                 print(e)
#         elif choice == "6":
#             new_plan_id = int(input("Enter the new plan ID to upgrade: "))
#             try:
#                 membership_service.upgrade_plan(user.id, new_plan_id, "data/books.json")
#                 print("Membership plan upgraded successfully!")
#             except ValueError as e:
#                 print(e)
#         elif choice == "7":
#             transactions = transaction_service.list_user_transactions(user.email)
#             print("\n=== Your Transactions ===")
#             for tx in transactions:
#                 print(f"- Book ID: {tx.book_id}, Price: ${tx.price}, Date: {tx.transaction_date}")
#         elif choice == "8":  # Purchase a Book
#             book_id = int(input("Enter the ID of the book you want to purchase: "))
#             try:
#                 book = book_service.find_book_by_id(book_id)
#                 if not book:
#                     print("Book not found.")
#                     continue

#                 membership_service.deduct_balance(user.id, book["price"])
#                 transaction_service.record_transaction(user.email, book_id, book["price"])
#                 book_service.mark_as_sold(book_id)

#                 print(f"Book '{book['title']}' purchased successfully!")
#             except ValueError as e:
#                 print(e)
#         elif choice == "9":
#             print("Logging out...")
#             break
#         else:
#             print("Invalid choice. Please try again.")


# def book_menu(admin, book_service):
#     """
#     Menu for managing books (Admin only).
#     """
#     while True:  # Added a loop to handle repeated interactions until "Go Back" is selected
#         print("\n=== Manage Books ===")
#         print("1. Add Book")
#         print("2. Update Book")
#         print("3. Delete Book")
#         print("4. View All Books")
#         print("0. Go Back")
#         choice = input("Enter your choice: ")

#         if choice == "1":
#             title = input("Enter book title: ")
#             author = input("Enter book author: ")
#             category = input("Enter book category: ")
#             publication_date = input("Enter publication date (YYYY-MM-DD): ")
#             price = float(input("Enter book price: "))
#             isbn = input("Enter book ISBN: ")
#             book_service.add_book(admin, {
#                 "title": title, "author": author, "category": category,
#                 "publication_date": publication_date, "price": price, "isbn": isbn
#             })
#             print("Book added successfully!")
#         elif choice == "2":
#             book_id = int(input("Enter book ID to update: "))
#             updated_data = {}
#             print("Leave fields blank to skip.")
#             title = input("New title: ")
#             if title:
#                 updated_data["title"] = title
#             book_service.update_book(admin, book_id, updated_data)
#             print("Book updated successfully!")
#         elif choice == "3":
#             book_id = int(input("Enter book ID to delete: "))
#             book_service.delete_book(admin, book_id)
#             print("Book deleted successfully!")
#         elif choice == "4":
#             books = book_service.list_books()
#             print("\n=== Books ===")
#             for book in books:
#                 print(f"- {book.title} by {book.author} (${book.price})")
#         elif choice == "0":
#             print("Returning to Admin Dashboard...")
#             return  # This exits the function and returns to the admin dashboard
#         else:
#             print("Invalid choice! Please try again.")

# def author_menu(admin, author_service):
#     """
#     Menu for managing authors (Admin only).
#     """
#     while True:  # Added a loop for repeated interaction
#         print("\n=== Manage Authors ===")
#         print("1. Add Author")
#         print("2. Update Author")
#         print("3. Delete Author")
#         print("4. Assign Book to Author")
#         print("5. List All Authors")
#         print("0. Go Back")  # Added "Go Back" option
#         choice = input("Enter your choice: ")

#         if choice == "1":
#             first_name = input("Enter author's first name: ")
#             last_name = input("Enter author's last name: ")
#             email = input("Enter author's email: ")
#             author_service.add_author(admin, {"first_name": first_name, "last_name": last_name, "email": email})
#             print("Author added successfully!")
#         elif choice == "2":
#             author_id = int(input("Enter author ID to update: "))
#             updated_data = {}
#             print("Leave fields blank to skip.")
#             first_name = input("New first name: ")
#             if first_name:
#                 updated_data["first_name"] = first_name
#             author_service.update_author(admin, author_id, updated_data)
#             print("Author updated successfully!")
#         elif choice == "3":
#             author_id = int(input("Enter author ID to delete: "))
#             author_service.delete_author(admin, author_id)
#             print("Author deleted successfully!")
#         elif choice == "4":
#             author_id = int(input("Enter author ID: "))
#             book_id = int(input("Enter book ID to assign: "))
#             author_service.assign_book_to_author(admin, author_id, book_id)
#             print("Book assigned to author successfully!")
#         elif choice == "5":
#             authors = author_service.list_authors()
#             print("\n=== Authors ===")
#             for author in authors:
#                 print(f"- {author.first_name} {author.last_name} (Email: {author.email})")
#         elif choice == "0":
#             print("Returning to Admin Dashboard...")
#             return  # Exits the function
#         else:
#             print("Invalid choice!")


# def category_menu(admin, category_service):
#     """
#     Menu for managing categories (Admin only).
#     """
#     while True:  # Added a loop for repeated interaction
#         print("\n=== Manage Categories ===")
#         print("1. Add Category")
#         print("2. Update Category")
#         print("3. Delete Category")
#         print("4. List All Categories")
#         print("0. Go Back")  # Added "Go Back" option
#         choice = input("Enter your choice: ")

#         if choice == "1":
#             name = input("Enter category name: ")
#             category_service.add_category(admin, {"name": name})
#             print("Category added successfully!")
#         elif choice == "2":
#             category_id = int(input("Enter category ID to update: "))
#             new_name = input("Enter new category name: ")
#             category_service.update_category(admin, category_id, new_name)
#             print("Category updated successfully!")
#         elif choice == "3":
#             category_id = int(input("Enter category ID to delete: "))
#             category_service.delete_category(admin, category_id)
#             print("Category deleted successfully!")
#         elif choice == "4":
#             categories = category_service.list_categories()
#             print("\n=== Categories ===")
#             for category in categories:
#                 print(f"- {category.name}")
#         elif choice == "0":
#             print("Returning to Admin Dashboard...")
#             return  # Exits the function
#         else:
#             print("Invalid choice!")

# def membership_menu(admin, membership_service):
#     """
#     Menu for managing memberships (Admin only).
#     """
#     while True:  # Added a loop for repeated interaction
#         print("\n=== Manage Membership Plans ===")
#         print("1. Add Membership Plan")
#         print("2. Update Membership Plan")
#         print("3. Delete Membership Plan")
#         print("4. List All Membership Plans")
#         print("0. Go Back")  # Added "Go Back" option
#         choice = input("Enter your choice: ")

#         if choice == "1":
#             plan_name = input("Enter plan name: ")
#             plan_price = float(input("Enter plan price: "))
#             membership_service.add_plan(admin, {"plan_name": plan_name, "plan_price": plan_price})
#             print("Membership plan added successfully!")
#         elif choice == "2":
#             plan_id = int(input("Enter plan ID to update: "))
#             new_price = float(input("Enter new plan price: "))
#             membership_service.update_plan(admin, plan_id, {"plan_price": new_price})
#             print("Membership plan updated successfully!")
#         elif choice == "3":
#             plan_id = int(input("Enter plan ID to delete: "))
#             membership_service.delete_plan(admin, plan_id)
#             print("Membership plan deleted successfully!")
#         elif choice == "4":
#             plans = membership_service.list_plans()
#             print("\n=== Membership Plans ===")
#             for plan in plans:
#                 print(f"- {plan.plan_name}: ${plan.plan_price}")
#         elif choice == "0":
#             print("Returning to Admin Dashboard...")
#             return  # Exits the function
#         else:
#             print("Invalid choice!")



# def ensure_data_files_exist():
#     """
#     Ensures that the `data/` directory and required JSON files exist.
#     Creates them if they do not exist.
#     """
#     os.makedirs("data", exist_ok=True)

#     # Define the required files
#     files = ["data/users.json", "data/books.json", "data/authors.json", 
#              "data/categories.json", "data/memberships.json", "data/transactions.json","data/user_memberships.json"]

#     # Create empty files if they do not exist
#     for file in files:
#         if not os.path.exists(file):
#             with open(file, "w") as f:
#                 f.write("[]")  # Initialize with an empty list


# def main():
#     ensure_data_files_exist()
#     user_service = UserService("data/users.json")
#     book_service = BookService("data/books.json")
#     author_service = AuthorService("data/authors.json")
#     category_service = CategoryService("data/categories.json")
#     membership_service = MembershipService("data/memberships.json","data/user_memberships.json")
#     transaction_service = TransactionService("data/transactions.json","data/user_memberships.json")

#     while True:
#         choice = initial_menu()
#         if choice == "1":  # Admin Login
#             email = input("Enter Admin Email: ")
#             password = input("Enter Admin Password: ")
#             admin = user_service.login(email, password)
#             if admin and admin.is_admin():
#                 admin_dashboard(admin, user_service, book_service, author_service, category_service, membership_service)
#         elif choice == "2":  # User Login
#             email = input("Enter User Email: ")
#             password = input("Enter User Password: ")
#             user = user_service.login(email, password)
#             if user and not user.is_admin():
#                 user_dashboard(user, book_service, membership_service, transaction_service)
#         elif choice == "3":  # User Sign-Up
#             first_name = input("Enter First Name: ")
#             last_name = input("Enter Last Name: ")
#             email = input("Enter Email: ")
#             password = input("Enter Password: ")
#             user_service.sign_up({
#                 "first_name": first_name, "last_name": last_name,
#                 "email": email, "password": password, "role": "user"
#             })
#             print("Sign-Up successful! You can now log in.")
#         elif choice == "0":  # Exit
#             print("Exiting... Goodbye!")
#             break
#         else:
#             print("Invalid choice. Please try again.")


# if __name__ == "__main__":
#     main()
