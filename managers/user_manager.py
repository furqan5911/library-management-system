import json
from entities.user import User

class UserManager:
    """
    UserManager handles user-related operations such as loading, saving, signing up, and logging in users.
    """
    def __init__(self, file_path="users.json"):
        self.file_path = file_path
        self.users_list = []
        # Hardcoded admin details
        self.admin_details = {
            "email": "admin@example.com",
            "password": "adminpass",
            "first_name": "Default",
            "last_name": "Admin",
            "role": "admin"
        }

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
        """Sign up a new user (restricted for admin accounts)."""
        if role == "admin":
            print("Error: Admin signup is restricted. Only one admin exists.")
            return False
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
        """Log in an existing user or the hardcoded admin."""
        # Check if the login is for the hardcoded admin
        if email == self.admin_details["email"] and password == self.admin_details["password"]:
            print(f"Welcome {self.admin_details['first_name']} (Admin)!")
            return User(
                first_name=self.admin_details["first_name"],
                last_name=self.admin_details["last_name"],
                email=self.admin_details["email"],
                password=self.admin_details["password"],
                role=self.admin_details["role"]
            )
        # Check if the login is for a regular user
        for user in self.users_list:
            if user.email == email and user.password == password:
                print(f"Welcome {user.first_name} ({'Admin' if user.is_admin() else 'User'})!")
                return user
        print("Invalid email or password.")
        return None

    def create_default_admin(self):
        """Create the hardcoded admin (for compatibility, does nothing in practice)."""
        print("Default admin already exists.")
