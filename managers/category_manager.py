# Category_manager file
import json
from entities.category import Category



class CategoryManager:
    """
    A manager class to handle operations related to categories.
    Attributes:
        categories_file (str): The path to the JSON file where categories are stored.
        categories_list (list): A list to store category objects.
    Methods:
        load_categories_from_disk():
            Load categories from a JSON file.
        save_categories_to_disk():
            Save the current categories list to a JSON file.
        add_category(current_user, name):
            Add a new category (Admin-only).
        update_category(current_user, old_name, new_name):
            Update an existing category's name (Admin-only).
        remove_category(current_user, name):
            Remove a category by name (Admin-only).
        list_categories():
            List all categories (Accessible to all users).
    """
    def __init__(self, categories_file="categories.json"):
        self.categories_file = categories_file
        self.categories_list = []

    def load_categories_from_disk(self):
        """Load categories from a JSON file."""
        try:
            with open(self.categories_file, "r") as file:
                data = json.load(file)
                self.categories_list = [Category.from_dict(cat) for cat in data]
                print("Categories loaded successfully!")
        except FileNotFoundError:
            self.categories_list = []
            print("No categories found. Starting fresh.")

    def save_categories_to_disk(self):
        """Save the current categories list to a JSON file."""
        with open(self.categories_file, "w") as file:
            data = [category.to_dict() for category in self.categories_list]
            json.dump(data, file, indent=4)
            print("Categories saved successfully!")

    def add_category(self, current_user, name):
        """Add a new category (Admin-only)."""
        if not current_user.is_admin():
            print("Error: Only admins can add categories.")
            return False
        if any(category.name == name for category in self.categories_list):
            print(f"Error: Category '{name}' already exists!")
            return False
        new_category = Category(name)
        self.categories_list.append(new_category)
        self.save_categories_to_disk()
        print(f"Category '{name}' added successfully!")
        return True

    def update_category(self, current_user, old_name, new_name):
        """Update an existing category's name (Admin-only)."""
        if not current_user.is_admin():
            print("Error: Only admins can update categories.")
            return False
        for category in self.categories_list:
            if category.name == old_name:
                category.name = new_name
                self.save_categories_to_disk()
                print(f"Category '{old_name}' updated to '{new_name}' successfully!")
                return True
        print(f"Error: Category '{old_name}' not found.")
        return False

    def remove_category(self, current_user, name):
        """Remove a category by name (Admin-only)."""
        if not current_user.is_admin():
            print("Error: Only admins can remove categories.")
            return False
        self.categories_list = [category for category in self.categories_list if category.name != name]
        self.save_categories_to_disk()
        print(f"Category '{name}' removed successfully!")

    def list_categories(self):
        """List all categories (Accessible to all users)."""
        if not self.categories_list:
            print("No categories available!")
        else:
            print("\n=== Available Categories ===")
            for category in self.categories_list:
                print(f"- {category.name}")

