import mysql.connector

import hashlib

def connect_server():

    db = mysql.connector.connect(
        
        host="localhost",
        
        port=3306,
        
        user="root",

        password="Reesh@123",
    )

    return db

def create_database():

    db = connect_server()

    mycursor = db.cursor()

    mycursor.execute("create database if not exists Aarathy")

    db.commit()

    print("Database created Successfully")

    mycursor.close()

    db.close()


def connect_database():

    db = mysql.connector.connect(

        host="localhost",

        port=3306,

        user="root",

        password= "Reesh@123",

        database="Aarathy"
    )

    return db

def create_tables():

    db = connect_database()

    mycursor = db.cursor()

    mycursor.execute("""
        CREATE TABLE if not exists USERS(
            user_id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR (50)UNIQUE,
            email VARCHAR(100),
            password_hash VARCHAR(255),
            role VARCHAR(20) DEFAULT 'user',
            status VARCHAR(20) DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    mycursor.execute("""
        CREATE TABLE  if not exists activity_logs (
            log_id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT,
            username VARCHAR(50),
            activity VARCHAR(100),
            status VARCHAR(30),
            activity_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    db.commit()

    print("Tables Created Successfully")

    mycursor.close()

    db.close()

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()

def log_activity(user_id, username, activity, status):

    db = connect_database()

    mycursor = db.cursor()

    query = (""" INSERT INTO activity_logs (user_id, username, activity, status)
                 VALUES(%s, %s, %s, %s)""")

    values = (user_id,username,activity,status)

    mycursor.execute(query,values)

    db.commit()

    mycursor.close()

    db.close()

def register_user():

    print("\n-----USER  REGISTRATION-----")

    username = input("Enter username:")

    email = input("Enter email:")

    password = input("Enter Password:")

    password_hash = hash_password(password)

    db = connect_database()

    mycursor = db.cursor()


    query = ("""INSERT INTO USERS(username,email,password_hash)
             VALUES(%s,%s,%s)""")

    values = ( username,email,password_hash)

    try:

        mycursor.execute(query,values)

        db.commit()

        user_id = mycursor.lastrowid

        print("Registration Successfull")

        log_activity(user_id, username, "Register", "Success")

    except mysql.connector.Error as e:

            print("Registation Failed")

            print(e)

    mycursor.close()

    db.close()

def login_user():

    print("\n-----USER LOGIN-----")

    username = input("Enter Username:")
    password = input("Enter Password:")

    password_hash = hash_password(password)

    db = connect_database()

    mycursor = db.cursor()

    query = (""" SELECT user_id, username, email, role, status FROM users
                WHERE username =%s AND password_hash = %s """)


    values = ( username, password_hash)

    mycursor.execute(query,values)

    user = mycursor.fetchone()

    if user:

        user_id = user[0]
        username = user[1]
        email = user[2]
        role = user[3]
        status = user[4]

        if status == "active":

            print("Login Successfull")
            print("Welcome",username)

            log_activity(user_id, username, "Login", "Success")

            mycursor.close()

            db.close()

            user_menu(user_id,username,email)

            return

        else:

            print("Account id Inactive")


            log_activity(user_id, username, "Login", "Blocked")

    else:

        print("Invalid Username or Password")

        log_activity(0,username,"Login","Failed")

    mycursor.close()

    db.close()

def view_profile(user_id, username):

    db = connect_database()

    mycursor = db.cursor()

    query = (""" SELECT username, email, role, status, created_at
                 FROM users WHERE user_id= %s""")

    mycursor.execute(
        query,
        (user_id,)
    )

    user = mycursor.fetchone()

    if user:

        print("\n-----My Profile-----")

        print("Username:",user[0])
        print("Email:",user[1])
        print("Role:",user[2])
        print("Status:",user[3])
        print("Created:",user[4])


        log_activity(user_id, username,"View_Profile","Success")


        mycursor.close()

        db.close()


def update_email(user_id, username):

    new_email = input("Enter new email:")

    db = connect_database()

    mycursor = db.cursor()

    query = (""" UPDATE users SET email = %s WHERE user_id = %s""")


    mycursor.execute(query,(new_email,user_id))

    db.commit()

    print("Email updated Successfully")


    log_activity(user_id, username, "update_email",  "Success")

    mycursor.close()

    db.close()

def change_password(user_id, username):

    old_password = input("Enter old password:")
    new_password = input("Enter new password:")

    old_hash = hash_password(old_password)

    db = connect_database()

    mycursor = db.cursor()

    query = (""" SELECT user_id FROM users WHERE user_id = %s
                 AND password_hash = %s""")

    mycursor.execute(query,(user_id, old_hash))

    result = mycursor.fetchone()

    if result:

        new_hash = hash_password(new_password)

        update_query=("""UPDATE users SET password_hash = %s  WHERE user_id=%s""")

        mycursor.execute(update_query,(new_hash,user_id))

        db.commit()

        print("password  changed successfully")

        log_activity(user_id, username,"Change password", "Success")

    else:
        print("Old password is incorrect")


        log_activity(user_id, username, "Change password","Failed")

    mycursor.close()
        
    db.close()

def view_my_activity(user_id):

    db = connect_database()

    mycursor = db.cursor()

    query =(""" SELECT activity,status, activity_time FROM activity_logs
                WHERE user_id = %s  ORDER BY activity_time DESC""")

    mycursor.execute(
        query,
        (user_id,)
    )

    records = mycursor.fetchall()

    print("\n-----My Activity Log-----")

    for record in records:

        print(record[0],record[1],record[2])

    mycursor.close()

    db.close()

def user_menu(user_id, username, email):

    while True:

        print("\n-----User Menu-----")

        print("1.View Profile")
        print("2.Update Email")
        print("3.Change Password")
        print("4.View My Activity")
        print("5.Logout")

        choice = input("Enter Your choice:")

        if choice =="1":

            view_profile(user_id, username)

        elif choice =="2":

            update_email(user_id, username)

        elif choice =="3":

            change_password(user_id, username)

        elif choice =="4":

            view_my_activity(user_id)

        elif choice =="5":

            log_activity(user_id, username,"Logout","Success")

            print("Logged Out Successfully")

            break

        else:

            print("Invalid choice")

def view_all_activity():

    db = connect_database()

    mycursor = db.cursor()

    query = (""" SELECT log_id, username, activity, status, activity_time FROM activity_logs ORDER BY activity_time DESC""")

    mycursor.execute(query)

    records = mycursor.fetchall()

    print("\n-----ALL ACTIVITY LOGS-----")

    for record in records:

       print("ID:", record[0])
       print("User:", record[1])
       print("Activity:", record[2])
       print("Status:", record[3])
       print("Time:", record[4])

    mycursor.close()

    db.close()

def main():

    print("\n----SECURE LOGIN AND ACTIVITY MONITOR-----")

    create_database()

    create_tables()

    while True:

        print("\n-----Main Menu-----")

        print("1.Register")
        print("2.Login")
        print("3.View All Activity logs")
        print("4.Exit")

        choice = input("Enter Your Choice:")

        if choice =="1":

            register_user()

        elif choice =="2":

            login_user()

        elif choice =="3":

            view_all_activity()

        elif choice =="4":

            print("Program Closed")

            break
        

        else:

            print("Invalid choice.")

main()
            
    


    

    


    

    

     

        
    

    

    

    



    
          
            
                        


