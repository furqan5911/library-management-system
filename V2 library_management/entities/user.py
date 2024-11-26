# User entity
from datetime import datetime

class User:
    """
    Represents a User entity in the system.

    Attributes:
        id (int): Unique identifier for the user.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        email (str): Email address of the user.
        password (str): Encrypted password for authentication.
        role (str): Role of the user (e.g., 'admin' or 'user').
        joined_date (str): Date and time when the user joined the system.
    """
    def __init__(self, id, first_name, last_name, email, password, role="user"):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.role = role
        self.joined_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def is_admin(self):
        """
        Checks if the user is an admin.

        :return: True if the user is an admin, False otherwise.
        """
        return self.role == "admin"

    def to_dict(self):
        """
        Converts the User object into a dictionary for JSON storage.

        :return: Dictionary representation of the User object.
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "joined_date": self.joined_date,
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a User object from a dictionary.

        :param data: Dictionary containing user data.
        :return: User object created from the dictionary data.
        """
        return User(
            id=data["id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password=data["password"],
            role=data["role"],
        )
