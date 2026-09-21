import mysql.connector

class DBConnection:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""  # Şifre yoksa burayı tamamen boş bırak (tırnaklar kalsın)
        self.database = "bot_db"

    def get_connection(self):
        return mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.database)