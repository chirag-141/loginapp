# add_user.py
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

client = MongoClient('mongodb://localhost:27017/')
db = client['login_db']
users_collection = db['users']

# Add a test user
users_collection.insert_one({
    'email': 'sathish@example.com',
    'password': generate_password_hash("12345")
})