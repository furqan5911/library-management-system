# User-Membership relationship entity


from datetime import datetime


class UserMembership:
    """
    Represents the association between a user and a membership plan.

    Attributes:
        id (int): Unique identifier for the user membership record.
        user_id (int): The ID of the associated user.
        membership_id (int): The ID of the associated membership plan.
        remaining_balance (float): The remaining balance of the user's membership.
        joined_date (datetime): The date when the user joined this membership plan.
    """

    def __init__(self, id, user_id, membership_id, remaining_balance, joined_date=None):
        self.id = id
        self.user_id = user_id
        self.membership_id = membership_id
        self.remaining_balance = remaining_balance
        self.joined_date = joined_date or datetime.now()

    def to_dict(self):
        """
        Converts the UserMembership object into a dictionary.
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "membership_id": self.membership_id,
            "remaining_balance": self.remaining_balance,
            "joined_date": self.joined_date.strftime("%Y-%m-%d %H:%M:%S"),
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a UserMembership object from a dictionary.
        """
        return UserMembership(
            id=data.get("id"),
            user_id=data.get("user_id"),
            membership_id=data.get("membership_id"),
            remaining_balance=data.get("remaining_balance"),
            joined_date=data.get("joined_date"),
        )
