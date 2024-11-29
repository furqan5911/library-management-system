def category_menu(admin, category_service):
    """
    Menu for managing categories (Admin only).
    """
    while True:
        print("\n=== Manage Categories ===")
        print("1. Add Category")
        print("2. Update Category")
        print("3. Delete Category")
        print("4. List All Categories")
        print("0. Go Back")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter category name: ")
            category_service.add_category(admin, {"name": name})
            print("Category added successfully!")
        elif choice == "2":
            category_id = int(input("Enter category ID to update: "))
            new_name = input("Enter new category name: ")
            if category_service.update_category(admin, category_id, new_name):
                print("Category updated successfully!")
            else:
                print(f"Error: No category found with ID: {category_id}")
        elif choice == "3":
            category_id = int(input("Enter category ID to delete: "))
            # Check if the deletion was successful
            if category_service.delete_category(admin, category_id):
                print("Category deleted successfully!")
            else:
                print(f"Error: No category found with ID: {category_id}")
        elif choice == "4":
            categories = category_service.list_categories()
            print("\n=== Categories ===")
            for category in categories:
                print(f"- {category.name}")
        elif choice == "0":
            print("Returning to Admin Dashboard...")
            return
        else:
            print("Invalid choice! Please try again.")






