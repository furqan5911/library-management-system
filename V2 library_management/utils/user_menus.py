def user_dashboard(user, book_service, membership_service, transaction_service):
    """
    Display the user dashboard with user functionalities.
    """
    while True:
        print("\n=== User Dashboard ===")
        print("1. View Books")
        print("2. Search Books")
        print("3. Filter Books by Category")
        print("4. View Membership Plans")
        print("5. Purchase Membership Plan")
        print("6. Upgrade Membership Plan")
        print("7. View Transactions")
        print("8. Purchase Book")
        print("9. Logout")
        choice = input("Enter your choice: ")

        try:
            if choice == "1":  # View Books
                books = book_service.list_books()
                if books:
                    print("\n=== Available Books ===")
                    for book in books:
                        print(f"- {book.title} by {book.author} (${book.price})")
                else:
                    print("No books available.")
            elif choice == "2":  # Search Books
                search_key = input("Search by (title/author/publication_date): ").strip()
                search_value = input("Enter the search value: ").strip()
                results = book_service.search_books(search_key, search_value)
                if results:
                    print("\n=== Search Results ===")
                    for book in results:
                        print(f"- {book.title} by {book.author} (${book.price})")
                else:
                    print("No matching books found.")
            elif choice == "3":  # Filter Books by Category
                category = input("Enter category name: ").strip()
                results = book_service.list_books_by_category(category)
                if results:
                    print("\n=== Books in Category ===")
                    for book in results:
                        print(f"- {book.title} by {book.author} (${book.price})")
                else:
                    print(f"No books found in the category '{category}'.")
            elif choice == "4":  # View Membership Plans
                plans = membership_service.list_plans()
                if plans:
                    print("\n=== Membership Plans ===")
                    for plan in plans:
                        print(f"- {plan.plan_name}: ${plan.plan_price}")
                else:
                    print("No membership plans available.")
            elif choice == "5":  # Purchase Membership Plan
                plan_id = int(input("Enter the plan ID to purchase: "))
                membership_service.purchase_plan(user.id,user.email,plan_id)
            elif choice == "6":  # Upgrade Membership Plan
                new_plan_id = int(input("Enter the new plan ID to upgrade: "))
                membership_service.upgrade_plan(user.id, new_plan_id, "data/books.json")
            elif choice == "7":  # View Transactions
                transactions = transaction_service.list_user_transactions(user.email)
                if transactions:
                    print("\n=== Your Transactions ===")
                    for tx in transactions:
                        # Ensure `Transaction` objects are formatted correctly
                        print(f"- Book ID: {tx.book_id}, Price: ${tx.price}, Date: {tx.transaction_date}")
                else:
                    print("No transactions found.")
            elif choice == "8":  # Purchase Book
                book_id = int(input("Enter the ID of the book you want to purchase: "))
                book = book_service.find_by_id(book_id)
                if not book:
                    print(f"Book with ID {book_id} not found.")
                else:
                    transaction_service.record_transaction( user.id,user.email,book_id,book["price"])
            elif choice == "9":  # Logout
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


