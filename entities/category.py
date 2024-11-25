# Category file

class Category:
    """
    A class used to represent a Category.
    Attributes
    ----------
    name : str
        the name of the category
    Methods
    -------
    to_dict():
        Converts the Category instance to a dictionary.
    from_dict(data):
        Creates a Category instance from a dictionary.
    """
    """
        Parameters
        ----------
        name : str
            The name of the category.
        """
    """
        Converts the Category instance to a dictionary.
        Returns
        -------
        dict
            A dictionary representation of the Category instance.
        """
    """
        Creates a Category instance from a dictionary.
        Parameters
        ----------
        data : dict
            A dictionary containing the category data.
        Returns
        -------
        Category
            A Category instance created from the dictionary data.
        """
    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {"name": self.name}

    @staticmethod
    def from_dict(data):
        return Category(data["name"])