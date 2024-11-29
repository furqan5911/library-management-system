def author_menu(admin, author_service):
    """
    Menu for managing authors (Admin only).
    """
    while True:
        print("\n=== Manage Authors ===")
        print("1. Add Author")
        print("2. Update Author")
        print("3. Delete Author")
        print("4. Assign Book to Author")
        print("5. List All Authors")
        print("0. Go Back")
        choice = input("Enter your choice: ")

        if choice == "1":
            first_name = input("Enter author's first name: ")
            last_name = input("Enter author's last name: ")
            email = input("Enter author's email: ")
            author_service.add_author(admin, {"first_name": first_name, "last_name": last_name, "email": email})
            print("Author added successfully!")
        elif choice == "2":
            author_id = int(input("Enter author ID to update: "))
            updated_data = {}
            print("Leave fields blank to skip.")
            first_name = input("New first name: ")
            if first_name:
                updated_data["first_name"] = first_name
            if author_service.update_author(admin, author_id, updated_data):
                print("Author updated successfully!")
            else:
                print(f"Error: No author found with ID: {author_id}")
        elif choice == "3":
            author_id = int(input("Enter author ID to delete: "))
            # Check if the deletion was successful
            if author_service.delete_author(admin, author_id):
                print("Author deleted successfully!")
            else:
                print(f"Error: No author found with ID: {author_id}")
        elif choice == "4":
            author_id = int(input("Enter author ID: "))
            book_id = int(input("Enter book ID to assign: "))
            if author_service.assign_book_to_author(admin, author_id, book_id):
                print("Book assigned to author successfully!")
            else:
                print("Error: Could not assign book. Check the author or book ID.")
        elif choice == "5":
            authors = author_service.list_authors()
            print("\n=== Authors ===")
            for author in authors:
                print(f"- {author.first_name} {author.last_name} (Email: {author.email})")
        elif choice == "0":
            print("Returning to Admin Dashboard...")
            return
        else:
            print("Invalid choice! Please try again.")


