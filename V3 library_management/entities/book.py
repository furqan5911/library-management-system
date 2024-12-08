# Book entity


class Book:
    """
    Represents a book entity in the library system.

    Attributes:
        id (int): The unique identifier for the book.
        title (str): The title of the book.
        author_id (int): The ID of the book's author.
        category_id (int): The ID of the book's category.
        publication_date (str): The publication date of the book.
        price (float): The price of the book.
        isbn (str): The ISBN number of the book.
        is_sold (bool): Whether the book is sold or available.
    """

    def __init__(self, id, title, author_id, category_id, publication_date, price, isbn, is_sold=False):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.category_id = category_id
        self.publication_date = publication_date
        self.price = price
        self.isbn = isbn
        self.is_sold = is_sold

    def to_dict(self):
        """
        Converts the Book object into a dictionary.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author_id": self.author_id,
            "category_id": self.category_id,
            "publication_date": self.publication_date,
            "price": self.price,
            "isbn": self.isbn,
            "is_sold": self.is_sold
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Book object from a dictionary.
        """
        return Book(
            id=data["id"],
            title=data["title"],
            author_id=data["author_id"],
            category_id=data["category_id"],
            publication_date=data["publication_date"],
            price=data["price"],
            isbn=data["isbn"],
            is_sold=data.get("is_sold", False)
        )
