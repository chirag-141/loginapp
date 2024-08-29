from flask import Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['login_db']
users_collection = db['users']

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    user = users_collection.find_one({'email': email})
    if user and check_password_hash(user['password'], password):
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Invalid credentials😞'})

@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get('email')
    
    user = users_collection.find_one({'email': email})
    if user:
        temp_password = "temporary_password"
        hashed_password = generate_password_hash(temp_password)
        users_collection.update_one({'email': email}, {'$set': {'password': hashed_password}})
        return jsonify({'success': True, 'temp_password': temp_password})
    return jsonify({'success': False, 'message': 'Email not found 😞'})

@app.route('/update-password', methods=['POST'])
def update_password():
    data = request.json
    email = data.get('email')
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    user = users_collection.find_one({'email': email})
    if user and check_password_hash(user['password'], current_password):
        hashed_new_password = generate_password_hash(new_password)
        users_collection.update_one({'email': email}, {'$set': {'password': hashed_new_password}})
        return jsonify({'success': True, 'message': 'Password updated successfully!'})
    return jsonify({'success': False, 'message': 'Current password is incorrect 😞'})

if __name__ == '__main__':
    app.run(debug=True)
