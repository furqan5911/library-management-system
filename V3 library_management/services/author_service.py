# Service class for Author operations

# Service class for Author operations

from repositories.author_repository import AuthorRepository
from entities.author import Author
from services.base_service import BaseService


class AuthorService(BaseService):
    """
    Service class for managing authors in the library system.
    """

    def __init__(self, db_client):
        """
        Initializes the AuthorService with a database client.
        """
        super().__init__()
        self.author_repo = AuthorRepository(db_client)

    def add_author(self, data):
        """
        Adds a new author to the library system.

        :param data: Dictionary containing author details (first_name, last_name, email).
        :return: The created or existing author as a dictionary.
        """
        try:
            self.validate_required_fields(data, ["first_name", "last_name", "email"])

            # Check if the author already exists
            existing_author = self.author_repo.find_by_email(data["email"])
            if existing_author:
                print(f"Author with email {data['email']} already exists.")
                return self.map_to_entity(Author, existing_author).to_dict()

            # Add new author
            author_id = self.author_repo.add_author(data)
            return Author(author_id, data["first_name"], data["last_name"], data["email"]).to_dict()
        except Exception as e:
            self.handle_error("adding author", e)
            return None

    def list_authors(self):
        """
        Lists all authors in the system.

        :return: A list of Author entities as dictionaries.
        """
        try:
            authors = self.author_repo.list_authors()
            return [self.map_to_entity(Author, author).to_dict() for author in authors]
        except Exception as e:
            self.handle_error("listing authors", e)
            return []

    def find_author_by_email(self, email):
        """
        Finds an author by their email.

        :param email: The email of the author.
        :return: The author as a dictionary, or None if not found.
        """
        try:
            author = self.author_repo.find_by_email(email)
            return self.map_to_entity(Author, author).to_dict() if author else None
        except Exception as e:
            self.handle_error("finding author by email", e)
            return None

    def delete_author(self, author_id):
        """
        Deletes an author from the library system.

        :param author_id: The ID of the author to delete.
        :return: True if successful, False otherwise.
        """
        try:
            return self.author_repo.delete(author_id)
        except Exception as e:
            self.handle_error("deleting author", e)
            return False


