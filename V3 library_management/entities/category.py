# Category entity


class Category:
    """
    Represents a category in the library system.

    Attributes:
        id (int): The unique identifier for the category.
        name (str): The name of the category.
    """

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_dict(self):
        """
        Converts the Category object into a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Category object from a dictionary.
        """
        return Category(
            id=data["id"],
            name=data["name"],
        )
