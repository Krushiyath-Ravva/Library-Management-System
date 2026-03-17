import sqlite3
from library_management.database.db_connection import DBConnection

class UserQueries:
    def __init__(self,db_file):
        self.db_file = db_file
        # CREATING AN OBJECT FOR THE CLASS PRESENT IN THE db_connection.py file
        self.db = DBConnection(db_file=self.db_file)
        # Connecting the database with respect to the object
        self.connection = self.db.connect()
        #After connecting the cursor will point to one specific operation to be performed
        self.cursor = self.connection.cursor()
        # TO jump from next step which is creating table 
        self.create_table()

    def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        role TEXT NOT NULL,
        user_id TEXT UNIQUE );"""
        self.cursor.execute(create_table_query)
        self.connection.commit()
#By using this method we will generate a user_id by like "STPY01" if he is student, name is python and id is 01
    def generate_user_id(self,id,username,role):
        role_prefix = 'ST' if role.lower() == 'student' else 'LB'
        user_char  = username[:2].upper()
        row_id = f"{id:02d}"
        return f"{role_prefix}{user_char}{row_id}"

    def add_user(self,username,email,role):
        try:
            insert_query = """
            INSERT INTO users (name,email,role) VALUES (?,?,?);"""
            self.cursor.execute(insert_query,(username,email,role))
            self.connection.commit()
#After we execute the insert statement ,the cursor.lastrowid will contain/point towards the newly inserted row.
#When we want to retrive the newly/recently created row`s id then we will use this lastrowid
            id = self.cursor.lastrowid
#Here generate_user_id() will take the arguments and return the generated user id , which is stored in variable.
            generated_user_id =  self.generate_user_id(id,username,role)
#Initially user_id value is NULL ,so we are updating the user user id by UPDATE querry
            update_user_id = """
            UPDATE users set user_id = ? WHERE id = ?;"""
            self.cursor.execute(update_user_id,(generated_user_id,id))
            self.connection.commit()
            print(f"Data added for the user {username} and user_id is {generated_user_id}")
            return generated_user_id
        except sqlite3.Error as e:
            print(f"From user_queries module Database Error: {e}")

    def get_user_by_id(self,user_id):
        select_query = """
        SELECT * FROM users WHERE user_id = ?;
        """
        self.cursor.execute(select_query,(user_id,))
        data = self.cursor.fetchone()
        if data:
            return data
        else:
            print(f"DATANOTFOUND : ENTERED USER_ID {user_id} DOES NOT CONTAIN ANY DATA--")
            return

    def close_connection(self):
        self.db.close()