# Base repository class
# Base repository class

import psycopg2
from psycopg2.errors import ProgrammingError


class BaseRepository:
    """
    Abstract base class for managing common database operations.
    This class should be extended by specific repository classes for each entity.
    """

    def __init__(self, db_client, table_name):
        """
        Initialize the repository with a database client and table name.
        
        :param db_client: A database connection client provided by DatabaseConnectionManager.
        :param table_name: The name of the database table associated with the repository.
        """
        self.db_client = db_client
        self.table_name = table_name

    def create_table(self, schema):
        """
        Create the table if it doesn't exist.
        
        :param schema: SQL schema definition for creating the table.
        """
        try:
            with self.db_client.cursor() as cursor:
                cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} ({schema});")
                self.db_client.commit()
                print(f"Table '{self.table_name}' ensured.")
        except ProgrammingError as e:
            print(f"Error creating table {self.table_name}: {e}")
            self.db_client.rollback()
        except Exception as e:
            print(f"Unexpected error while creating table {self.table_name}: {e}")
            self.db_client.rollback()

    def insert(self, data):
        """
        Insert a new record into the table.
        
        :param data: A dictionary of column-value pairs to insert.
        :return: The ID of the inserted record.
        """
        try:
            columns = ", ".join(data.keys())
            values = ", ".join([f"%({key})s" for key in data.keys()])
            query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({values}) RETURNING id;"
            
            with self.db_client.cursor() as cursor:
                cursor.execute(query, data)
                self.db_client.commit()
                return cursor.fetchone()["id"]
        except Exception as e:
            print(f"Error inserting data into {self.table_name}: {e}")
            self.db_client.rollback()

    def update(self, id, data):
        """
        Update a record by ID.
        
        :param id: The ID of the record to update.
        :param data: A dictionary of column-value pairs to update.
        """
        try:
            set_clause = ", ".join([f"{key} = %({key})s" for key in data.keys()])
            query = f"UPDATE {self.table_name} SET {set_clause} WHERE id = %(id)s;"
            data["id"] = id

            with self.db_client.cursor() as cursor:
                cursor.execute(query, data)
                self.db_client.commit()
        except Exception as e:
            print(f"Error updating record {id} in {self.table_name}: {e}")
            self.db_client.rollback()

    def delete(self, id):
        """
        Delete a record by ID.
        
        :param id: The ID of the record to delete.
        """
        try:
            query = f"DELETE FROM {self.table_name} WHERE id = %s;"
            with self.db_client.cursor() as cursor:
                cursor.execute(query, (id,))
                self.db_client.commit()
        except Exception as e:
            print(f"Error deleting record {id} from {self.table_name}: {e}")
            self.db_client.rollback()

    def find_by_id(self, id):
        """
        Retrieve a record by ID.
        
        :param id: The ID of the record to retrieve.
        :return: A dictionary representing the record, or None if not found.
        """
        try:
            query = f"SELECT * FROM {self.table_name} WHERE id = %s;"
            with self.db_client.cursor() as cursor:
                cursor.execute(query, (id,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving record {id} from {self.table_name}: {e}")

    def list_all(self):
        """
        Retrieve all records from the table.
        
        :return: A list of dictionaries representing all records.
        """
        try:
            query = f"SELECT * FROM {self.table_name};"
            with self.db_client.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error listing records from {self.table_name}: {e}")
