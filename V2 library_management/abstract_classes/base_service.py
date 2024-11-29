# Abstract BaseService class
import json
from abstract_classes.storage_manager import StorageManager

class BaseService:
    """
    A base class for all service classes to handle CRUD operations.
    
    Attributes:
        file_path (str): Path to the file where data is stored.
        storage_manager (StorageManager): Instance of StorageManager to handle file operations.
        id_tracker (int): Keeps track of the next ID for new records.
    """
    def __init__(self, file_path):
        """
        Initialize BaseService with the file path and set up StorageManager.
        
        :param file_path: Path to the JSON file for data storage.
        """
        self.file_path = file_path
        self.storage_manager = StorageManager(file_path)
        self.id_tracker = None  # Track the next available ID

    def load(self):
        """
        Load all data from the file and initialize the ID tracker.
        """
        data = self.storage_manager.load_data()
        if data:
            self.id_tracker = max(item["id"] for item in data) + 1
        else:
            self.id_tracker = 1
        return data

    def create(self, data):
        """
        Add a new record to the data file.
        
        :param data: Dictionary containing new record data.
        :return: The newly created record.
        """
        if self.id_tracker is None:
            self.load()  # Initialize id_tracker if not already done
        data["id"] = self.id_tracker
        self.storage_manager.save_data(data)
        self.id_tracker += 1
        return data

    def find(self, query):
        """
        Find records that match the query.
        
        :param query: Dictionary with key-value pairs to match.
        :return: List of records that match the query.
        """
        data = self.load()
        return [item for item in data if all(item[key] == value for key, value in query.items())]

    def find_one_by_q(self, key, value):
        """
        Find a single record by a key-value pair.
        
        :param key: The key to search by.
        :param value: The value to match.
        :return: The first matching record or None.
        """
        data = self.load()
        return next((item for item in data if item.get(key) == value), None)

    def find_by_id(self, id):
        """
        Find a single record by ID.
        
        :param id: The ID to search for.
        :return: The record with the matching ID or None.
        """
        return self.find_one_by_q("id", id)

    def update(self, id, updated_data):
        """
        Update an existing record by ID.
        
        :param id: The ID of the record to update.
        :param updated_data: Dictionary with updated key-value pairs.
        :return: The updated record.
        """
        try:
            data = self.load()
            for item in data:
                if item["id"] == id:
                    item.update(updated_data)
                    self.storage_manager.update_data(item)
                    return item
        except ValueError as e:
            print(e)
            return False  # Ensure the method gracefully handles the error
       
    

    def delete(self, id):
        """
        Delete a record by ID.

        :param id: The ID of the record to delete.
        :return: True if the record was deleted, False otherwise.
        """
        try:
            data = self.load()
            updated_data = [item for item in data if item["id"] != id]
            if len(updated_data) == len(data):
                raise ValueError(f"No record found with ID: {id}")
            with open(self.file_path, "w") as file:
                json.dump(updated_data, file, indent=4)
            print(f"Record with ID {id} deleted successfully.")
            return True
        except ValueError as e:
            print(e)
            return False  # Ensure the method gracefully handles the error


