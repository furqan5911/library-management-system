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
        print("2. Add Membership Plan")  # New Option
        print("3. Update Membership Plan") 
        print("4. Delete Membership Plan")
        print("0. Go Back")
        print_separator()
        choice = input("Enter your choice: ")

        if choice == "1":
            list_memberships(membership_service)
        elif choice == "2":
            add_membership(membership_service)  # Call new function
        elif choice == "3":
            update_membership(membership_service)  # Call new function
        elif choice == "4":
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

def add_membership(membership_service: MembershipService):
    """
    Adds a new membership plan.
    """
    print("\n=== Add Membership Plan ===")
    plan_name = input("Enter Plan Name: ").strip()
    plan_price = input("Enter Plan Price: ").strip()
    try:
        plan_price = float(plan_price)
        data = {"plan_name": plan_name, "plan_price": plan_price}
        result = membership_service.add_membership(data)
        if isinstance(result, dict):
            print(f"Membership plan '{result['plan_name']}' added successfully!")
        else:
            print(result)  # Error message if already exists
    except ValueError:
        print("Invalid price. Please enter a numeric value.")
    except Exception as e:
        print(f"An error occurred: {e}")


def update_membership(membership_service: MembershipService):
    """
    Updates an existing membership plan.
    """
    print("\n=== Update Membership Plan ===")
    membership_id = input("Enter Membership ID to update: ").strip()
    try:
        membership_id = int(membership_id)
        plan_price = input("Enter New Plan Price: ").strip()
        plan_price = float(plan_price)
        data = {"plan_price": plan_price}
        success = membership_service.update_membership(membership_id, data)
        if success:
            print("Membership plan updated successfully!")
        else:
            print("Failed to update membership plan. Please ensure the ID is correct.")
    except ValueError:
        print("Invalid input. Please ensure the ID is a number and the price is numeric.")
    except Exception as e:
        print(f"An error occurred: {e}")
