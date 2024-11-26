def membership_menu(admin, membership_service):
    """
    Menu for managing memberships (Admin only).
    """
    while True:
        print("\n=== Manage Membership Plans ===")
        print("1. Add Membership Plan")
        print("2. Update Membership Plan")
        print("3. Delete Membership Plan")
        print("4. List All Membership Plans")
        print("0. Go Back")
        choice = input("Enter your choice: ")

        if choice == "1":
            plan_name = input("Enter plan name: ")
            plan_price = float(input("Enter plan price: "))
            membership_service.add_plan(admin, {"plan_name": plan_name, "plan_price": plan_price})
            print("Membership plan added successfully!")
        elif choice == "2":
            plan_id = int(input("Enter plan ID to update: "))
            new_price = float(input("Enter new plan price: "))
            membership_service.update_plan(admin, plan_id, {"plan_price": new_price})
            print("Membership plan updated successfully!")
        elif choice == "3":
            plan_id = int(input("Enter plan ID to delete: "))
            membership_service.delete_plan(admin, plan_id)
            print("Membership plan deleted successfully!")
        elif choice == "4":
            plans = membership_service.list_plans()
            print("\n=== Membership Plans ===")
            for plan in plans:
                print(f"- {plan.plan_name}: ${plan.plan_price}")
        elif choice == "0":
            print("Returning to Admin Dashboard...")
            return
        else:
            print("Invalid choice! Please try again.")
