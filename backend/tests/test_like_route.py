def test_manage_like(client, dummy_user, logged_in_client, dummy_post, dummy_like):
    dummy_like.delete()

    # Like a post
    response = client.post('/like/managed-like', json={"post_id": str(dummy_post.id)}, headers=logged_in_client)
    assert response.status_code == 201
    assert response.json['message'] == 'Post liked successfully.'

    # Attempt to like the same post again
    response = client.post('/like/managed-like', json={"post_id": str(dummy_post.id)}, headers=logged_in_client)
    assert response.status_code == 200
    assert response.json['message'] == 'User already liked this post.'

    # Unlike the post
    response = client.delete('/like/managed-like', json={"post_id": str(dummy_post.id)}, headers=logged_in_client)
    assert response.status_code == 200
    assert response.json['message'] == 'Like removed successfully.'

    # Attempt to unlike the same post again
    response = client.delete('/like/managed-like', json={"post_id": str(dummy_post.id)}, headers=logged_in_client)
    assert response.status_code == 200
    assert response.json['message'] == 'User has not liked this post.'


def test_get_likes_by_post(client, dummy_user, logged_in_client, dummy_post, dummy_like):
    response = client.get(f'/like/all-likes/{str(dummy_post.id)}', headers=logged_in_client)
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['author_username'] == dummy_user[0].username