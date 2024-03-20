def test_add_like(client, dummy_user, logged_in_client, dummy_post):
    response = client.post('/like', json={"post_id": str(dummy_post.id)}, headers=logged_in_client)
    assert response.status_code == 201
    assert response.json['message'] == 'Post liked successfully.'

def test_remove_like(client, dummy_user, logged_in_client, dummy_post, dummy_like):
    response = client.delete('/like', json={"post_id": str(dummy_post.id)}, headers=logged_in_client)
    assert response.status_code == 200
    assert response.json['message'] == 'Like removed successfully.'

def test_get_likes_by_post(client, dummy_user, logged_in_client, dummy_post, dummy_like):
    response = client.get(f'/like/all-likes/{str(dummy_post.id)}', headers=logged_in_client)
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['author_username'] == dummy_user[0].username