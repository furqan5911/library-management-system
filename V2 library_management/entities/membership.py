# Membership entity
from datetime import datetime

class Membership:
    """
    Represents a Membership entity in the system.

    Attributes:
        id (int): Unique identifier for the membership plan.
        plan_name (str): Name of the membership plan.
        plan_price (float): Price of the membership plan.
        created_at (str): Date and time when the membership plan was created.
    """
    def __init__(self, id, plan_name, plan_price):
        self.id = id
        self.plan_name = plan_name
        self.plan_price = plan_price
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """
        Converts the Membership object into a dictionary for JSON storage.

        :return: Dictionary representation of the Membership object.
        """
        return {
            "id": self.id,
            "plan_name": self.plan_name,
            "plan_price": self.plan_price,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Membership object from a dictionary.

        :param data: Dictionary containing membership data.
        :return: Membership object created from the dictionary data.
        """
        return Membership(
            id=data["id"],
            plan_name=data["plan_name"],
            plan_price=data["plan_price"],
        )
