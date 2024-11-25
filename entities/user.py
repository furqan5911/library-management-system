# User file
from datetime import datetime

# User Entity
class User:
    def __init__(self, first_name, last_name, email, password, role="user"):
        """
        Initialize a new User object.
        
        :param first_name: First name of the user
        :param last_name: Last name of the user
        :param email: Email address of the user
        :param password: Password for the user account
        :param role: Role of the user, default is 'user'
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.joined_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current date and time
        self.role = role  # Can be 'admin' or 'user'

    def is_admin(self):
        """
        Check if the user is an admin.
        
        :return: True if the user is an admin, False otherwise
        """
        return self.role == "admin"

    def to_dict(self):
        """
        Convert the user object to a dictionary for JSON storage.
        
        :return: Dictionary representation of the user object
        """
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "joined_date": self.joined_date,
            "role": self.role,
        }

    @staticmethod
    def from_dict(data):
        """
        Create a User object from a dictionary.
        
        :param data: Dictionary containing user data
        :return: User object created from the dictionary data
        """
        return User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password=data["password"],
            role=data["role"],
        )
