from flask import Blueprint, request, jsonify
from models.users import Users, UserLoginDto, UserRegisterDto
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import hashlib
import secrets

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user_dto = UserRegisterDto(
        firstname=data.get('firstname'),
        lastname=data.get('lastname'),
        username=data.get('username'),
        password=data.get('password'),
        email=data.get('email')
    )

    existing_user = Users.objects(username=user_dto.username).first()
    if existing_user:
        return jsonify(message='Username is already taken!'), 400

    password_salt, password_hash = create_password_hash(user_dto.password)

    new_user = Users(
        firstname=user_dto.firstname,
        lastname=user_dto.lastname,
        username=user_dto.username,
        password_salt=password_salt,
        password_hash=password_hash,
        email=user_dto.email
    )
    new_user.save()

    return jsonify(message='Registration successful!'), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_dto = UserLoginDto(
        username=data.get('username'),
        password=data.get('password')
    )

    user = Users.objects(username=user_dto.username).first()

    if user and verify_password_hash(user_dto.password, user.password_salt, user.password_hash):
        access_token = create_access_token(identity=user_dto.username)
        return jsonify(access_token=access_token, message='Login successful!'), 200
    else:
        return jsonify({'message': 'Invalid username or password!'}), 401

@auth_bp.route('/get_users', methods=['GET'])
@jwt_required()
def get_users():
    current_user = get_jwt_identity()

    user = Users.objects(username=current_user).first()
   
    if user:
        return jsonify({'username': user.username, 'email': user.email}), 200
    else:
        return jsonify({'message': 'User not found!'}), 404


def create_password_hash(password):
    password_salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + password_salt).encode('utf-8')).hexdigest()
    
    return password_salt, password_hash

def verify_password_hash(password, password_salt, stored_password_hash):
    hashed_password = hashlib.sha256((password + password_salt).encode('utf-8')).hexdigest()
    
    return hashed_password == stored_password_hash