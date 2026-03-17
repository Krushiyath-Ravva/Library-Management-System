from library_management.services import user_services,book_services,transaction_services
from library_management.utils.exceptions import UserNotFound,BookNotFound,WrongInputSelected,AuthenticationFailed
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
db_name = BASE_DIR / "library.db"

user_service = user_services.UserServices(db_file=db_name)
transaction_service = transaction_services.TransactionServices(db_file=db_name)
book_service = book_services.BookServices(db_file=db_name) 

LIBRARIAN_LOGIN = "LBM@123"

def start_program():
    print("---------------Welcome to Library Management System--------------")
    print("Here you can read books by borrowing ...")
    print("Select '1' to LogIn (If you are old User).")
    print("Select '2' to SignUp (If you are new User).")
    login = int(input("Select your Login Type based on the above data :- "))
    if login == 1:
        user_id = input("Enter your User ID to LogIn :- ")
        if user_service.is_student(user_id=user_id):
            print("Select '1' If you want to Borrow Book from Library.")
            print("Select '2' If you want to Return Book to Library.")
            stu_input = int(input("Select your Response based on the above data :- "))
            if stu_input == 1:
                show_books(user_id=user_id)
            elif stu_input == 2:
                print("Select '1' to Return Book with Transaction ID.")
                print("Select '2' to want to Get the Transaction ID.")
                return_choice = int(input("Select your Response based on the above data :- "))
                if return_choice == 1:
                    transaction_id = int(input("Enter Transaction Id to Return Book :- "))
                    if transaction_service.get_transaction_by_id(transaction_id=transaction_id):
                        return_book(transaction_id=transaction_id)
                if return_choice == 2:
                    get_transaction_by_user_id(user_id=input("Enter your User ID to get Transactions :- "))
                    print("Try Again with Entering Transaction ID to Return Book to Library.")
        elif user_service.is_librarian(user_id=user_id):
            if input("Enter the Librarian Password to LogIn :- ").upper() == LIBRARIAN_LOGIN:
                print("Select '1' If you want to Add Book to Library.")
                print("Select '2' If you want to Update Book Data in Library.")
                print("Select '3' If you want to Remove Book from Library.")
                librarian_choices = int(input("Select your Response based on the above data :- "))
                if librarian_choices == 1:
                    add_books(title=input("Enter Book Name :- "),author=input("Enter Author of the Book :- "),isbn=input("Enter ISBN Code of the Book :- "),available_copies=int(input("Enter the Number of Copies (Books) you are Adding :- ")))
                elif librarian_choices == 2:
                    book_id =int(input("Enter the Book ID :- "))
                    if get_one_book(book_id=book_id):
                        update_book(book_id=book_id,title=input("Enter Book Name :- "),author=input("Enter Author of the Book :- "),isbn=input("Enter ISBN Code of the Book :- "),available_copies=(input("Enter the Number of Copies (Books) you are Adding :- ")))
                elif librarian_choices == 3:
                    remove_book(book_id=int(input("Enter the Book ID :- ")))
            else:
                raise AuthenticationFailed()
        else:
            raise UserNotFound()    
    elif login == 2:
        print("Select '1' If you want to SignUp as an Student.")
        print("Select '2' If you want to SignUp as an Librarian.")
        signup_choice = int(input("Select your Response based on the above data :- "))
        if signup_choice == 1:
            add_user(name=input("Enter your Name :- "),email=input("Enter your Email :- "))
        elif signup_choice == 2:
            if input("Enter the Librarian Password to LogIn :- ").upper() == LIBRARIAN_LOGIN:
                add_librarian(name=input("Enter your Name :- "),email=input("Enter your Email :- "))
            else:
                raise AuthenticationFailed()
        else:
            raise WrongInputSelected()
    else:
        raise WrongInputSelected()
        
def show_books(user_id):
    books = book_service.get_all_books()
    print(f"ID \t Book Title \t \t Book Author \t \t Book ISBN Code \t Book Availability")
    for book in books:
        print(f"{book[0]} \t {book[1]} \t {book[2]} \t \t  {book[3]} \t \t {book[4]}")
    book_id = int(input("Enter the Book Id of the Borrowing Book :- "))
    if book_service.is_available(book_id=book_id):
        return borrow_book(user_id=user_id,book_id=book_id)
    else:
        raise BookNotFound("Book Not Available")

def add_user(name,email):
    user_service.register_student(name=name,email=email)

def add_librarian(name,email):
    user_service.register_librarian(name=name,email=email)

def borrow_book(user_id,book_id):
    id = transaction_service.borrow_book(user_id=user_id,book_id=book_id)
    return get_transaction_by_id(transaction_id=id)

def return_book(transaction_id):
    transaction_service.return_book(transaction_id=transaction_id)
    return get_transaction_by_id(transaction_id=transaction_id)

def get_transaction_by_id(transaction_id):
    transaction = transaction_service.get_transaction_by_id(transaction_id=transaction_id)
    print("ID \t User Id \t Book Id \t Borrowed Date \t \t Returned Date")
    print(f"{transaction[0]} \t {transaction[1]} \t \t {transaction[2]} \t {transaction[3]} \t {transaction[4]}")

def get_transaction_by_user_id(user_id):
    print("ID \t User Id \t Book Id \t Borrowed Date \t Returned Date")
    for transaction in transaction_service.get_transaction_by_user_id(user_id=user_id):
        print(f"{transaction[0]} \t {transaction[1]} \t \t {transaction[2]} \t {transaction[3]} \t {transaction[4]}")

def add_books(title , author , isbn , available_copies):
    book_service.add_book(title=title,author=author,isbn=isbn,available_copies=available_copies)

def update_book(book_id,title = None , author = None , isbn = None , available_copies = None):
    book = book_service.update_book(book_id=book_id,title=title,author=author,isbn=isbn,available_copies=available_copies)
    print(f"ID \t Book Title \t \t Book Author \t \t Book ISBN Code \t Book Availability")
    print(f"{book[0]} \t {book[1]} \t {book[2]} \t \t  {book[3]} \t \t {book[4]}")

def get_one_book(book_id):
    book = book_service.get_one_book(book_id=book_id)
    return book

def remove_book(book_id):
    book_service.remove_book(book_id=book_id)

if __name__ == "__main__":
    start_program()