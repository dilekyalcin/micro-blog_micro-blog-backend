def test_manage_tags(client, dummy_user, logged_in_client, dummy_tag):
    # Test GET request to retrieve tags
    response = client.get('/tag/managed-tags', headers=logged_in_client)
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, list)
    assert len(data) > 0
    assert all('id' in tag and 'name' in tag for tag in data)

    # Test adding a new tag
    tag_name = "New Tag"
    response = client.post('/tag/managed-tags', json={"tag_name": tag_name}, headers=logged_in_client)
    assert response.status_code == 201
    data = response.json
    assert "message" in data and "tag_id" in data
    assert data["message"] == "Tag added successfully"

    # Test adding an existing tag
    response = client.post('/tag/managed-tags', json={"tag_name": dummy_tag.tag_name}, headers=logged_in_client)
    assert response.status_code == 400
    data = response.json
    assert "message" in data
    assert data["message"] == "Tag already exists"

    # Test adding a tag without providing a name
    response = client.post('/tag/managed-tags', json={}, headers=logged_in_client)
    assert response.status_code == 400
    data = response.json
    assert "message" in data
    assert data["message"] == "Tag name is required"


def test_get_popular_tags(client, dummy_user, logged_in_client, dummy_post, dummy_tag, popular_tags):
    response = client.get('/tag/popular-tags', headers=logged_in_client)
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, list)

    # Check if tags are ordered by popularity score
    assert data[0]["tag_name"] == "Tag3"
    assert data[0]["count"] == 30
    assert data[1]["tag_name"] == "Tag2"
    assert data[1]["count"] == 20
    assert data[2]["tag_name"] == "Tag1"
    assert data[2]["count"] == 10

def test_get_tag_posts(client, dummy_user, logged_in_client, dummy_post, dummy_tag):
    response = client.get(f'/tag/{dummy_tag.tag_name}', headers=logged_in_client)
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, list)
    assert len(data) > 0
    assert all('id' in post and 'title' in post and 'content' in post and 'author' in post and 'tag' in post and 'created_at' in post for post in data)

def test_get_followed_users_posts(client, dummy_user, logged_in_client, follower1):
    response = client.post(f'/user/follow/{follower1.username}', headers=logged_in_client)
    assert response.status_code == 200
    assert response.json == {"username": follower1.username}

    # Test with a tag that exists
    tag_name = "Test Tag"
    response = client.get(f'/tag/{tag_name}/followed-users-posts', headers=logged_in_client)
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, list)
    assert len(data) > 0
    assert all('id' in post and 'title' in post and 'content' in post for post in data)

    # Test with a tag that does not exist
    tag_name = "Nonexistent Tag"
    response = client.get(f'/tag/{tag_name}/followed-users-posts', headers=logged_in_client)
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, list)
    assert len(data) == 0

def test_followed_users_tags(client, dummy_user, logged_in_client):
    response = client.get('/tag/followed-users-tags', headers=logged_in_client)
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, list)
    assert all('name' in tag for tag in data)