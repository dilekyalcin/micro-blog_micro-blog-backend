from flask import request, Blueprint, jsonify
from models.Tag import Tags
from models.Post import Post
from models.Users import Users
from models.like import Like
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity

tag_bp = Blueprint('tag', __name__)

@tag_bp.route('/managed-tags', methods=['GET', 'POST'])
@cross_origin()
def manage_tags():
    if request.method == 'GET':
        tags = Tags.objects()
        tag_list = [{'id': str(tag.id), 'name': tag.tag_name} for tag in tags]
        return jsonify(tag_list)
    elif request.method == 'POST':
        data = request.get_json()
        tag_name = data.get('tag_name')

        if not tag_name:
            return jsonify({"message": "Tag name is required"}), 400

        existing_tag = Tags.objects(tag_name__iexact=tag_name).first()
        if existing_tag:
            return jsonify({"message": "Tag already exists"}), 400

        new_tag = Tags(tag_name=tag_name)
        new_tag.save()

        return jsonify({"message": "Tag added successfully", "tag_id": str(new_tag.id)}), 201

@tag_bp.route('/popular-tags', methods=['GET'])
@jwt_required()
@cross_origin()
def get_popular_tags():
    """
    Retrieves the most popular tags.

    Returns:
        jsonify: A JSON response containing the most popular tags.
    """
    all_tags = Tags.objects().order_by('-popularity_score')
    popular_tags = all_tags[:6]

    tag_list = [{"tag_name": tag.tag_name, "count": tag.popularity_score} for tag in popular_tags]
    return jsonify(tag_list)

@tag_bp.route('/<tag_name>', methods=['GET'])
@jwt_required()
@cross_origin()
def get_tag_posts(tag_name):
    """
    Retrieves posts associated with a specific tag.

    Args:
        tag_name (str): The name of the tag.

    Returns:
        jsonify: A JSON response containing the posts associated with the tag.
    """
    tag = Tags.objects(tag_name=tag_name).first()
    if not tag:
        return jsonify({"message": "Tag not found."}), 404

    posts = Post.objects(tag=tag)
    tag_posts = []
    for post in posts:
        tag = post.tag.tag_name if post.tag else None
        tag_posts.append({
            "id": str(post.id),
            "title": post.title,
            "content": post.content,
            "author": post.author.username,
            "firstname": post.author.firstname,
            "lastname": post.author.lastname,
            "tag": tag,
            "created_at": post.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify(tag_posts), 200

@tag_bp.route('/<tag_name>/followed-users-posts', methods=['GET'])
@jwt_required()
@cross_origin()
def get_followed_users_posts(tag_name):
    """
    Retrieves posts associated with users that the current user follows and have a specific tag.

    Args:
        tag_name (str): The name of the tag.

    Returns:
        jsonify: A JSON response containing the posts associated with the users that the current user follows and have the specified tag.
    """
    user_id = get_jwt_identity()
    user = Users.objects(id=user_id).first()

    following_users = user.following
    tag = Tags.objects(tag_name=tag_name).first()
    following_posts = []

    if tag:
        for following_user in following_users:
            posts = Post.objects(author=following_user, tag=tag)
            for post in posts:
                tag_name = post.tag.tag_name if post.tag else None
                likes = Like.objects(post=post.id)
                likes_info = []
                for like in likes:
                    user_info = {
                        "user_id": str(like.user.id),
                        "username": like.user.username,
                    }

                    likes_info.append(user_info)

                following_posts.append({
                    "id": str(post.id),
                    "title": post.title,
                    "content": post.content,
                    "author": post.author.username,
                    "firstname": post.author.firstname,
                    "lastname": post.author.lastname,
                    "likeCount": len(likes_info),
                    "likes": likes_info,
                    "tag": tag_name,
                    "created_at": post.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                })

    return jsonify(following_posts), 200
@tag_bp.route('/followed-users-tags', methods=['GET'])
@jwt_required()
@cross_origin()
def followed_users_tags():
    user_id = get_jwt_identity()
    user = Users.objects(id=user_id).first()

    followed_users = user.following
    tag_set = set()
    for followed_user in followed_users:
        posts = Post.objects(author=followed_user)
        for post in posts:
            if post.tag:
                tag_set.add(post.tag.tag_name)

    tag_list = [{'name': tag_name} for tag_name in tag_set]
    return jsonify(tag_list)
