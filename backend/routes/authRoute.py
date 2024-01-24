from flask import Blueprint, request, jsonify
from models.Users import Users
from flask_jwt_extended import create_access_token
from flask_cors import cross_origin
import hashlib
import secrets


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@cross_origin()
def register():
    """
    Handles the user registration process.

    Validates input data, checks for existing username, creates a password hash,
    and saves the new user to the database.

    Returns:
        jsonify: A JSON response indicating the success or failure of the registration process.
    """
    data = request.get_json()

    existing_user = Users.objects(username=data.get('username')).first()
    if existing_user:
        return jsonify(message='Username is already taken!'), 400

    password_salt, password_hash = create_password_hash(data.get('password'))

    new_user = Users(
       firstname=data.get('firstname'),
        lastname=data.get('lastname'),
        username=data.get('username'),
        password_salt=password_salt,
        password_hash=password_hash,
        email=data.get('email')
    )
    new_user.save()

    return jsonify(message='Registration successful!'), 201

@auth_bp.route('/login', methods=['POST'])
@cross_origin()
def login():
    """
    Handles user login authentication.

    Validates login credentials, generates an access token, and returns a JSON
    response with the access token and user information.

    Returns:
        jsonify: A JSON response containing the access token and user information upon successful login.
    """
    data = request.get_json()
    print('data: ', data)

    user = Users.objects(username=data.get('username')).first()
    print('user: ', user)
    if user and verify_password_hash(data.get('password'), user.password_salt, user.password_hash):
        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token, userId=str(user.id), message='Login successful!'), 200
    else:
        return jsonify({'message': 'Invalid username or password!'}), 401

def create_password_hash(password):
    """
    Generates a password salt and hash for secure password storage.

    Args:
        password (str): The password to be hashed.

    Returns:
        tuple: A tuple containing the password salt and hashed password.
    """
    password_salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + password_salt).encode('utf-8')).hexdigest()
    
    return password_salt, password_hash

def verify_password_hash(password, password_salt, stored_password_hash):
    """
    Verifies a password against the stored hash.

    Args:
        password (str): The password to be verified.
        password_salt (str): The salt used during password hashing.
        stored_password_hash (str): The stored hash of the password.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    hashed_password = hashlib.sha256((password + password_salt).encode('utf-8')).hexdigest()
    
    return hashed_password == stored_password_hash