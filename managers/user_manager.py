# User_manager file
import json
from entities.user import User

class UserManager:
    """
    UserManager handles user-related operations such as loading, saving, signing up, and logging in users.
    Attributes:
        file_path (str): The path to the JSON file where user data is stored.
        users_list (list): A list of User objects representing the users.
    Methods:
        load_users_from_disk():
            Load users from a JSON file. If the file does not exist, initialize an empty user list.
        save_users_to_disk():
            Save the current users list to a JSON file.
        signup_user(first_name, last_name, email, password, role="user"):
            Sign up a new user or admin. Returns False if the email is already registered, otherwise True.
        login_user(email, password):
            Log in an existing user. Returns the User object if successful, otherwise None.
        create_default_admin():
            Ensure there is at least one admin account. Creates a default admin account if none exists.
    """
    def __init__(self, file_path="users.json"):
        self.file_path = file_path
        self.users_list = []

    def load_users_from_disk(self):
        """Load users from a JSON file."""
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
                self.users_list = [User.from_dict(user) for user in data]
                print("Users loaded successfully!")
        except FileNotFoundError:
            self.users_list = []
            print("No users found. Starting fresh.")

    def save_users_to_disk(self):
        """Save the current users list to a JSON file."""
        with open(self.file_path, "w") as file:
            data = [user.to_dict() for user in self.users_list]
            json.dump(data, file, indent=4)
            print("Users saved successfully!")

    def signup_user(self, first_name, last_name, email, password, role="user"):
        """Sign up a new user or admin."""
        # Check if the email is already registered
        if any(user.email == email for user in self.users_list):
            print("Error: Email already exists!")
            return False
        # Create and add the user
        new_user = User(first_name, last_name, email, password, role)
        self.users_list.append(new_user)
        self.save_users_to_disk()
        print(f"User {email} signed up successfully as {role}!")
        return True

    def login_user(self, email, password):
        """Log in an existing user."""
        for user in self.users_list:
            if user.email == email and user.password == password:
                print(f"Welcome {user.first_name} ({'Admin' if user.is_admin() else 'User'})!")
                return user
        print("Invalid email or password.")
        return None

    def create_default_admin(self):
        """Ensure there is at least one admin account."""
        if not any(user.is_admin() for user in self.users_list):
            print("No admin found. Creating a default admin account...")
            self.signup_user(
                first_name="Default",
                last_name="Admin",
                email="admin@example.com",
                password="adminpass",
                role="admin"
            )
