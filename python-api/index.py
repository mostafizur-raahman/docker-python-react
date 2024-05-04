from flask import Flask, request, jsonify
from pymongo import MongoClient 

app = Flask(__name__)
client = MongoClient('mongodb+srv://python:e4qUmi3qDJeAosHA@cluster0.nnzvw7t.mongodb.net/')
db = client['python']
collection = db['users']

# Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    dob = data.get('dob')

    if name and age and dob:
        user = {
            "name": name,
            "age": age,
            "dob": dob
        }
        collection.insert_one(user)
        
        return jsonify({"message": "User created successfully"}), 201
    else:
        return jsonify({"error": "Missing fields"}), 400

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = list(collection.find({}, {'_id': 0}))
    return jsonify(users), 200

# Update a user
@app.route('/users/<name>', methods=['PUT'])
def update_user(name):
    data = request.json
    new_age = data.get('age')
    new_dob = data.get('dob')

    query = {"name": name}
    new_values = {"$set": {"age": new_age, "dob": new_dob}}
    collection.update_one(query, new_values)

    if collection.find_one(query):
        return jsonify({"message": "User updated successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404

# Delete a user
@app.route('/users/<name>', methods=['DELETE'])
def delete_user(name):
    query = {"name": name}
    result = collection.delete_one(query)
    
    if result.deleted_count > 0:
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404
    

@app.route('/')
def index():
    return 'Hello, World! This is my Flask application.'


if __name__ == '__main__':
    app.run(debug=True)
