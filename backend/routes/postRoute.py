from flask import Flask, request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from models.dbContext import connect_to_mongodb
from models.post import Post 
from models.users import Users 
from models.comment import Comment
from models.like import Like
from datetime import datetime 
from flask_cors import cross_origin
import json
from mongoengine import DoesNotExist

connect_to_mongodb()

post_bp = Blueprint('post', __name__)
    
@post_bp.route('/add_post', methods=['POST'])
@jwt_required()
@cross_origin()
def add_post():
    if not current_user:
        return jsonify({'message': 'User not found!'}), 404

    data = request.get_json()

    new_post = Post(
        title=data.get('title'),
        content=data.get('content'),
        author=current_user['id'],
        created_at=datetime.now()
    )

    new_post.save()

    return jsonify({'message': 'Post added successfully!'}), 201


@post_bp.route('/delete_post/<post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):

    if not current_user:
        return jsonify({'message': 'User not found!'}), 404

    post = Post.objects(id=post_id, author=current_user).first()

    if not post:
        return jsonify({'message': 'Post not found or you do not have permission to delete it!'}), 404
    
    Comment.objects(post=post).delete()

    Like.objects(post=post).delete()

    post.delete()

    return jsonify({'message': 'Post deleted successfully!'}), 200


@post_bp.route('/update_post/<post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):

    if not current_user:
        return jsonify({'message': 'User not found!'}), 404

    post = Post.objects(id=post_id, author=current_user).first()

    if not post:
        return jsonify({'message': 'Post not found or you do not have permission to update it!'}), 404

    data = request.get_json()

    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    post.created_at = datetime.now()
    post.save()

    return jsonify({'message': 'Post updated successfully!'}), 200


@post_bp.route('/get_all_posts', methods=['GET'])
@jwt_required()
def get_all_posts():
    
    posts = Post.objects().all()
    result = []

    for post in posts:
        result.append({
            'id': str(post.id),
            'title': post.title,
            'content': post.content,
            'author': post.author.username,
            'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify(result), 200


@post_bp.route('/get_posts_by_date', methods=['GET'])
@jwt_required()
def get_posts_by_date():
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'message': 'Invalid date format! Please use YYYY-MM-DD.'}), 400

    posts = Post.objects(created_at__gte=start_date, created_at__lte=end_date).all()

    result = []
    for post in posts:
        result.append({
            'id': str(post.id),
            'title': post.title,
            'content': post.content,
            'author': post.author.username,
            'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify(result), 200


@post_bp.route('/get_posts_by_attribute', methods=['GET'])
@jwt_required()
def get_posts_by_attribute():
    attribute = request.args.get('attribute', '').lower()
    value = request.args.get('value', '')

    if attribute not in ['title', 'content', 'author', 'created_at']:
        return jsonify({'message': 'Invalid attribute! Please choose from title, content, author, or created_at.'}), 400

    posts = [] 

    if attribute == 'title':
        posts = Post.objects(title=value).all()

    if attribute == 'created_at':
        try:
            value = datetime.datetime.strptime(value, '%Y-%m-%d')
            posts = Post.objects(created_at__gte=value, created_at__lt=value + datetime.timedelta(days=1)).all()
        except ValueError:
            return jsonify({'message': 'Invalid date format! Please use YYYY-MM-DD.'}), 400

    if attribute == 'author':
        try:
            author = Users.objects.get(username=value)
        except DoesNotExist:
            return jsonify({'message': f'Author with username {value} not found.'}), 404

        posts = Post.objects(author=author).all()

    result = []
    for post in posts:
        result.append({
            'id': str(post.id),
            'title': post.title,
            'content': post.content,
            'author': post.author.username,
            'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify(result), 200
