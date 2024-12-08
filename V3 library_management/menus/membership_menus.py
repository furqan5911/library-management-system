# Membership menu options

from services.membership_service import MembershipService
from utils.helpers import print_separator


def manage_memberships(membership_service: MembershipService):
    """
    Menu for managing memberships.
    """
    while True:
        print_separator()
        print("\n=== Manage Memberships ===")
        print("1. List All Membership Plans")
        print("2. Delete Membership Plan")
        print("0. Go Back")
        print_separator()
        choice = input("Enter your choice: ")

        if choice == "1":
            list_memberships(membership_service)
        elif choice == "2":
            delete_membership(membership_service)
        elif choice == "0":
            print("Returning to Admin Dashboard...")
            break
        else:
            print("Invalid choice! Please try again.")


def list_memberships(membership_service: MembershipService):
    """
    Lists all membership plans.
    """
    memberships = membership_service.list_memberships()
    if memberships:
        print("\n=== Membership Plans ===")
        for membership in memberships:
            print(f"ID: {membership['id']}, Name: {membership['plan_name']}, Price: ${membership['plan_price']}")
    else:
        print("No membership plans found.")


def delete_membership(membership_service: MembershipService):
    """
    Deletes a membership plan by its ID.
    """
    membership_id = input("Enter Membership ID to delete: ").strip()
    try:
        membership_id = int(membership_id)
        if membership_service.delete_membership(membership_id):
            print("Membership plan deleted successfully.")
        else:
            print("Failed to delete membership plan.")
    except ValueError:
        print("Invalid Membership ID.")
