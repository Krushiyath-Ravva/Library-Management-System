from library_management.models.users import User,Student,Librarian
from library_management.database.user_queries import UserQueries
from library_management.utils.exceptions import UserAlreadyExists,UserNotFound

class UserServices:
    def __init__(self , db_file):
        self.user_queries = UserQueries(db_file=db_file)

    def register_librarian(self,name,email):
        librarian = Librarian(name=name , email=email)
        librarian_id  = self.user_queries.add_user(username=librarian.name , email=librarian.email , role= librarian.role)
        if librarian_id:
            return librarian_id
        else:
            raise UserAlreadyExists()

    def register_student(self,name,email):
            student = Student(name=name , email=email)
            student_id = self.user_queries.add_user(username=student.name , email=student.email , role=student.role)
            if student_id:
                return student_id
            else:
                raise UserAlreadyExists()
        
    def get_user(self , user_id):
        user = self.user_queries.get_user_by_id(user_id=user_id)
        if user:
            return user
        else:
            raise UserNotFound()
        
    def is_student(self , user_id):
        return  self.get_user(user_id)[3] == 'student'
    
    def is_librarian(self , user_id):
        return self.get_user(user_id)[3] == 'librarian'

    def close(self):
        self.user_queries.close_connection()