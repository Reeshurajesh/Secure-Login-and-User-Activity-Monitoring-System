# Secure Login and User Activity Monitoring System

## Project Overview

The Secure Login and User Activity Monitoring System is a Python-based application connected to a MySQL database. It provides user registration, secure login, profile management, password changing, and activity monitoring features.

## Features

* User Registration
* User Login Authentication
* Password Hashing using SHA-256
* View User Profile
* Update Email
* Change Password
* View Personal Activity Logs
* View All Activity Logs
* MySQL Database Integration

## Technologies Used

* Python
* MySQL
* MySQL Connector
* Hashlib

## Database

**Database Name:** `Aarathy`

**Tables:**

* `USERS` – Stores user details and password hashes.
* `activity_logs` – Stores user activities, status, and timestamps.

## How to Run

1. Install Python and MySQL.

2. Install the required package:

   `pip install mysql-connector-python`

3. Create a MySQL user or configure the existing MySQL connection details in the program.

4. Run `secure_login.py` using Python IDLE or the command prompt.

The program creates the database and tables automatically when the MySQL connection is configured correctly.


## Source Code

The complete Python source code is available in [`secure_login.py`](secure_login.py).


## Project Screenshots

### 1. User Registration
![User Registration](Screenshot%20(50)%201.png)

### 2. Login
![Login](Screenshot%20(51)%202.png)

### 3. User Profile
![User Profile](Screenshot%20(52)%203.png)

### 4. Update Email
![Update Email](Screenshot%20(53)%204.png)

### 5. Change Password
![Change Password](Screenshot%20(54)%205.png)

### 6. My Activity Logs
![My Activity Logs](Screenshot%20(55)%206.png)

### 7. All Activity Logs
![All Activity Logs](Screenshot%20(56)%207.png)


## Author

Reeshma Devi R

