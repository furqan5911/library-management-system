# Service class for Membership operations


from repositories.membership_repository import MembershipRepository
from entities.membership import Membership
from services.base_service import BaseService


class MembershipService(BaseService):
    """
    Service class for managing membership plans in the library system.
    """

    def __init__(self, db_client):
        """
        Initializes the MembershipService with a database client.
        """
        super().__init__()
        self.membership_repo = MembershipRepository(db_client)

    def add_membership(self, data):
        """
        Adds a new membership plan to the system.

        :param data: Dictionary containing membership plan details (e.g., plan_name, plan_price).
        :return: The created membership plan or an error message if it already exists.
        """
        try:
            self.validate_required_fields(data, ["plan_name", "plan_price"])

            # Check if the membership plan already exists
            existing_plan = self.membership_repo.find_by_name(data["plan_name"])
            if existing_plan:
                return f"Membership plan '{data['plan_name']}' already exists."

            # Add the membership plan
            membership_id = self.membership_repo.add_membership(data)
            return Membership(
                id=membership_id,
                plan_name=data["plan_name"],
                plan_price=data["plan_price"],
                created_at=None,  # Let the database handle created_at
            ).to_dict()
        except Exception as e:
            self.handle_error("adding membership plan", e)
            return None

    def list_memberships(self):
        """
        Lists all membership plans in the system.

        :return: A list of membership plans as dictionaries.
        """
        try:
            memberships = self.membership_repo.list_memberships()
            return [self.map_to_entity(Membership, membership).to_dict() for membership in memberships]
        except Exception as e:
            self.handle_error("listing memberships", e)
            return []

    def update_membership(self, membership_id, data):
        """
        Updates an existing membership plan.

        :param membership_id: The ID of the membership plan to update.
        :param data: Dictionary containing updated membership plan details.
        :return: True if successful, False otherwise.
        """
        try:
            self.validate_required_fields(data, ["plan_price"])
            return self.membership_repo.update_membership(membership_id, data)
        except Exception as e:
            self.handle_error(f"updating membership ID {membership_id}", e)
            return False

    def find_membership_by_id(self, membership_id):
        """
        Finds a membership plan by its ID.

        :param membership_id: The ID of the membership plan.
        :return: The membership plan as a dictionary, or None if not found.
        """
        try:
            membership = self.membership_repo.find_by_id(membership_id)
            return self.map_to_entity(Membership, membership).to_dict() if membership else None
        except Exception as e:
            self.handle_error(f"finding membership by ID {membership_id}", e)
            return None

    def delete_membership(self, membership_id):
        """
        Deletes a membership plan from the system.

        :param membership_id: The ID of the membership plan to delete.
        :return: True if successful, False otherwise.
        """
        try:
            return self.membership_repo.delete_membership(membership_id)
        except Exception as e:
            self.handle_error(f"deleting membership ID {membership_id}", e)
            return False
