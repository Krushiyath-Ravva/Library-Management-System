import sqlite3

class DBConnection:
    def __init__(self,db_file):
        self.db_file = db_file
        self.connection = None

    def connect(self):
        """Establishing Connection to the database"""
        try:
            self.connection = sqlite3.connect(self.db_file)
            self.connection.execute("PRAGMA foreign_keys = ON")
        except sqlite3.Error as e:
            print(f'From db_connection module Database Error: {e}')
        return self.connection

    def close(self):
        try:
            if self.connection:
                self.connection.close()
        except sqlite3.Error as e:
            print(f"From db_connection module Database Error: {e}")