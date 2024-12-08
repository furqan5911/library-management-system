# Membership entity
# Membership entity

from datetime import datetime


class Membership:
    """
    Represents a membership plan in the library system.

    Attributes:
        id (int): The unique identifier for the membership plan.
        plan_name (str): The name of the membership plan.
        plan_price (float): The price of the membership plan.
        created_at (datetime): The creation date of the membership plan.
    """

    def __init__(self, id, plan_name, plan_price, created_at=None):
        self.id = id
        self.plan_name = plan_name
        self.plan_price = plan_price
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        """
        Converts the Membership object into a dictionary.
        """
        return {
            "id": self.id,
            "plan_name": self.plan_name,
            "plan_price": self.plan_price,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Membership object from a dictionary.
        """
        return Membership(
            id=data.get("id"),
            plan_name=data.get("plan_name"),
            plan_price=data.get("plan_price"),
            created_at=data.get("created_at"),
        )
