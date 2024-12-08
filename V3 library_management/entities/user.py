# User entity
# User entity

class User:
    """
    Represents the User entity in the library system.

    Attributes:
        id (int): Unique identifier for the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email of the user.
        password (str): The user's hashed password.
        joined_date (datetime): The date when the user joined the system.
        role (str): The role of the user (e.g., 'admin' or 'user').
    """

    def __init__(self, id, first_name, last_name, email, password, joined_date, role):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.joined_date = joined_date
        self.role = role

    def to_dict(self):
        """
        Converts the User object into a dictionary.
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "joined_date": self.joined_date.strftime("%Y-%m-%d %H:%M:%S"),
            "role": self.role,
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a User object from a dictionary.
        """
        return User(
            id=data.get("id"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            password=data.get("password"),
            joined_date=data.get("joined_date"),
            role=data.get("role"),
        )
