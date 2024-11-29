# AuthorService class
from abstract_classes.base_service import BaseService
from entities.author import Author
import json

class AuthorService(BaseService):
    """
    Handles author-related functionality such as adding, updating, deleting, and assigning books to authors.
    """

    def __init__(self, file_path):
        super().__init__(file_path)
        try:
            self.authors = self.load()
        except Exception as e:
            print(f"Error loading authors: {e}")
            self.authors = []

    def save(self):
        """
        Saves the list of authors to the file.
        """
        try:
            with open(self.file_path, "w") as file:
                json.dump([author.to_dict() if isinstance(author, Author) else author for author in self.authors], file, indent=4)
                print("Authors saved successfully!")
        except Exception as e:
            print(f"Error saving authors: {e}")

    def add_author(self, current_user, author_data, source="author_menu"):
        """
        Adds a new author to the system (Admin-only).
        Tracks if the author is added via the book adding process or the author menu.
        """
        try:
            if not current_user.is_admin():
                raise PermissionError("Only admins can add authors.")

            # Check if the author already exists
            existing_author = next(
                (Author.from_dict(author) for author in self.authors if author["first_name"] == author_data["first_name"] and author["last_name"] == author_data["last_name"]),
                None
            )
            if existing_author:
                print(f"Author '{author_data['first_name']} {author_data['last_name']}' already exists.")
                return existing_author

            # If author doesn't exist, create a new one
            new_author = Author(
                id=self.get_next_id(self.authors),
                first_name=author_data["first_name"],
                last_name=author_data["last_name"],
                email=author_data["email"]
            )
            self.authors.append(new_author.to_dict())  # Append as a dictionary

            self.save()  # Save the author list to file
            print(f"Author '{author_data['first_name']} {author_data['last_name']}' added successfully!")

            if source == "book_menu":
                print("Author added via book menu.")

            return new_author  # Return the `Author` object
        except PermissionError as e:
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error while adding author: {e}")
            return None

    def list_authors(self):
        """
        Lists all authors in the system.
        """
        try:
            return [Author.from_dict(author) if isinstance(author, dict) else author for author in self.authors]
        except Exception as e:
            print(f"Error while listing authors: {e}")
            return []

    def get_next_id(self, authors):
        """
        Helper function to get the next available author ID.
        """
        if authors:
            return max(author["id"] if isinstance(author, dict) else author.id for author in authors) + 1
        return 1

    def update_author(self, current_user, author_id, updated_data):
        """
        Updates author details (Admin-only).
        """
        try:
            if not current_user.is_admin():
                raise PermissionError("Only admins can update authors.")
            return self.update(author_id, updated_data)
        except PermissionError as e:
            print(f"Error: {e}")
            return None
        except ValueError as e:
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error while updating author: {e}")
            return None

    def delete_author(self, current_user, author_id):
        """
        Deletes an author from the system (Admin-only).
        """
        try:
            if not current_user.is_admin():
                raise PermissionError("Only admins can delete authors.")
            return self.delete(author_id)
        except PermissionError as e:
            print(f"Error: {e}")
            return False
        except ValueError as e:
            print(f"Error: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error while deleting author: {e}")
            return False

    def assign_book_to_author(self, current_user, author_id, book_id):
        """
        Assigns a book to an author (Admin-only).
        """
        try:
            if not current_user.is_admin():
                raise PermissionError("Only admins can assign books to authors.")
            author = self.find_by_id(author_id)
            if not author:
                raise ValueError(f"No author found with ID: {author_id}")
            if book_id in author.get("books", []):
                raise ValueError(f"Book ID {book_id} is already assigned to this author.")
            author.setdefault("books", []).append(book_id)
            return self.update(author_id, author)
        except PermissionError as e:
            print(f"Error: {e}")
            return None
        except ValueError as e:
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error while assigning book: {e}")
            return None


