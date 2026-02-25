import http

from flask import Flask, jsonify, request
app = Flask(__name__)
# create a list of users
users = [
    {"id": 1, "name": "John Doe", "email": "john.doe@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane.smith@example.com"},
    {"id": 3, "name": "Bob Johnson", "email": "bob.johnson@example.com"}
]



#1. Create a route to get home page
@app.route('/', methods=['GET'])
def home_page():
    return 'database of users'
#2. Create a route to get all users

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)
#to get a specific user by id

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    for user in users:
        if user['id']== user_id:
            return jsonify(user)
        
    return jsonify({'error' : 'users not found '})
 # route to add new users
@app.route('/users', methods=['POST'])
def add_user():
    new_user = {
        "id": "5",
        "name": "Raj ",
        "email": "raj@example.com",
    }
    users.append(new_user)
    return jsonify({'message': ' user added succesfully'})

# start a server
if __name__ == '__main__':
    app.run(debug=True)