# 📚 Library Management System (CMD Based)

## 📌 Description
This is a Command Line (CMD) based Library Management System developed using Python and SQLite3.  
It manages both user and librarian operations with authentication and transaction tracking.

---

## 🚀 Features

### 👤 User Features
- User registration (Name, Email stored in database)
- Unique User ID generation
- View all available books
- Borrow books (if available)
- Return books using Transaction ID
- View all transactions using User ID (if Transaction ID is forgotten)

---

### 👨‍💼 Librarian Features
- Secure login with authentication (password-based)
- Add books with quantity
- Remove books from library
- Manage book availability

---

## 🔐 Authentication System
- Librarian access is restricted using a password
- Only librarians can modify book records
- Users have read and borrow permissions only

## 🔐 Librarian Authentication 
- The Librarians can only Add, Manage ,Remove Book Records
- To Access as a Librarian using Librarian Id Sounds Incomplete
- Use "LBM@123" whenever system Ask for Authentication  

---

## 🗄️ Database (SQLite3)
The system uses SQLite3 to store:
- User details (ID, Name, Email)
- Librarian details
- Book details (Book ID,Book Name,Book Author, Book ISBN, Quantity)
- Transactions:
  - Transaction ID
  - User ID
  - Book ID
  - Borrow Date
  - Return Date

---

## 🔄 Workflow

1. User/Librarian registers → gets unique ID  
2. Login using ID  
3. User:
   - View books → Borrow → Transaction created  
   - Return book using Transaction ID  
4. Librarian:
   - Login with password  
   - Add/Remove books  

---

## ▶️ How to Run

```bash
python main.py 
- check path "C:\......\Library Management System> ""# Library-Management-System" 
