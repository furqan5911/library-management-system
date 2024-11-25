# Author_manager file
import json
from entities.author import Author


class AuthorManager:
    """
    Manages a list of authors, including loading from and saving to a JSON file.
    Attributes:
        authors_file (str): The path to the JSON file containing author data.
        authors_list (list): A list of Author objects.
    Methods:
        load_authors_from_disk():
            Load authors from a JSON file.
        save_authors_to_disk():
            Save the current authors list to a JSON file.
        add_author(current_user, first_name, last_name, email):
            Add a new author (Admin-only).
        assign_book_to_author(current_user, email, book_title):
            Assign a book to an author (Admin-only).
        update_author(current_user, email, updated_data):
            Update an author's details (Admin-only).
        remove_author(current_user, email):
            Remove an author by email (Admin-only).
        list_authors():
            List all authors (Admin-only).
    """
    def __init__(self, authors_file="authors.json"):
        self.authors_file = authors_file
        self.authors_list = []

    def load_authors_from_disk(self):
        """Load authors from a JSON file."""
        try:
            with open(self.authors_file, "r") as file:
                data = json.load(file)
                self.authors_list = [Author.from_dict(author) for author in data]
                print("Authors loaded successfully!")
        except FileNotFoundError:
            self.authors_list = []
            print("No authors found. Starting fresh.")

    def save_authors_to_disk(self):
        """Save the current authors list to a JSON file."""
        with open(self.authors_file, "w") as file:
            data = [author.to_dict() for author in self.authors_list]
            json.dump(data, file, indent=4)
            print("Authors saved successfully!")

    def add_author(self, current_user, first_name, last_name, email):
        """Add a new author (Admin-only)."""
        if not current_user.is_admin():
            print("Error: Only admins can add authors.")
            return False
        if any(author.email == email for author in self.authors_list):
            print(f"Error: Author with email '{email}' already exists!")
            return False
        new_author = Author(first_name, last_name, email)
        self.authors_list.append(new_author)
        self.save_authors_to_disk()
        print(f"Author '{first_name} {last_name}' added successfully!")
        return True

    def assign_book_to_author(self, current_user, email, book_title):
        """Assign a book to an author (Admin-only)."""
        if not current_user.is_admin():
            print("Error: Only admins can assign books to authors.")
            return False
        for author in self.authors_list:
            if author.email == email:
                if author.book_title:
                    print(f"Error: Author '{author.first_name} {author.last_name}' already has a book assigned: '{author.book_title}'.")
                    return False
                author.assign_book(book_title)
                self.save_authors_to_disk()
                print(f"Book '{book_title}' assigned to author '{author.first_name} {author.last_name}'.")
                return True
        print(f"Error: Author with email '{email}' not found.")
        return False

    def update_author(self, current_user, email, updated_data):
        """Update an author's details (Admin-only)."""
        if not current_user.is_admin():
            print("Error: Only admins can update authors.")
            return False
        for author in self.authors_list:
            if author.email == email:
                for key, value in updated_data.items():
                    setattr(author, key, value)
                self.save_authors_to_disk()
                print(f"Author with email '{email}' updated successfully!")
                return True
        print(f"Error: Author with email '{email}' not found.")
        return False

    def remove_author(self, current_user, email):
        """Remove an author by email (Admin-only)."""
        if not current_user.is_admin():
            print("Error: Only admins can remove authors.")
            return False
        self.authors_list = [author for author in self.authors_list if author.email != email]
        self.save_authors_to_disk()
        print(f"Author with email '{email}' removed successfully!")

    def list_authors(self):
        """List all authors (Admin-only)."""
        if not self.authors_list:
            print("No authors available!")
        else:
            print("\n=== Author List ===")
            for author in self.authors_list:
                book_info = f"Assigned Book: {author.book_title}" if author.book_title else "No book assigned"
                print(f"- {author.first_name} {author.last_name} ({author.email}) | {book_info}")
