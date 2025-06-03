"""
The Chromatic BaNANAs: Amanda Tan, Anastasia Lee, Naomi Lai, and Nia Lam
SoftDev
P05: Color Theory for Dummies
2025-06-06
"""
import csv
import bcrypt
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://anastasial25:lqRQwo37qTkbKnlG@softdev-p5.cvervwo.mongodb.net/?retryWrites=true&w=majority&appName=softdev-p5"

# Create a new client and connect to the server
client = MongoClient(uri, server_api = ServerApi('1'))

database = client['database']
user_collection = database['users']

def insert_user_data(username, password):
    # use bcrypt as a password hasher
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password.encode('utf-8'), salt)

    user_dict = {
        'username': username,
        # plaintext password is NOT stored, only its salt and hash
        'salt': salt,
        'password_hash': hash,
        'color1': '#33ccff',
        'color2': '#ff99cc',
        'to': 0,
        'scores': []
    }
    user_collection.insert_one(user_dict)

def verify_user_login(inputted_username, inputted_password):
    for user_document in user_collection.find({'username': inputted_username}):
        salt = user_document['salt']
        password_hash = user_document['password_hash']
        inputted_password_hash = bcrypt.hashpw(inputted_password.encode('utf-8'), salt)
        if password_hash == inputted_password_hash:
            print(f'Login successful for {inputted_username}!')
            return True
        else:
            print('Incorrect password.')
            return False
    print('Username not found.')
    return False

def get_color_info(username):
    for user_document in user_collection.find({'username': username}):
        color_info = [user_document['color1'], user_document['color2'], user_document['to']]
    return color_info

def update_color_info(username, color1, color2, to):
    user_collection.update_one( 
        {'username': username},
        {'$set': {'color1': color1, 'color2': color2, 'to': to}}
        )

def get_scores(username):
    for user_document in user_collection.find({'username': username}):
        scores = user_document['scores']
    return scores

def update_scores(username, score):
    new_scores = get_scores(username).append(score)
    user_collection.update_one( 
        {'username': username},
        {'$set': {'scores': scores}}
        )

def clear_collection(collection_name):
    document_deletion = collection_name.delete_many({})
    print(f'{document_deletion.deleted_count} documents deleted from {collection_name}.')
