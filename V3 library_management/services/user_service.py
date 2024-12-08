# Service class for User operations


from repositories.user_repository import UserRepository
from entities.user import User
from services.base_service import BaseService


class UserService(BaseService):
    """
    Service class for managing users in the library system.
    """

    def __init__(self, db_client):
        """
        Initializes the UserService with a database client.
        """
        super().__init__()
        self.user_repository = UserRepository(db_client)

    def create_user(self, first_name, last_name, email, password, role="user"):
        """
        Creates a new user in the system.
        Ensures no duplicate emails and adds the user to the database.

        :param first_name: First name of the user.
        :param last_name: Last name of the user.
        :param email: Email address of the user.
        :param password: Password of the user.
        :param role: Role of the user (default is 'user').
        :return: The created user's ID or an error message.
        """
        try:
            self.validate_required_fields(
                {"first_name": first_name, "last_name": last_name, "email": email, "password": password},
                ["first_name", "last_name", "email", "password"]
            )

            # Check for duplicate email
            if self.user_repository.find_by_email(email):
                raise ValueError("A user with this email already exists.")

            user_data = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password,
                "role": role,
            }
            user_id = self.user_repository.create_user(user_data)
            return user_id
        except Exception as e:
            self.handle_error("creating user", e)
            return None

    def authenticate_user(self, email, password):
        """
        Authenticates a user by email and password.

        :param email: The user's email.
        :param password: The user's password.
        :return: The authenticated User object or None if authentication fails.
        """
        try:
            self.validate_required_fields({"email": email, "password": password}, ["email", "password"])
            user = self.user_repository.find_by_email(email)
            if not user or user["password"] != password:
                raise ValueError("Invalid email or password.")
            return self.map_to_entity(User, user)
        except Exception as e:
            self.handle_error("authenticating user", e)
            return None

    def list_users(self):
        """
        Lists all users in the system.

        :return: A list of User objects as dictionaries.
        """
        try:
            users = self.user_repository.list_all_users()
            return [self.map_to_entity(User, user).to_dict() for user in users]
        except Exception as e:
            self.handle_error("listing users", e)
            return []

    def ensure_default_admin(self):
        """
        Ensures a default admin exists in the database.

        :return: True if a default admin exists or was created successfully, False otherwise.
        """
        try:
            if not self.user_repository.check_admin_exists():
                admin_data = {
                    "first_name": "Default",
                    "last_name": "Admin",
                    "email": "admin@example.com",
                    "password": "adminpass",
                    "role": "admin",
                }
                self.user_repository.create_user(admin_data)
                print("Default admin created successfully.")
            return True
        except Exception as e:
            self.handle_error("ensuring default admin", e)
            return False

    def delete_user(self, user_id):
        """
        Deletes a user from the system.

        :param user_id: The ID of the user to delete.
        :return: True if successful, False otherwise.
        """
        try:
            return self.user_repository.delete(user_id)
        except Exception as e:
            self.handle_error(f"deleting user ID {user_id}", e)
            return False
