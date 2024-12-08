# Service class for Category operations


from repositories.category_repository import CategoryRepository
from entities.category import Category


class CategoryService:
    """
    Service class for managing categories in the library system.
    """

    def __init__(self, db_client):
        """
        Initializes the CategoryService with a database client.
        """
        self.category_repo = CategoryRepository(db_client)

    def add_category(self, data):
        """
        Adds a new category to the library system.

        :param data: Dictionary containing category details (e.g., name).
        :return: The created or existing category as a dictionary.
        """
        try:
            # Check if the category already exists
            existing_category = self.category_repo.find_by_name(data["name"])
            if existing_category:
                print(f"Category '{data['name']}' already exists.")
                return Category.from_dict(existing_category).to_dict()

            # Add new category
            category_id = self.category_repo.add_category(data)
            return Category(category_id, data["name"]).to_dict()
        except Exception as e:
            print(f"Error adding category: {e}")
            return None

    def list_categories(self):
        """
        Lists all categories in the system.

        :return: A list of categories as dictionaries.
        """
        try:
            categories = self.category_repo.list_categories()
            return [Category.from_dict(category).to_dict() for category in categories]
        except Exception as e:
            print(f"Error listing categories: {e}")
            return []

    def find_category_by_name(self, name):
        """
        Finds a category by its name.

        :param name: The name of the category.
        :return: The category as a dictionary, or None if not found.
        """
        try:
            category = self.category_repo.find_by_name(name)
            return Category.from_dict(category).to_dict() if category else None
        except Exception as e:
            print(f"Error finding category by name: {e}")
            return None

    def delete_category(self, category_id):
        """
        Deletes a category from the library system.

        :param category_id: The ID of the category to delete.
        :return: True if successful, False otherwise.
        """
        try:
            return self.category_repo.delete(category_id)
        except Exception as e:
            print(f"Error deleting category with ID {category_id}: {e}")
            return False
