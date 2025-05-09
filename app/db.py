"""
The Chromatic BaNANAs: Amanda Tan, Anastasia Lee, Naomi Lai, and Nia Lam
SoftDev
P05: Color Theory for Dummies
2025-06-11
"""

import sqlite3, os

DATABASE_NAME = "DATABASE.db"

def createTables():
    if os.path.exists(DATABASE_NAME):
        print("Database already exists!!!\nWill not create tables")
    else:
        print("Creating tables...")
        db = sqlite3.connect(DATABASE_NAME)
        c = db.cursor()

        #User Info
        c.execute('''
                CREATE TABLE IF NOT EXISTS UserData (
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                    )
            ''')

        db.commit()
        db.close()

        print("Tables successfully created \n")
        return True

#just call this when resetting db, it calls createTables
#if not, call neither
def resetDB():
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
        print("Resetting DB")
        return createTables()
    else:
        print("Cannot reset database as database does not exist")
        print("Creating database")
        return createTables()

def createUser(username, password):
    print(f"Adding user {username}")
    db = sqlite3.connect(DATABASE_NAME)
    c = db.cursor()

    try:
        c.execute('INSERT INTO UserData VALUES (?, ?)', (username, password))
        db.commit()
        db.close()
        print("Successfully added user")
        return True
    except Exception as e:
        print("Failed to add user (does the user already exist in the database?)")
        db.close()
        return False

def checkLogin(username, password):
    print(f"Checking login for {username}")
    db = sqlite3.connect(DATABASE_NAME)
    c = db.cursor()
    c.execute("SELECT password FROM UserData WHERE username = ?", (username,))
    row = c.fetchone()

    if row == None:
        print("Username does not exist in db")
        return False #account w that email does not exist

    if row[0] == password:
        print("Login correct")
        return True
    else:
        print("Incorrect password")
        return False

#will reset DB and add some data
def createSampleData():
    resetDB()