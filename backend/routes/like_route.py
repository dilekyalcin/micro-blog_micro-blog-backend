from flask import Flask, request, Blueprint, jsonify
from models.like import Like
from models.Post import Post 
from models.Users import Users 
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from flask_cors import cross_origin
import datetime

like_bp = Blueprint('like', __name__)

@like_bp.route('', methods=['POST', 'DELETE'])
@jwt_required()
@cross_origin()
def like_unlike_post():
    if not current_user:
        return {"error": 'User not found.'}, 404

    data = request.get_json()
    post = Post.objects(id=data['post_id']).first()

    if not post:
        return {"error": 'Post not found.'}, 404

    existing_like = Like.objects(user=current_user, post=post).first()

    if request.method == 'POST':
        if existing_like:
            return {"message": "User already liked this post."}, 200

        new_like = Like(user=current_user, post=post)
        new_like.save()

        tag = post.tag
        tag.popularity_score += 1
        tag.save()

        like_count = Like.objects(post=post).count()

        return {"message": "Post liked successfully.", "liked": True, "likeCount": like_count}, 201

    elif request.method == 'DELETE': 
        if not existing_like:
            return {"message": "User has not liked this post."}, 200

        existing_like.delete()

        tag = post.tag
        tag.popularity_score -= 1
        tag.save()

        return {"message": "Like removed successfully."}, 200



@like_bp.route("/all-likes/<post_id>", methods=['GET'])
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