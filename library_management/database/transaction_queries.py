import sqlite3
from library_management.database.db_connection import DBConnection
from library_management.database.book_queries import BookQueries

class TransactionQueries:
    def __init__(self,db_file):
        self.db_file = db_file
        self.db = DBConnection(db_file=self.db_file)
        self.connection = self.db.connect()
        self.cursor = self.connection.cursor()
        self.book_queries = BookQueries(self.db_file)
        self.create_table()

    def create_table(self):
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            book_id integer NOT NULL,
            borrowed_date TEXT NOT NULL,
            returned_date TEXT ,
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
            FOREIGN KEY (book_id) REFERENCES books (id) ON DELETE CASCADE 
            );"""
            self.cursor.execute(create_table_query)
            self.connection.commit()
        except Exception as e:
            print(e)

    def borrow_book(self, user_id , book_id , borrowed_date):
        try:
            book_presence = self.book_queries.get_book(book_id)
            if book_presence:
                if book_presence[4] > 0 :
                    borrow_book = """
                    INSERT INTO transactions (user_id , book_id , borrowed_date) VALUES (?,?,?);"""
                    self.cursor.execute(borrow_book, (user_id , book_id , borrowed_date))
                    self.connection.commit()
                    transaction_id = self.cursor.lastrowid
                    update_query = """
                    UPDATE books SET available_copies = available_copies - 1 WHERE id = ?;"""
                    self.cursor.execute(update_query , (book_id,))
                    self.connection.commit()
                    print(f"book ID {book_id} for the user {user_id} and the transaction id is {transaction_id}")
                    return transaction_id
                else:
                    print(f'The required Book Id :{book_id} is not available!!')
            else:
                print(f'The required Book Id :{book_id} is not available!!')
        except sqlite3.Error as e:
            print(f'Database Error : {e}')
            
    def return_book(self , transaction_id , returned_date):
        try:
            transaction = self.get_transaction_by_id(transaction_id)
            if transaction:
                book_id = transaction[2]
                return_query = """
                UPDATE transactions SET returned_date = ? where id = ?;
                """
                self.cursor.execute(return_query , (returned_date, transaction_id))
                self.connection.commit()
                update_query = """
                UPDATE books SET available_copies = available_copies + 1 WHERE id = ?;
                """
                self.cursor.execute(update_query , (book_id,))
                self.connection.commit()
                print(f'Books with ID {book_id} is returned on {returned_date}')
                return book_id,returned_date
            else:
                print(f'The transaction ID:{transaction_id} is not found ')
        except sqlite3.Error as e:
            print(f'Database Error: {e}')    

    def get_transaction_by_id(self , transaction_id):
        select_query = """
        SELECT * FROM transactions WHERE id = ?;"""
        self.cursor.execute(select_query , (transaction_id,))
        transaction = self.cursor.fetchone()
        return transaction
    
    def get_transaction_by_user_id(self , user_id):
        select_query = """
        SELECT * FROM transactions WHERE user_id = ?;
        """
        self.cursor.execute(select_query , (user_id,))
        transactions = self.cursor.fetchall()
        return transactions

    def close_connection(self):
        self.db.close()