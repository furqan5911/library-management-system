# Transaction_manager file


import json
from entities.transaction import BooksTransaction


class BooksTransactionManager:
    def __init__(self, transactions_file="transactions.json", user_plans_file="user_plans.json", books_file="books.json"):
        self.transactions_file = transactions_file
        self.user_plans_file = user_plans_file
        self.books_file = books_file
        self.transactions_list = []
        self.user_plans = {}
        self.books_list = []

    def load_data_from_disk(self):
        """Load transactions, user plans, and books from JSON files."""
        try:
            with open(self.transactions_file, "r") as file:
                self.transactions_list = [BooksTransaction.from_dict(tx) for tx in json.load(file)]
            print("Transactions loaded successfully!")
        except FileNotFoundError:
            self.transactions_list = []
            print("No transactions found. Starting fresh.")

        try:
            with open(self.user_plans_file, "r") as file:
                self.user_plans = json.load(file)
            print("User plans loaded successfully!")
        except FileNotFoundError:
            self.user_plans = {}
            print("No user plans found. Starting fresh.")

        try:
            with open(self.books_file, "r") as file:
                self.books_list = json.load(file)
            print("Books loaded successfully!")
        except FileNotFoundError:
            self.books_list = []
            print("No books found. Starting fresh.")

    def save_data_to_disk(self):
        """Save transactions, user plans, and books to JSON files."""
        with open(self.transactions_file, "w") as file:
            json.dump([tx.to_dict() for tx in self.transactions_list], file, indent=4)
            print("Transactions saved successfully!")

        with open(self.user_plans_file, "w") as file:
            json.dump(self.user_plans, file, indent=4)
            print("User plans saved successfully!")

        with open(self.books_file, "w") as file:
            json.dump(self.books_list, file, indent=4)
            print("Books saved successfully!")

    def record_transaction(self, current_user, book_title):
        """Record a new book transaction for a user."""
        if current_user.email not in self.user_plans:
            print("Error: You need to purchase a membership plan before making transactions.")
            return False

        # Check if the book exists
        book = next((book for book in self.books_list if book["title"] == book_title), None)
        if not book:
            print(f"Error: Book '{book_title}' not found.")
            return False

        # Check if the book price is valid
        if book["price"] > 5:
            print("Error: Book price must be greater than $5.")
            return False

        # Check if the user has sufficient balance
        user_plan = self.user_plans[current_user.email]
        if user_plan["plan_price"] < book["price"]:
            print(f"Error: Insufficient balance. Your current balance is ${user_plan['plan_price']}.")
            return False

        # Check if the user already purchased the book
        if any(tx.user_email == current_user.email and tx.book_title == book_title for tx in self.transactions_list):
            print(f"Error: You have already purchased the book '{book_title}'.")
            return False

        # Deduct the price from the user's plan and record the transaction
        user_plan["plan_price"] -= book["price"]
        self.user_plans[current_user.email] = user_plan  # Update the user's plan with the new balance
        self.transactions_list.append(BooksTransaction(current_user.email, book_title, price=book["price"]))

        # Remove the book from the available books list
        self.books_list = [b for b in self.books_list if b["title"] != book_title]

        # Save all data
        self.save_data_to_disk()

        print(f"Transaction successful! You purchased '{book_title}' for ${book['price']}. Remaining balance: ${user_plan['plan_price']}.")
        return True

    def list_user_transactions(self, current_user):
        """List all transactions for the logged-in user."""
        user_transactions = [tx for tx in self.transactions_list if tx.user_email == current_user.email]
        if not user_transactions:
            print("No transactions found.")
        else:
            print("\n=== Your Transactions ===")
            for tx in user_transactions:
                print(f"- {tx.book_title}: ${tx.price} (Purchased on {tx.transaction_date})")
