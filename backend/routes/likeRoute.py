from flask import Flask, request, Blueprint
from models.dbContext import connect_to_mongodb
from models.like import Like
from models.post import Post 
from models.users import Users 
import datetime

connect_to_mongodb()

like_bp = Blueprint('like', __name__)

@like_bp.route("/addLike", methods=['POST', 'OPTIONS'])
def add_like():
    data = request.get_json()

    user = Users.objects(id=data['user_id']).first()
    if not user:
        return {"error": 'User not found.'}, 404

    post = Post.objects(id=data['post_id']).first()
    if not post:
        return {"error": 'Post not found.'}, 404

    
    existing_like = Like.objects(user=user, post=post).first()
    if existing_like:
        return {"message": "User already liked this post."}, 200


    new_like = Like(user=user, post=post)
    new_like.save()


    return {"message": "Post liked successfully."}, 201

