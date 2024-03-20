from models.Comment import Comment
from bson import ObjectId

def test_add_comment(client, dummy_user, logged_in_client, dummy_post):
    headers = logged_in_client
    data = {
        'content': 'Test Comment',
        'post_id': str(dummy_post.id)
    }
    response = client.post('/comment', headers=headers, json=data)
    assert response.status_code == 201

    response = client.post('/comment', headers=headers,json={
        'content': 'Test Comment2',
        'post_id': str(ObjectId())
    })
    assert response.status_code == 404

def test_delete_comment(client, dummy_user, logged_in_client, dummy_comment):
    headers = logged_in_client
    response = client.delete(f'/comment/{str(dummy_comment.id)}', headers=headers)
    assert response.status_code == 200
    
    response = client.delete(f'/comment/{str(str(ObjectId()))}', headers=headers)
    assert response.status_code == 404

def test_update_comment(client, dummy_user, logged_in_client, dummy_comment):
    update_data = {
        "content": "Updated Comment."
    }

    response = client.put(f'/comment/{dummy_comment.id}', json=update_data, headers=logged_in_client)
    assert response.status_code == 200
    assert response.json["message"] == "Comment updated."

    updated_comment = Comment.objects(id=dummy_comment.id).first()
    assert updated_comment.content == update_data["content"]


def test_get_comments_by_post(client, dummy_user, logged_in_client, dummy_post, dummy_comment):
    response = client.get(f'/comment/all-comments/{dummy_post.id}', headers=logged_in_client)
    assert response.status_code == 200

    assert response.headers['Content-Type'] == 'application/json'

    comments = response.json
    assert len(comments) > 0  

    first_comment = comments[0]
    assert 'id' in first_comment
    assert 'content' in first_comment
    assert 'author_username' in first_comment
    assert 'author_id' in first_comment
    assert 'post' in first_comment
    assert 'created_at' in first_comment

    assert first_comment['post'] == dummy_post.content
    assert first_comment['author_username'] == dummy_user[0].username


