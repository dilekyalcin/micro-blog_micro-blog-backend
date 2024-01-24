from flask import Flask, request, Blueprint, jsonify
from models.DbContext import connect_to_mongodb
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from models.Users import Users 
from models.Post import Post
from flask_cors import cross_origin
import datetime
import hashlib
import secrets

connect_to_mongodb()

user_bp = Blueprint('user', __name__)

@user_bp.route("/update_user", methods=['PUT'])
@jwt_required()
@cross_origin()
def update_user():
    """
    Updates information about the authenticated user.

    Retrieves user information, validates the current user's existence,
    and updates the user's information.

    Returns:
        jsonify: A JSON response indicating the success or failure of the user update.
    """
    data = request.get_json()
    
    user_id = get_jwt_identity()

    current_user = Users.objects(id=user_id).first()

    if not current_user:
        return {"error": 'User not found.'}, 404
    
      
    if 'password' in data:
        password_salt = secrets.token_hex(16)
        password_hash = hashlib.sha256((data['password'] + password_salt).encode('utf-8')).hexdigest()
        current_user.update(set__password_salt=password_salt, set__password_hash=password_hash)

    current_user.update(
        set__firstname=data.get('firstname', current_user.firstname),
        set__lastname=data.get('lastname', current_user.lastname),
        set__username=data.get('username', current_user.username),
        set__email=data.get('email', current_user.email),
        set__bio=data.get('bio', current_user.bio),
 
    )

    return {"message": "User updated."}, 200

def create_password_hash(password):
    """
    Generates a password hash and salt.

    Args:
        password (str): The password to hash.

    Returns:
        tuple: A tuple containing the password salt and hash.
    """
    password_salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + password_salt).encode('utf-8')).hexdigest()
    
    return password_salt, password_hash

@user_bp.route("/get_user_info", methods=['GET'])
@jwt_required()
@cross_origin()
def get_user_info():
    """
    Retrieves information about the authenticated user.

    Returns:
        jsonify: A JSON response containing information about the authenticated user.
    """
    user = Users.objects(username=current_user.username).first()

    if user:
        user_info ={
            "firstname": user.firstname,
            "lastname": user.lastname,
         }
        return jsonify(user_info), 200
    else:
        return jsonify({"error": "User not found"}), 404

@user_bp.route("/get_user_profile", methods=['GET'])
def get_user_profile():
    """
    Retrieves information about a specific user's profile.

    Returns:
        jsonify: A JSON response containing information about the specified user's profile.
    """
    username = request.args.get('username', '')

    user = Users.objects(username=username).first()

    if not user:
        return jsonify({"message": "User not found"}), 404


    user_posts = Post.objects(author=user)

    user_profile = {
        "username": user.username,
        "bio": user.bio,
        "posts": [
            {
                "title": post.title,
                "content": post.content,
                "created_at": str(post.created_at),
            }
            for post in user_posts
        ],
    }

    return jsonify(user_profile), 200


@user_bp.route("/search_users", methods=['GET'])
@cross_origin()
def search_users():
    """
    Searches for users based on a query.

    Returns:
        jsonify: A JSON response containing information about users matching the search query.
    """
    search_query = request.args.get('query', '')

    similar_users = Users.objects(firstname__icontains=search_query)

    users_list = [
        {
            "username": user.username,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "bio": user.bio,
            "birthdate": str(user.birthdate) if user.birthdate else None,
            "created_at": str(user.created_at),
        }
        for user in similar_users
    ]

    return jsonify(users_list), 200
