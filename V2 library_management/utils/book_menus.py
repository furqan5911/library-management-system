def book_menu(admin, book_service):
    """
    Menu for managing books (Admin only).
    """
    while True:
        print("\n=== Manage Books ===")
        print("1. Add Book")
        print("2. Update Book")
        print("3. Delete Book")
        print("4. View All Books")
        print("0. Go Back")
        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            category = input("Enter book category: ")
            publication_date = input("Enter publication date (YYYY-MM-DD): ")
            price = float(input("Enter book price: "))
            isbn = input("Enter book ISBN: ")
            book_service.add_book(admin, {
                "title": title, "author": author, "category": category,
                "publication_date": publication_date, "price": price, "isbn": isbn
            })
            print("Book added successfully!")
        elif choice == "2":
            book_id = int(input("Enter book ID to update: "))
            updated_data = {}
            print("Leave fields blank to skip.")
            title = input("New title: ")
            if title:
                updated_data["title"] = title
            if book_service.update_book(admin, book_id, updated_data):
                print("Book updated successfully!")
            else:
                print(f"Error: No book found with ID: {book_id}")
        elif choice == "3":
            book_id = int(input("Enter book ID to delete: "))
            # Check if the deletion was successful
            if book_service.delete_book(admin, book_id):
                print("Book deleted successfully!")
            else:
                print(f"Error: No book found with ID: {book_id}")
        elif choice == "4":
            books = book_service.list_books()
            print("\n=== Books ===")
            for book in books:
                print(f"- {book.title} by {book.author} (${book.price})")
        elif choice == "0":
            print("Returning to Admin Dashboard...")
            return
        else:
            print("Invalid choice! Please try again.")


