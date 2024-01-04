from flask import Flask, request, Blueprint, jsonify
from models.dbContext import connect_to_mongodb
from models.like import Like
from models.post import Post 
from models.users import Users 
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from flask_cors import cross_origin
import datetime

connect_to_mongodb()

like_bp = Blueprint('like', __name__)

@like_bp.route("/add_like", methods=['POST', 'OPTIONS'])
@jwt_required()
@cross_origin()
def add_like():
    
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


@like_bp.route("/get_all_likes", methods=['GET'])
@jwt_required()
@cross_origin()
def get_all_likes():
    likes = Like.objects().all()

    result = []

    for like in likes:
        result.append({
            'id': str(like.id),
            'author_username': like.user.username,
            'post': like.post.content,
        })

    return jsonify(result), 200
