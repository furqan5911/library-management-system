# Membership_manager file
import json
from entities.membership import Membership


class MembershipManager:
    """
    A class to manage membership plans and user subscriptions.
    Attributes:
    -----------
    memberships_file : str
        The file path to the JSON file storing membership plans.
    user_plans_file : str
        The file path to the JSON file storing user plans.
    membership_plans : list
        A list to store membership plan objects.
    user_plans : dict
        A dictionary to store user plans with user email as the key.
    Methods:
    --------
    load_memberships_from_disk():
        Load membership plans from a JSON file.
    save_memberships_to_disk():
        Save the current membership plans to a JSON file.
    load_user_plans_from_disk():
        Load user plans from a JSON file.
    save_user_plans_to_disk():
        Save the current user plans to a JSON file.
    list_plans():
        List all available membership plans.
    purchase_plan(current_user, plan_name):
        Allow a user to purchase a membership plan.
    upgrade_plan(current_user, new_plan_name):
        Allow a user to upgrade their membership plan.
    create_plan(current_user, plan_name, plan_price):
        Allow an admin to create a new membership plan.
    update_plan(current_user, plan_name, new_price):
        Allow an admin to update the price of an existing membership plan.
    delete_plan(current_user, plan_name):
        Allow an admin to delete a membership plan.
    """
    def __init__(self, memberships_file="memberships.json", user_plans_file="user_plans.json"):
        self.memberships_file = memberships_file
        self.user_plans_file = user_plans_file
        self.membership_plans = []
        self.user_plans = {}

    def load_memberships_from_disk(self):
        """Load memberships from a JSON file."""
        try:
            with open(self.memberships_file, "r") as file:
                data = json.load(file)
                self.membership_plans = [Membership.from_dict(plan) for plan in data]
                print("Membership plans loaded successfully!")
        except FileNotFoundError:
            self.membership_plans = []
            print("No membership plans found. Starting fresh.")

    def save_memberships_to_disk(self):
        """Save the current membership plans to a JSON file."""
        with open(self.memberships_file, "w") as file:
            data = [plan.to_dict() for plan in self.membership_plans]
            json.dump(data, file, indent=4)
            print("Membership plans saved successfully!")

    def load_user_plans_from_disk(self):
        """Load user plans from a JSON file."""
        try:
            with open(self.user_plans_file, "r") as file:
                self.user_plans = json.load(file)
                print("User plans loaded successfully!")
        except FileNotFoundError:
            self.user_plans = {}
            print("No user plans found. Starting fresh.")

    def save_user_plans_to_disk(self):
        """Save the current user plans to a JSON file."""
        with open(self.user_plans_file, "w") as file:
            json.dump(self.user_plans, file, indent=4)
            print("User plans saved successfully!")

    def list_plans(self):
        """List all available membership plans (Accessible to all users)."""
        if not self.membership_plans:
            print("No membership plans available!")
        else:
            print("\n=== Available Membership Plans ===")
            for plan in self.membership_plans:
                print(f"- {plan.plan_name}: ${plan.plan_price}")

    def purchase_plan(self, current_user, plan_name):
        """Allow a user to purchase a membership plan (User-only)."""
        # Check if the plan exists
        plan = next((p for p in self.membership_plans if p.plan_name == plan_name), None)
        if not plan:
            print(f"Error: Membership plan '{plan_name}' does not exist.")
            return False

        # Check if the user already has the same plan
        if current_user.email in self.user_plans:
            current_plan = self.user_plans[current_user.email]
            if current_plan["plan_name"] == plan_name:
                if current_plan["plan_price"] >= 2:
                    print(f"Error: You already have the '{plan_name}' plan with a balance of ${current_plan['plan_price']}.")
                    print("You cannot purchase the same plan again unless the balance is zero.")
                    return False
                else:
                    print(f"You are repurchasing the '{plan_name}' plan because your current balance is zero.")

        # Assign the new plan to the user
        self.user_plans[current_user.email] = {
            "plan_name": plan.plan_name,
            "plan_price": plan.plan_price,
        }
        self.save_user_plans_to_disk()
        print(f"Membership plan '{plan.plan_name}' purchased successfully!")
        return True


    def upgrade_plan(self, current_user, new_plan_name):
        """Allow a user to upgrade their membership plan."""
        if current_user.email not in self.user_plans:
            print("Error: You need an existing membership plan to upgrade.")
            return False

        current_plan = self.user_plans[current_user.email]
        current_plan_name = current_plan["plan_name"]
        current_plan_price = current_plan["plan_price"]

        new_plan = next((p for p in self.membership_plans if p.plan_name == new_plan_name), None)
        if not new_plan:
            print(f"Error: Membership plan '{new_plan_name}' does not exist.")
            return False

        if new_plan.plan_price <= current_plan_price:
            print("Error: You cannot downgrade or select a plan at the same level.")
            return False

        upgrade_cost = new_plan.plan_price - current_plan_price
        print(f"Upgrading from '{current_plan_name}' to '{new_plan_name}'.")
        print(f"Additional Amount to Pay: ${upgrade_cost}")

        self.user_plans[current_user.email] = {
            "plan_name": new_plan.plan_name,
            "plan_price": new_plan.plan_price,
        }
        self.save_user_plans_to_disk()
        print(f"Membership plan upgraded to '{new_plan_name}' successfully!")
        return True

    def create_plan(self, current_user, plan_name, plan_price):
        if not current_user.is_admin():
            print("Error: Only admins can create membership plans.")
            return False
        if any(plan.plan_name == plan_name for plan in self.membership_plans):
            print(f"Error: Membership plan '{plan_name}' already exists!")
            return False
        new_plan = Membership(plan_name, plan_price)
        self.membership_plans.append(new_plan)
        self.save_memberships_to_disk()
        print(f"Membership plan '{plan_name}' created successfully!")
        return True

    def update_plan(self, current_user, plan_name, new_price):
        if not current_user.is_admin():
            print("Error: Only admins can update membership plans.")
            return False
        for plan in self.membership_plans:
            if plan.plan_name == plan_name:
                plan.plan_price = new_price
                self.save_memberships_to_disk()
                print(f"Membership plan '{plan_name}' updated successfully!")
                return True
        print(f"Error: Membership plan '{plan_name}' not found.")
        return False

    def delete_plan(self, current_user, plan_name):
        if not current_user.is_admin():
            print("Error: Only admins can delete membership plans.")
            return False
        self.membership_plans = [plan for plan in self.membership_plans if plan.plan_name != plan_name]
        self.save_memberships_to_disk()
        print(f"Membership plan '{plan_name}' deleted successfully!")

