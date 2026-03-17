import sqlite3
from library_management.database.db_connection import DBConnection

class BookQueries:
    def __init__(self,db_file):
        self.db_file = db_file
        self.db = DBConnection(db_file=self.db_file)
        self.connection = self.db.connect()
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        isbn TEXT UNIQUE NOT NULL,
        available_copies INTEGER NOT NULL);"""
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def add_book(self,title,author,isbn,available_copies):
        try:
            add_book_query = """
            INSERT INTO books (title,author,isbn,available_copies) VALUES (?,?,?,?);"""
            self.cursor.execute(add_book_query,(title,author,isbn,available_copies))
            self.connection.commit()
            book_id = self.cursor.lastrowid
            print(f"book with ID :{book_id} added Successfully!!!")
            return book_id
        except sqlite3.Error as e:
            print(f"Database Error: {e}")

    def update_book(self,book_id,title = None , author = None , isbn = None , available_copies = None):
        if self.get_book(book_id):
            update_fields = []
            values = []
            if title:
                update_fields.append("title = ?")
                values.append(title)
            if author:
                update_fields.append("author = ?")
                values.append(author)
            if isbn:
                update_fields.append("isbn = ?")
                values.append(isbn)
            if available_copies:
                update_fields.append("available_copies = ?")
                values.append(available_copies)
            if not update_fields:
                print("You have not provided any fields to uopdate")
            update_query = f"UPDATE books SET {(', '.join(update_fields))} WHERE id = ?;"
            values.append(book_id)
            try:
                self.cursor.execute(update_query, tuple(values))
                self.connection.commit()
                print(f"Changes have been done successfully on book Id:{book_id}. ")
                return book_id
            except sqlite3.Error as e:
                print(f"database Error: {e}")
        else:
            print(f'The Book with Book Id {book_id} is not present in our database')

    def get_book(self,book_id):
        try:
            select_query = """
            SELECT * FROM books where id = ?;"""
            self.cursor.execute(select_query , (book_id,))
            book = self.cursor.fetchone()
            return book
        except sqlite3.Error as e:
            print(f"Database Error : {e}")

    def get_all_books(self):
        try:
            select_query = """
                    SELECT * FROM books;
                    """
            self.cursor.execute(select_query)
            books = self.cursor.fetchall()
            return books
        except sqlite3.Error as e:
             print(f'Database Error : {e}')

    def remove_book(self, book_id):
        try:
            remove_query = """
            DELETE FROM books WHERE id = ?;"""
            self.cursor.execute(remove_query , (book_id,))
            self.connection.commit()
            print(f'Book with id : {book_id} removed')
            return book_id
        except sqlite3.Error as e:
            print(f"Database Error : {e}")

    def close_connection(self):
        self.db.close()