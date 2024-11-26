# UserService class
from abstract_classes.base_service import BaseService
from entities.user import User

class UserService(BaseService):
    """
    Handles user-related functionality such as login, sign-up, and admin restrictions.

    Methods:
        login(email, password): Authenticates a user.
        sign_up(user_data): Creates a new user (user-only sign-up).
    """
    DEFAULT_ADMIN = {
        "id": 1,
        "first_name": "Default",
        "last_name": "Admin",
        "email": "admin@gmail.com",
        "password": "adminpass",  
        "role": "admin"
    }

    def __init__(self, file_path):
        super().__init__(file_path)
        self.users = self.load()
        self.ensure_default_admin()

    def ensure_default_admin(self):
        """
        Ensures that a default admin account exists in the system.
        """
        if not any(user["role"] == "admin" for user in self.users):
            self.create(self.DEFAULT_ADMIN)

    def login(self, email, password):
        """
        Authenticates a user.

        :param email: User's email address.
        :param password: User's password.
        :return: The authenticated User object, or None if authentication fails.
        """
        user = self.find_one_by_q("email", email)
        if user and user["password"] == password:
            return User.from_dict(user)
        print("Invalid email or password.")
        return None

    def sign_up(self, user_data):
        """
        Registers a new user (restricted to 'user' role).

        :param user_data: Dictionary containing user information.
        :return: The created User object.
        """
        if user_data.get("role", "user") == "admin":
            raise ValueError("Sign-up is restricted to 'user' role only.")
        return self.create(user_data)