# MembershipService class

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
            print("Error: User membership file not found. Starting with empty data.")
            return []
        except Exception as e:
            print(f"Unexpected error while loading user memberships: {e}")
            return []

    def save_user_memberships(self, user_memberships):
        """
        Saves user-specific membership data to the file.
        """
        try:
            with open(self.user_membership_file, "w") as file:
                json.dump(user_memberships, file, indent=4)
                print("User memberships saved successfully!")
        except Exception as e:
            print(f"Error while saving user memberships: {e}")

    def add_plan(self, current_user, plan_data):
        """
        Adds a new membership plan to the system (Admin-only).
        """
        try:
            if not current_user.is_admin():
                raise PermissionError("Only admins can add membership plans.")
            return self.create(plan_data)
        except PermissionError as e:
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error while adding plan: {e}")
            return None

    def update_plan(self, current_user, plan_id, updated_data):
        """
        Updates membership plan details (Admin-only).
        """
        try:
            if not current_user.is_admin():
                raise PermissionError("Only admins can update membership plans.")
            return self.update(plan_id, updated_data)
        except PermissionError as e:
            print(f"Error: {e}")
            return None
        except ValueError as e:
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error while updating plan: {e}")
            return None

    def delete_plan(self, current_user, plan_id):
        """
        Deletes a membership plan (Admin-only).
        """
        try:
            if not current_user.is_admin():
                raise PermissionError("Only admins can delete membership plans.")
            return self.delete(plan_id)
        except PermissionError as e:
            print(f"Error: {e}")
            return False
        except ValueError as e:
            print(f"Error: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error while deleting plan: {e}")
            return False

    def list_plans(self):
        """
        Lists all membership plans in the system.
        """
        try:
            plans = self.load()
            return [Membership.from_dict(plan) for plan in plans]
        except Exception as e:
            print(f"Error loading plans: {e}")
            return []

    def purchase_plan(self, user_id, email, plan_id):
        """
        Allows a user to purchase a membership plan.
        """
        try:
            # Ensure the plan exists
            plan = self.find_by_id(plan_id)
            if not plan:
                raise ValueError(f"No plan found with ID: {plan_id}")

            # Load user memberships
            user_memberships = self.load_user_memberships()

            # Check if the user already has a membership plan
            for membership in user_memberships:
                if membership["user_id"] == user_id:
                    raise ValueError(f"User already has an active plan '{membership['plan_name']}'.")

            # Assign the membership plan to the user
            user_memberships.append({
                "user_id": user_id,
                "email": email,  # Add email to the membership
                "plan_id": plan["id"],
                "plan_name": plan["plan_name"],
                "remaining_balance": plan["plan_price"]
            })

            # Save updated memberships
            self.save_user_memberships(user_memberships)
            print(f"Membership plan '{plan['plan_name']}' purchased successfully!")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error during plan purchase: {e}")

    def upgrade_plan(self, user_id, new_plan_id, books_file_path):
        """
        Allows a user to upgrade their membership plan.
        """
        try:
            # Load user memberships
            user_memberships = self.load_user_memberships()

            # Check if the user has an active membership plan
            current_plan = None
            for membership in user_memberships:
                if membership["user_id"] == user_id:
                    current_plan = membership
                    break

            if not current_plan:
                raise ValueError("User does not have an active membership plan.")

            # Find the new plan
            new_plan = self.find_by_id(new_plan_id)
            if not new_plan:
                raise ValueError(f"No plan found with ID: {new_plan_id}")

            # Ensure the new plan is higher-priced than the current plan
            if new_plan["plan_price"] <= current_plan["remaining_balance"]:
                raise ValueError("Upgrade can only be done to a higher-priced plan.")

            # Load books to check the lowest book price
            with open(books_file_path, "r") as file:
                books = json.load(file)
                lowest_book_price = min(book["price"] for book in books if book.get("price"))

            # Upgrade logic
            if current_plan["remaining_balance"] < lowest_book_price:
                if current_plan["plan_id"] == new_plan["id"]:
                    current_plan["remaining_balance"] = new_plan["plan_price"]
                    # Update the user membership list
                    for i, membership in enumerate(user_memberships):
                        if membership["user_id"] == user_id:
                            user_memberships[i] = current_plan
                            break
                    self.save_user_memberships(user_memberships)
                    print("Upgraded to the same plan due to insufficient balance.")
                    return

            # Update the current plan
            current_plan["remaining_balance"] = new_plan["plan_price"]
            current_plan["plan_name"] = new_plan["plan_name"]
            current_plan["plan_id"] = new_plan["id"]

            # Save the updated memberships
            for i, membership in enumerate(user_memberships):
                if membership["user_id"] == user_id:
                    user_memberships[i] = current_plan
                    break

            self.save_user_memberships(user_memberships)
            print(f"Membership plan upgraded successfully to '{new_plan['plan_name']}'!")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error during plan upgrade: {e}")



