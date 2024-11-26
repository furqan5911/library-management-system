from utils.admin_menus import admin_dashboard
from utils.user_menus import user_dashboard


def handle_admin_menu(admin, user_service, book_service, author_service, category_service, membership_service):
    """
    Handles the admin menu by delegating to the admin dashboard.
    """
    admin_dashboard(admin, user_service, book_service, author_service, category_service, membership_service)


def handle_user_menu(user, book_service, membership_service, transaction_service):
    """
    Handles the user menu by delegating to the user dashboard.
    """
    user_dashboard(user, book_service, membership_service, transaction_service)
