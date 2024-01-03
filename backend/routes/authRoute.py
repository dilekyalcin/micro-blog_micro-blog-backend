from flask import Blueprint, request, jsonify
from models.users import Users
from flask_jwt_extended import create_access_token
import hashlib
import secrets


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
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
def login():
    data = request.get_json()

    user = Users.objects(username=data.get('username')).first()

    if user and verify_password_hash(data.get('password'), user.password_salt, user.password_hash):
        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token, message='Login successful!'), 200
    else:
        return jsonify({'message': 'Invalid username or password!'}), 401


# @auth_bp.route('/logout', methods=['POST'])
# @jwt_required()
# def logout():
#     jti = get_jwt()["jti"]
#     token_blacklist = request.blueprint.token_blacklist
#     token_blacklist.add(jti)
#     return jsonify(message='Logged out successfully'), 200

def create_password_hash(password):
    password_salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + password_salt).encode('utf-8')).hexdigest()
    
    return password_salt, password_hash

def verify_password_hash(password, password_salt, stored_password_hash):
    hashed_password = hashlib.sha256((password + password_salt).encode('utf-8')).hexdigest()
    
    return hashed_password == stored_password_hash