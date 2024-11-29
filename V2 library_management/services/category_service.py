# CategoryService class

from abstract_classes.base_service import BaseService
from entities.category import Category

class CategoryService(BaseService):
    """
    Handles category-related functionality such as adding, updating, deleting, and listing categories.

    Methods:
        add_category(current_user, category_data): Adds a new category (Admin-only).
        update_category(current_user, category_id, updated_name): Updates category details (Admin-only).
        delete_category(current_user, category_id): Deletes a category (Admin-only).
        list_categories(): Lists all categories.
    """
    def __init__(self, file_path):
        super().__init__(file_path)
        try:
            self.categories = self.load()
        except Exception as e:
            print(f"Error loading categories: {e}")
            self.categories = []

    def add_category(self, current_user, category_data):
        """
        Adds a new category to the system (Admin-only).

        :param current_user: The admin user adding the category.
        :param category_data: Dictionary containing category information.
        :return: The created Category object.
        """
        try:
            if not current_user.is_admin():
                raise PermissionError("Only admins can add categories.")
            return self.create(category_data)
        except PermissionError as e:
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error while adding category: {e}")
            return None

    def update_category(self, current_user, category_id, updated_name):
        """
        Updates category details (Admin-only).

        :param current_user: The admin user updating the category.
        :param category_id: ID of the category to update.
        :param updated_name: New name for the category.
        :return: The updated Category object.
        """
        try:
            if not current_user.is_admin():
                raise PermissionError("Only admins can update categories.")
            return self.update(category_id, {"name": updated_name})
        except PermissionError as e:
            print(f"Error: {e}")
            return None
        except ValueError as e:
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error while updating category: {e}")
            return None

    def delete_category(self, current_user, category_id):
        """
        Deletes a category from the system (Admin-only).

        :param current_user: The admin user deleting the category.
        :param category_id: ID of the category to delete.
        :return: True if deletion was successful.
        """
        try:
            if not current_user.is_admin():
                raise PermissionError("Only admins can delete categories.")
            return self.delete(category_id)
        except PermissionError as e:
            print(f"Error: {e}")
            return False
        except ValueError as e:
            print(f"Error: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error while deleting category: {e}")
            return False

    def list_categories(self):
        """
        Lists all categories in the system.

        :return: List of all categories.
        """
        try:
            return [Category.from_dict(category) for category in self.categories]
        except Exception as e:
            print(f"Error while listing categories: {e}")
            return []


