# Membership file
from datetime import datetime

class Membership:
    def __init__(self, plan_name, plan_price, created_at=None):
        """
        Initialize a new Membership instance.

        :param plan_name: Name of the membership plan.
        :param plan_price: Price of the membership plan.
        :param created_at: Timestamp when the membership was created. Defaults to current time if not provided.
        """
        self.plan_name = plan_name
        self.plan_price = plan_price
        self.created_at = created_at if created_at else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """
        Convert the membership object to a dictionary.

        :return: A dictionary representation of the membership object.
        """
        return {
            "plan_name": self.plan_name,
            "plan_price": self.plan_price,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data):
        """
        Create a Membership object from a dictionary.

        :param data: A dictionary containing membership data.
        :return: A Membership instance created from the dictionary data.
        """
        return Membership(
            plan_name=data["plan_name"],
            plan_price=data["plan_price"],
            created_at=data["created_at"],
        )
