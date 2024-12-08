# Author entity
# Author entity

from datetime import datetime


class Author:
    """
    Represents an author in the library system.

    Attributes:
        id (int): The unique identifier for the author.
        first_name (str): The first name of the author.
        last_name (str): The last name of the author.
        email (str): The email of the author.
        joined_date (datetime): The date when the author was added.
    """

    def __init__(self, id, first_name, last_name, email, joined_date=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.joined_date = joined_date or datetime.now()

    def to_dict(self):
        """
        Converts the Author object into a dictionary.
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "joined_date": self.joined_date.strftime("%Y-%m-%d %H:%M:%S"),
        }

    @staticmethod
    def from_dict(data):
        """
        Creates an Author object from a dictionary.
        """
        return Author(
            id=data.get("id"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            joined_date=data.get("joined_date"),
        )
