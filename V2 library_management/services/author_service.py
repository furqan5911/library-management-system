# AuthorService class
from abstract_classes.base_service import BaseService
from entities.author import Author

class AuthorService(BaseService):
    """
    Handles author-related functionality such as adding, updating, deleting, and assigning books to authors.

    Methods:
        add_author(current_user, author_data): Adds a new author (Admin-only).
        update_author(current_user, author_id, updated_data): Updates author details (Admin-only).
        delete_author(current_user, author_id): Deletes an author (Admin-only).
        assign_book_to_author(current_user, author_id, book_id): Assigns a book to an author (Admin-only).
        list_authors(): Lists all authors.
    """
    def __init__(self, file_path):
        super().__init__(file_path)
        self.authors = self.load()

    def add_author(self, current_user, author_data):
        """
        Adds a new author to the system (Admin-only).

        :param current_user: The admin user adding the author.
        :param author_data: Dictionary containing author information.
        :return: The created Author object.
        """
        if not current_user.is_admin():
            raise PermissionError("Only admins can add authors.")
        return self.create(author_data)

    def update_author(self, current_user, author_id, updated_data):
        """
        Updates author details (Admin-only).

        :param current_user: The admin user updating the author.
        :param author_id: ID of the author to update.
        :param updated_data: Dictionary containing updated author details.
        :return: The updated Author object.
        """
        if not current_user.is_admin():
            raise PermissionError("Only admins can update authors.")
        return self.update(author_id, updated_data)

    def delete_author(self, current_user, author_id):
        """
        Deletes an author from the system (Admin-only).

        :param current_user: The admin user deleting the author.
        :param author_id: ID of the author to delete.
        :return: True if deletion was successful.
        """
        if not current_user.is_admin():
            raise PermissionError("Only admins can delete authors.")
        return self.delete(author_id)

    def assign_book_to_author(self, current_user, author_id, book_id):
        """
        Assigns a book to an author (Admin-only).

        :param current_user: The admin user assigning the book.
        :param author_id: ID of the author.
        :param book_id: ID of the book to assign.
        :return: The updated Author object.
        """
        if not current_user.is_admin():
            raise PermissionError("Only admins can assign books to authors.")
        author = self.find_by_id(author_id)
        if not author:
            raise ValueError(f"No author found with ID: {author_id}")
        if book_id in author["books"]:
            raise ValueError(f"Book ID {book_id} is already assigned to this author.")
        author["books"].append(book_id)
        return self.update(author_id, author)

    def list_authors(self):
        """
        Lists all authors in the system.

        :return: List of all authors.
        """
        return [Author.from_dict(author) for author in self.authors]
