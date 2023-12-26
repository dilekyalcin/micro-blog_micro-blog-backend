from flask import Flask, request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from models.dbContext import connect_to_mongodb
from models.users import Users
from models.post import Post
from models.comment import Comment
import datetime

connect_to_mongodb()

comment_bp = Blueprint('comment', __name__)


@comment_bp.route("/add_comment", methods=['POST'])
@jwt_required()
def add_comment():
  
    if not current_user:
        return {"error": 'User not found.'}, 404

    data = request.get_json()

    post = Post.objects(id=data['post_id']).first()
    if not post:
        return {"error": 'Post not found.'}, 404

    new_comment = Comment(
        content=data['content'],
        author=current_user,
        post=post,
        created_at=datetime.datetime.now()
    )

    new_comment.save()

    return {"message": 'Comment added.'}, 201


@comment_bp.route("/delete_comment/<comment_id>", methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):

    if not current_user:
        return {"error": 'User not found.'}, 404

    comment = Comment.objects(id=comment_id, author=current_user).first()
    if not comment:
        return {"error": 'Comment not found or you do not have permission to delete it.'}, 404

    comment.delete()

    return {"message": 'Comment deleted.'}, 200


@comment_bp.route("/update_comment/<comment_id>", methods=['PUT'])
@jwt_required()
def update_comment(comment_id):

    if not current_user:
        return {"error": 'User not found.'}, 404

    comment = Comment.objects(id=comment_id, author=current_user).first()
    if not comment:
        return {"error": 'Comment not found or you do not have permission to update it.'}, 404

    data = request.get_json()

    comment.content = data.get('content', comment.content)
    comment.created_at = datetime.datetime.now()
    comment.save()

    return {"message": 'Comment updated.'}, 200


@comment_bp.route("/get_all_comments", methods=['GET'])
@jwt_required()
def get_all_comments():
    comments = Comment.objects().all()

    result = []
    for comment in comments:
        result.append({
            'id': str(comment.id),
            'content': comment.content,
            'author_username': comment.author.username,
            'post': comment.post.content,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify(result), 200
