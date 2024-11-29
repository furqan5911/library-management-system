# UserMembership entity

from datetime import datetime

class UserMembership:
    """
    Represents a User Membership entity.

    Attributes:
        user_id (str): Unique identifier for the user (e.g., email).
        plan_id (int): ID of the user's active membership plan.
        plan_name (str): Name of the user's active membership plan.
        remaining_balance (float): Remaining balance of the plan.
        purchase_date (str): Timestamp of when the membership was purchased.
    """

    def __init__(self, user_id, plan_id, plan_name, remaining_balance, purchase_date=None):
        self.user_id = user_id
        self.plan_id = plan_id
        self.plan_name = plan_name
        self.remaining_balance = remaining_balance
        self.purchase_date = purchase_date or datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    def to_dict(self):
        """
        Converts the UserMembership object into a dictionary for JSON storage.

        :return: Dictionary representation of the UserMembership object.
        """
        return {
            "user_id": self.user_id,
            "plan_id": self.plan_id,
            "plan_name": self.plan_name,
            "remaining_balance": self.remaining_balance,
            "purchase_date": self.purchase_date,
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a UserMembership object from a dictionary.

        :param data: Dictionary containing user membership data.
        :return: UserMembership object created from the dictionary data.
        """
        return UserMembership(
            user_id=data["user_id"],
            plan_id=data["plan_id"],
            plan_name=data["plan_name"],
            remaining_balance=data["remaining_balance"],
            purchase_date=data.get("purchase_date"),
        )
