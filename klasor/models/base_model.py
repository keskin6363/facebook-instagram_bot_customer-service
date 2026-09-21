from database.db_connection import DBConnection

class BaseModel:
    def __init__(self):
        self.db = DBConnection()

    def get_connection(self):
        return self.db.get_connection()