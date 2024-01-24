from flask import Flask, request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from models.dbContext import connect_to_mongodb
from models.users import Users
from models.post import Post
from models.comment import Comment
import datetime
from flask_cors import cross_origin

connect_to_mongodb()

comment_bp = Blueprint('comment', __name__)


@comment_bp.route("/add_comment", methods=['POST'])
@jwt_required()
@cross_origin()
def add_comment():
    """
    Adds a new comment to a post.

    Validates user authentication, retrieves post information,
    and creates a new comment associated with the current user.

    Returns:
        jsonify: A JSON response indicating the success or failure of the comment addition.
    """
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
@cross_origin()
def delete_comment(comment_id):
    """
    Deletes a comment identified by its ID.

    Validates user authentication and ownership of the comment,
    then deletes the comment.

    Args:
        comment_id (str): The ID of the comment to be deleted.

    Returns:
        jsonify: A JSON response indicating the success or failure of the comment deletion.
    """
    if not current_user:
        return {"error": 'User not found.'}, 404

    comment = Comment.objects(id=comment_id, author=current_user).first()
    if not comment:
        return {"error": 'Comment not found or you do not have permission to delete it.'}, 404

    comment.delete()

    return {"message": 'Comment deleted.'}, 200


@comment_bp.route("/update_comment/<comment_id>", methods=['PUT'])
@jwt_required()
@cross_origin()
def update_comment(comment_id):
    """
    Updates the content of a comment identified by its ID.

    Validates user authentication and ownership of the comment,
    then updates the comment content.

    Args:
        comment_id (str): The ID of the comment to be updated.

    Returns:
        jsonify: A JSON response indicating the success or failure of the comment update.
    """
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


@comment_bp.route("/get_all_comments/<post_id>", methods=['GET'])
@jwt_required()
@cross_origin()
def get_comments_by_post(post_id):
    """
    Retrieves all comments on a post.

    Validates user authentication and retrieves all comments associated with the specified post.

    Args:
        post_id (str): The ID of the post to retrieve comments for.

    Returns:
        jsonify: A JSON response containing information about all comments on the specified post.
    """
    comments = Comment.objects(post = post_id)

    result = []
    for comment in comments:
        result.append({
            'id': str(comment.id),
            'content': comment.content,
            'author_username': comment.author.username,
            'author_id': str(comment.author.id),
            'post': comment.post.content,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify(result), 200
