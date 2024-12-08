# Service class for User-Membership operations


from repositories.user_membership_repository import UserMembershipRepository
from entities.user_membership import UserMembership
from services.base_service import BaseService
from datetime import datetime


class UserMembershipService(BaseService):
    """
    Service class for managing user memberships in the library system.
    """

    def __init__(self, db_client):
        """
        Initializes the UserMembershipService with a database client.
        """
        super().__init__()
        self.user_membership_repo = UserMembershipRepository(db_client)

    def create_user_membership(self, user_id, membership_id, balance):
        """
        Creates a new user membership record.

        :param user_id: The ID of the user.
        :param membership_id: The ID of the membership plan.
        :param balance: Initial balance for the membership.
        :return: The created user membership record or an error message.
        """
        try:
            # Validate required fields
            self.validate_required_fields(
                {"user_id": user_id, "membership_id": membership_id, "balance": balance},
                ["user_id", "membership_id", "balance"]
            )

            # Check if the user already has a membership
            existing_membership = self.user_membership_repo.get_membership_by_user_id(user_id)
            if existing_membership:
                return f"User ID {user_id} already has an active membership."

            # Create a new user membership
            data = {
                "user_id": user_id,
                "membership_id": membership_id,
                "remaining_balance": balance,
                "joined_date": datetime.now(),
            }
            user_membership_id = self.user_membership_repo.add_user_membership(data)
            return UserMembership(
                id=user_membership_id,
                user_id=user_id,
                membership_id=membership_id,
                remaining_balance=balance,
                joined_date=data["joined_date"],
            ).to_dict()
        except Exception as e:
            self.handle_error("creating user membership", e)
            return None

    def update_remaining_balance(self, user_id, new_balance):
        """
        Updates the remaining balance for a user's membership.

        :param user_id: The ID of the user.
        :param new_balance: The new remaining balance.
        :return: True if successful, False otherwise.
        """
        try:
            return self.user_membership_repo.update_balance(user_id, new_balance)
        except Exception as e:
            self.handle_error(f"updating remaining balance for user ID {user_id}", e)
            return False

    def get_user_membership(self, user_id):
        """
        Retrieves a user's membership details.

        :param user_id: The ID of the user.
        :return: The user membership record or None if not found.
        """
        try:
            membership = self.user_membership_repo.get_membership_by_user_id(user_id)
            return self.map_to_entity(UserMembership, membership).to_dict() if membership else None
        except Exception as e:
            self.handle_error(f"retrieving membership for user ID {user_id}", e)
            return None

    def list_all_user_memberships(self):
        """
        Lists all user memberships in the system.

        :return: A list of user memberships as dictionaries.
        """
        try:
            memberships = self.user_membership_repo.list_all()
            return [self.map_to_entity(UserMembership, membership).to_dict() for membership in memberships]
        except Exception as e:
            self.handle_error("listing all user memberships", e)
            return []

    def delete_user_membership(self, user_membership_id):
        """
        Deletes a user membership record.

        :param user_membership_id: The ID of the user membership to delete.
        :return: True if successful, False otherwise.
        """
        try:
            return self.user_membership_repo.delete(user_membership_id)
        except Exception as e:
            self.handle_error(f"deleting user membership ID {user_membership_id}", e)
            return False
