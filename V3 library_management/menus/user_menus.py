# User menu options
# User menu options

from services.book_service import BookService
from services.transaction_service import TransactionService
from services.user_membership_service import UserMembershipService
from utils.helpers import print_separator


def user_dashboard(user, book_service: BookService, transaction_service: TransactionService,
                   user_membership_service: UserMembershipService):
    """
    User dashboard for accessing library features.
    """
    while True:
        print_separator()
        print("\n=== User Dashboard ===")
        print("1. View Books")
        print("2. Search Books")
        print("3. Purchase a Book")
        print("4. View Membership Details")
        print("5. View Transaction History")
        print("0. Logout")
        print_separator()
        choice = input("Enter your choice: ")

        if choice == "1":
            view_books(book_service)
        elif choice == "2":
            search_books(book_service)
        elif choice == "3":
            purchase_book(user, book_service, transaction_service, user_membership_service)
        elif choice == "4":
            view_membership_details(user, user_membership_service)
        elif choice == "5":
            view_transaction_history(user, transaction_service)
        elif choice == "0":
            print("Logging out from User Dashboard...")
            break
        else:
            print("Invalid choice! Please try again.")


def view_books(book_service: BookService):
    """
    Display all available books.
    """
    books = book_service.list_books()
    if books:
        print("\n=== Available Books ===")
        for book in books:
            print(f"ID: {book['id']}, Title: {book['title']}, Price: ${book['price']}, Status: {'Sold' if book['is_sold'] else 'Available'}")
    else:
        print("No books available.")


def search_books(book_service: BookService):
    """
    Search for books based on criteria.
    """
    print("\n=== Search Books ===")
    print("1. By Title")
    print("2. By Author")
    print("3. By Category")
    choice = input("Enter your choice: ").strip()

    if choice == "1":
        title = input("Enter Title: ").strip()
        results = book_service.search_books("title", title)
    elif choice == "2":
        author_name = input("Enter Author Name: ").strip()
        results = book_service.search_books("author", author_name)
    elif choice == "3":
        category_name = input("Enter Category Name: ").strip()
        results = book_service.search_books("category", category_name)
    else:
        print("Invalid choice!")
        return

    if results:
        print("\n=== Search Results ===")
        for book in results:
            print(f"ID: {book['id']}, Title: {book['title']}, Price: ${book['price']}")
    else:
        print("No books found matching your criteria.")


def purchase_book(user, book_service: BookService, transaction_service: TransactionService,
                  user_membership_service: UserMembershipService):
    """
    Allow the user to purchase a book if conditions are met.
    """
    book_id = input("Enter Book ID to purchase: ").strip()
    try:
        book_id = int(book_id)
    except ValueError:
        print("Invalid Book ID.")
        return

    # Fetch user's membership details
    membership = user_membership_service.get_user_membership(user["id"])
    if not membership:
        print("You need an active membership to purchase books.")
        return

    # Fetch the book details
    book = book_service.search_books("id", book_id)
    if not book or book[0]["is_sold"]:
        print("Book is either not available or already sold.")
        return

    book_price = book[0]["price"]
    remaining_balance = membership["remaining_balance"]

    # Check balance
    if remaining_balance < book_price:
        print("Insufficient balance in your membership. Please upgrade your plan.")
        return

    # Process the purchase
    transaction = transaction_service.record_transaction(user["id"], book_id, book_price)
    if transaction:
        print(f"Book purchased successfully! Transaction ID: {transaction['id']}")
    else:
        print("Failed to process the purchase.")


def view_membership_details(user, user_membership_service: UserMembershipService):
    """
    Display the user's membership details.
    """
    membership = user_membership_service.get_user_membership(user["id"])
    if membership:
        print("\n=== Membership Details ===")
        print(f"Plan Name: {membership['membership_id']}")
        print(f"Remaining Balance: ${membership['remaining_balance']}")
        print(f"Joined Date: {membership['joined_date']}")
    else:
        print("You do not have an active membership.")


def view_transaction_history(user, transaction_service: TransactionService):
    """
    Display the user's transaction history.
    """
    transactions = transaction_service.list_transactions_for_user(user["id"])
    if transactions:
        print("\n=== Transaction History ===")
        for tx in transactions:
            print(f"Transaction ID: {tx['id']}, Book ID: {tx['book_id']}, Price: ${tx['price']}, Date: {tx['transaction_date']}")
    else:
        print("You have no transaction history.")
