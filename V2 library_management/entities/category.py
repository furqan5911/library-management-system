# Category entity
class Category:
    """
    Represents a Category entity in the system.

    Attributes:
        id (int): Unique identifier for the category.
        name (str): Name of the category.
    """
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_dict(self):
        """
        Converts the Category object into a dictionary for JSON storage.

        :return: Dictionary representation of the Category object.
        """
        return {
            "id": self.id,
            "name": self.name,
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Category object from a dictionary.

        :param data: Dictionary containing category data.
        :return: Category object created from the dictionary data.
        """
        return Category(
            id=data["id"],
            name=data["name"],
        )
