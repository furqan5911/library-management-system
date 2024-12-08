# Base service class


class BaseService:
    """
    Abstract base class for common service functionality.
    This class should be extended by specific service classes for each entity.
    """

    def __init__(self):
        pass

    @staticmethod
    def validate_required_fields(data, required_fields):
        """
        Validates that all required fields are present in the data.

        :param data: The dictionary of input data to validate.
        :param required_fields: A list of required field names.
        :return: True if all fields are present, False otherwise.
        """
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
        return True

    @staticmethod
    def map_to_entity(entity_class, data):
        """
        Maps a dictionary to an entity class.

        :param entity_class: The entity class to map data to.
        :param data: The dictionary containing entity data.
        :return: An instance of the entity class.
        """
        return entity_class.from_dict(data)

    @staticmethod
    def handle_error(action, error):
        """
        Handles and logs errors for service methods.

        :param action: The action being performed (e.g., "adding book").
        :param error: The error that occurred.
        """
        print(f"Error {action}: {error}")
