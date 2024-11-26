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

        if choice == "1":
            books = book_service.list_books()
            print("\n=== Available Books ===")
            for book in books:
                print(f"- {book.title} by {book.author} (${book.price})")
        elif choice == "2":
            search_key = input("Search by (title/author/publication_date): ").strip()
            search_value = input("Enter the search value: ").strip()
            results = book_service.search_books(search_key, search_value)
            print("\n=== Search Results ===")
            for book in results:
                print(f"- {book.title} by {book.author} (${book.price})")
        elif choice == "3":
            category = input("Enter category name: ").strip()
            results = book_service.list_books_by_category(category)
            print("\n=== Books in Category ===")
            for book in results:
                print(f"- {book.title} by {book.author} (${book.price})")
        elif choice == "4":
            plans = membership_service.list_plans()
            print("\n=== Membership Plans ===")
            for plan in plans:
                print(f"- {plan.plan_name}: ${plan.plan_price}")
        elif choice == "5":
            plan_id = int(input("Enter the plan ID to purchase: "))
            membership_service.purchase_plan(user.id, plan_id)
        elif choice == "6":
            new_plan_id = int(input("Enter the new plan ID to upgrade: "))
            membership_service.upgrade_plan(user.id, new_plan_id, "data/books.json")
        elif choice == "7":
            transactions = transaction_service.list_user_transactions(user.email)
            print("\n=== Your Transactions ===")
            for tx in transactions:
                print(f"- Book ID: {tx.book_id}, Price: ${tx.price}, Date: {tx.transaction_date}")
        elif choice == "8":
            book_id = int(input("Enter the ID of the book you want to purchase: "))
            transaction_service.record_transaction(user.email, book_id, book_service.find_by_id(book_id)["price"])
        elif choice == "9":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")
