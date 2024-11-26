# Abstract StorageManager class
import json

class StorageManager:
    """
    Abstract class to handle data persistence for services.

    Attributes:
        file_path (str): Path to the file where data is stored.
    """
    def __init__(self, file_path):
        """
        Initialize with the file path.

        :param file_path: Path to the JSON file for data storage.
        """
        self.file_path = file_path

    def load_data(self):
        """
        Load data from the file.

        :return: List of data objects or an empty list if the file does not exist.
        """
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []  # Return empty list if the file does not exist

    def save_data(self, new_data):
        """
        Save new data to the file. Avoid duplicates by checking IDs.

        :param new_data: Dictionary containing the new data.
        """
        all_data = self.load_data()
        if any(item["id"] == new_data["id"] for item in all_data):
            raise ValueError(f"Duplicate ID detected: {new_data['id']}")
        all_data.append(new_data)
        with open(self.file_path, "w") as file:
            json.dump(all_data, file, indent=4)

    def update_data(self, updated_object):
        """
        Update an existing record in the file.

        :param updated_object: Dictionary containing updated data.
        """
        all_data = self.load_data()
        updated = False
        for index, item in enumerate(all_data):
            if item["id"] == updated_object["id"]:
                all_data[index] = updated_object
                updated = True
                break
        if not updated:
            raise ValueError(f"No record found with ID: {updated_object['id']}")
        with open(self.file_path, "w") as file:
            json.dump(all_data, file, indent=4)
