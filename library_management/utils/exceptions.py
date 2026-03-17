class LibraryError(Exception):
    pass

class UserAlreadyExists(LibraryError):
    def __init__(self , message='User already exists'):
        self.message = message
        super().__init__(message)

class UserNotFound(LibraryError):
    def __init__(self , message = 'User not found'):
        self.message = message
        super().__init__(message)

class BookNotFound(LibraryError):
    def __init__(self , message = 'Book not Found'):
        self.message = message
        super().__init__(message)

class DuplicateBookISBNError(LibraryError):
    def __init__(self , message = 'Book Already Exists'):
        self.message = message
        super().__init__(message)

class TransactionNotFound(LibraryError):
    def __init__(self , message = 'Transaction not Found'):
        self.message = message
        super().__init__(message)

class AuthenticationFailed(LibraryError):
    def __init__(self,message = "Wrong Password Entered "):
        super().__init__(message)

class WrongInputSelected(LibraryError):
    def __init__(self , message = 'Invalid Input Selected !!! Try Again ...'):
        self.message = message
        super().__init__(message)