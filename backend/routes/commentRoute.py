from flask import Flask, request,Blueprint
from models.dbContext import connect_to_mongodb
import datetime
from models.users import Users
from models.post import Post
from models.comment import Comment


connect_to_mongodb()

comment_bp = Blueprint('comment', __name__)

@comment_bp.route("/addComment", methods=['POST', 'OPTIONS'])
def add_comment():
    data = request.get_json()

    author = Users.objects(id=data['author_id']).first()
    if not author:
        return {"error":'User not found.'}, 404

    post = Post.objects(id=data['post_id']).first()
    if not post:
        return {"error":'Post not found.'}, 404

    new_comment = Comment(
        content=data['content'],
        author=author,
        post=post,
        created_at=datetime.datetime.now()
    )

    new_comment.save()

    return {"message": 'Comment added.'}, 201

