# Repository for Category-related queries
# Repository for Category-related queries

from repositories.base_repository import BaseRepository


class CategoryRepository(BaseRepository):
    """
    Handles all category-related database operations.
    """

    def __init__(self, db_client):
        """
        Initialize the CategoryRepository with a database client and ensure the categories table exists.
        """
        super().__init__(db_client, "categories")
        self.create_table(self.get_category_schema())

    def get_category_schema(self):
        """
        Returns the SQL schema for the categories table.
        """
        return """
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL
        """

    def add_category(self, data):
        """
        Add a new category to the database.

        :param data: A dictionary containing category details.
        :return: The ID of the created category or None if the operation fails.
        """
        try:
            return self.insert(data)
        except Exception as e:
            print(f"Unexpected error while adding category: {e}")
            return None

    def list_categories(self):
        """
        Retrieve all categories.

        :return: A list of dictionaries representing all categories.
        """
        try:
            return self.list_all()
        except Exception as e:
            print(f"Error retrieving categories: {e}")
            return []

    def find_by_name(self, name):
        """
        Retrieve a category by its name.

        :param name: The name of the category.
        :return: A dictionary representing the category, or None if not found.
        """
        try:
            query = f"SELECT * FROM {self.table_name} WHERE name = %s;"
            with self.db_client.cursor() as cursor:
                cursor.execute(query, (name,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving category by name: {e}")
            return None
