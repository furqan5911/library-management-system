# MembershipService class
from abstract_classes.base_service import BaseService
from entities.membership import Membership
import json


class MembershipService(BaseService):
    """
    Handles membership-related functionality such as adding, updating, deleting, 
    viewing, purchasing, and upgrading membership plans.
    """
    def __init__(self, file_path, user_membership_file):
        super().__init__(file_path)
        self.user_membership_file = user_membership_file

    def load_user_memberships(self):
        """
        Loads user-specific membership data from the file.
        """
        try:
            with open(self.user_membership_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_user_memberships(self, user_memberships):
        """
        Saves user-specific membership data to the file.
        """
        with open(self.user_membership_file, "w") as file:
            json.dump(user_memberships, file, indent=4)

    def purchase_plan(self, user_id, plan_id):
        """
        Allows a user to purchase a membership plan.
        """
        plan = self.find_by_id(plan_id)
        if not plan:
            raise ValueError(f"No plan found with ID: {plan_id}")

        user_memberships = self.load_user_memberships()
        if user_id in user_memberships:
            raise ValueError("User already has a membership plan.")

        user_memberships[user_id] = {
            "plan_id": plan["id"],
            "plan_name": plan["plan_name"],
            "remaining_balance": plan["plan_price"]
        }
        self.save_user_memberships(user_memberships)
        print(f"Membership plan '{plan['plan_name']}' purchased successfully!")

    def upgrade_plan(self, user_id, new_plan_id, books_file_path):
        """
        Allows a user to upgrade their membership plan.
        """
        user_memberships = self.load_user_memberships()
        current_plan = user_memberships.get(user_id)
        if not current_plan:
            raise ValueError("User does not have an active membership plan.")

        new_plan = self.find_by_id(new_plan_id)
        if not new_plan:
            raise ValueError(f"No plan found with ID: {new_plan_id}")

        try:
            with open(books_file_path, "r") as file:
                books = json.load(file)
                lowest_book_price = min(book["price"] for book in books if book.get("price"))
        except (FileNotFoundError, ValueError):
            raise ValueError("Unable to load or find valid books.")

        if current_plan["remaining_balance"] < lowest_book_price:
            if current_plan["plan_id"] == new_plan["id"]:
                current_plan["remaining_balance"] = new_plan["plan_price"]
                user_memberships[user_id] = current_plan
                self.save_user_memberships(user_memberships)
                print("Upgraded to the same plan due to insufficient balance.")
                return

        if new_plan["plan_price"] <= current_plan["remaining_balance"]:
            raise ValueError("Upgrade can only be done to a higher-priced plan.")

        current_plan["remaining_balance"] = new_plan["plan_price"]
        user_memberships[user_id] = current_plan
        self.save_user_memberships(user_memberships)
        print("Membership plan upgraded successfully!")
