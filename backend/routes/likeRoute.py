from flask import Flask, request, Blueprint, jsonify
from models.DbContext import connect_to_mongodb
from models.like import Like
from models.Post import Post 
from models.Users import Users 
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from flask_cors import cross_origin
import datetime

connect_to_mongodb()

like_bp = Blueprint('like', __name__)

@like_bp.route("/add_like", methods=['POST', 'OPTIONS'])
@jwt_required()
@cross_origin()
def add_like():
    """
    Adds a like to a post.

    Validates user authentication, retrieves post information,
    and adds a like associated with the current user.

    Returns:
        jsonify: A JSON response indicating the success or failure of the like addition.
    """
    if not  current_user:
        return {"error": 'User not found.'}, 404

    data = request.get_json()

    post = Post.objects(id=data['post_id']).first()

    if not post:
        return {"error": 'Post not found.'}, 404

    existing_like = Like.objects(user=current_user, post=post).first()
    if existing_like:
        return {"message": "User already liked this post."}, 200

    new_like = Like(user=current_user, post=post)
    new_like.save()

    like_count = Like.objects(post=post).count()

    return {"message": "Post liked successfully.", "liked": True, "likeCount": like_count}, 201


@like_bp.route("/remove_like", methods=['DELETE'])
@jwt_required()
@cross_origin()
def remove_like():
    """
    Removes a like from a post.

    Validates user authentication and removes the like associated with the current user.

    Returns:
        jsonify: A JSON response indicating the success or failure of the like removal.
    """
    if not current_user:
        return {"error": 'User not found.'}, 404

    data = request.get_json()
    post = Post.objects(id=data['post_id']).first()

    if not post:
        return {"error": 'Post not found.'}, 404

    existing_like = Like.objects(user=current_user, post=post).first()
    if not existing_like:
        return {"message": "User has not liked this post."}, 200

    existing_like.delete()

    return {"message": "Like removed successfully."}, 200


@like_bp.route("/get_all_likes/<post_id>", methods=['GET'])
@jwt_required()
@cross_origin()
def get_likes_by_post(post_id):
    
    likes = Like.objects(post=post_id)

    result = []

    for like in likes:
        result.append({
            'id': str(like.id),
            'author_username': like.user.username,
            'post': like.post.content,
            'firstname' : like.user.firstname,
            'lastname' : like.user.lastname
        })

    return jsonify(result), 200
