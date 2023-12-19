from flask import Flask, request, Blueprint
from models.dbContext import connect_to_mongodb
from models.post import Post 
from models.users import Users 
import datetime

connect_to_mongodb()

post_bp = Blueprint('post', __name__)
    

@post_bp.route("/addPost", methods=['POST', 'OPTIONS'])
def add_post():
    data = request.get_json()

    author = Users.objects(id=data['author_id']).first()
    if not author:
        return {"error":'User not found.'}, 404

    new_post = Post(
        title=data['title'],
        content=data['content'],
        author=author,
        created_at=datetime.datetime.now(),
    )

    new_post.save()
    return {"message": "Post added."}, 201


