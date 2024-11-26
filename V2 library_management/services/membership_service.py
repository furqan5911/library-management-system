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

# from abstract_classes.base_service import BaseService
# from entities.membership import Membership
# import json

# class MembershipService(BaseService):
#     """
#     Handles membership-related functionality such as adding, updating, deleting, 
#     viewing, purchasing, and upgrading membership plans.

#     Methods:
#         add_plan(current_user, plan_data): Adds a new membership plan (Admin-only).
#         update_plan(current_user, plan_id, updated_data): Updates membership plan details (Admin-only).
#         delete_plan(current_user, plan_id): Deletes a membership plan (Admin-only).
#         list_plans(): Lists all membership plans.
#         purchase_plan(user_id, plan_id): Allows users to purchase a membership plan.
#         upgrade_plan(user_id, new_plan_id): Allows users to upgrade their membership plan.
#     """
#     def __init__(self, file_path):
#         super().__init__(file_path)
#         self.plans = self.load()
#         self.user_memberships = {}  # Tracks user memberships by user_id

#     def add_plan(self, current_user, plan_data):
#         """
#         Adds a new membership plan to the system (Admin-only).

#         :param current_user: The admin user adding the plan.
#         :param plan_data: Dictionary containing plan information.
#         :return: The created Membership object.
#         """
#         if not current_user.is_admin():
#             raise PermissionError("Only admins can add membership plans.")
#         return self.create(plan_data)

#     def update_plan(self, current_user, plan_id, updated_data):
#         """
#         Updates membership plan details (Admin-only).

#         :param current_user: The admin user updating the plan.
#         :param plan_id: ID of the plan to update.
#         :param updated_data: Dictionary containing updated plan details.
#         :return: The updated Membership object.
#         """
#         if not current_user.is_admin():
#             raise PermissionError("Only admins can update membership plans.")
#         return self.update(plan_id, updated_data)

#     def delete_plan(self, current_user, plan_id):
#         """
#         Deletes a membership plan (Admin-only).

#         :param current_user: The admin user deleting the plan.
#         :param plan_id: ID of the plan to delete.
#         :return: True if deletion was successful.
#         """
#         if not current_user.is_admin():
#             raise PermissionError("Only admins can delete membership plans.")
#         return self.delete(plan_id)

#     def list_plans(self):
#         """
#         Lists all membership plans in the system.

#         :return: List of all membership plans.
#         """
#         return [Membership.from_dict(plan) for plan in self.plans]

#     def purchase_plan(self, user_id, plan_id):
#         """
#         Allows a user to purchase a membership plan.

#         :param user_id: ID of the user purchasing the plan.
#         :param plan_id: ID of the plan to purchase.
#         :return: The purchased Membership object.
#         """
#         plan = self.find_by_id(plan_id)
#         if not plan:
#             raise ValueError(f"No plan found with ID: {plan_id}")
#         if user_id in self.user_memberships:
#             raise ValueError("User already has a membership plan.")
#         self.user_memberships[user_id] = plan
#         return plan

#     def upgrade_plan(self, user_id, new_plan_id, books_file_path):
#         """
#         Allows a user to upgrade their membership plan.

#         :param user_id: ID of the user upgrading the plan.
#         :param new_plan_id: ID of the new plan to upgrade to.
#         :param books_file_path: Path to the books.json file.
#         :return: The upgraded Membership object.
#         """
#         # Validate the user's current membership
#         current_plan = self.user_memberships.get(user_id)
#         if not current_plan:
#             raise ValueError("User does not have an active membership plan.")

#         # Load the new plan details
#         new_plan = self.find_by_id(new_plan_id)
#         if not new_plan:
#             raise ValueError(f"No plan found with ID: {new_plan_id}")

#         # Load book data and find the lowest price
#         try:
#             with open(books_file_path, "r") as file:
#                 books = json.load(file)
#                 lowest_book_price = min(book["price"] for book in books if book.get("price"))
#         except FileNotFoundError:
#             raise ValueError("Books data file not found.")
#         except ValueError:
#             raise ValueError("No valid books found to determine the lowest price.")

#         # Check if the user's balance is less than the lowest book price
#         if current_plan["plan_price"] < lowest_book_price:
#             if current_plan["id"] == new_plan["id"]:
#                 # Allow upgrading to the same plan due to insufficient balance
#                 current_plan["plan_price"] = new_plan["plan_price"]
#                 self.update(current_plan["id"], current_plan)
#                 print("Upgrade successful to the same plan due to insufficient balance.")
#                 return current_plan
#             else:
#                 raise ValueError("Upgrade to a different plan requires sufficient balance.")

#         # Enforce rule: Upgrade can only be done to a higher-priced plan
#         if new_plan["plan_price"] <= current_plan["plan_price"]:
#             raise ValueError("Upgrade can only be done to a higher-priced plan.")

#         # Perform the upgrade
#         current_plan["plan_price"] = new_plan["plan_price"]
#         self.update(current_plan["id"], current_plan)
#         print("Membership plan upgraded successfully!")
#         return current_plan


#     def validate_membership(self, user_id):
#             """
#             Validates if the user has an active membership.

#             :param user_id: ID of the user.
#             :return: Membership object if valid, otherwise raises an error.
#             """
#             user_membership = self.user_memberships.get(user_id)
#             if not user_membership:
#                 raise ValueError("You do not have an active membership.")
#             return user_membership

#     def deduct_balance(self, user_id, amount):
#             """
#             Deducts the balance from the user's membership plan.

#             :param user_id: ID of the user.
#             :param amount: Amount to deduct.
#             """
#             membership = self.validate_membership(user_id)
#             if membership["plan_price"] < amount:
#                 raise ValueError("Insufficient balance in your membership plan.")
#             membership["plan_price"] -= amount
#             self.update(membership["id"], membership)