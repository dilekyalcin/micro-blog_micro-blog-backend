from routes.postRoute import Post
from models.Users import Users
from datetime import datetime


def test_get_all_posts(client, dummy_user, logged_in_client, dummy_post, dummy_comment, dummy_like):
    response = client.get('/post/get_all_posts', headers=logged_in_client)
    assert response.status_code == 200

    posts = response.json
    assert len(posts) > 0

    print("get all posts: ",posts)

    first_post = posts[0]

    assert 'id' in first_post
    assert 'title' in first_post
    assert 'content' in first_post
    assert 'author' in first_post
    assert 'firstname' in first_post
    assert 'lastname' in first_post
    assert 'likeCount' in first_post
    assert 'likes' in first_post
    assert 'created_at' in first_post

    
    expected_date = datetime.strftime(dummy_post.created_at, "%Y-%m-%d %H:%M:%S")
    assert expected_date in first_post['created_at']


def test_add_post(client, dummy_user, logged_in_client):
    data1 = {
    'title': 'New Post Title',
    'content': 'New Post Content'
    }
    response = client.post('/post/add_post', json=data1, headers=logged_in_client)
    assert response.status_code == 201
    assert response.json["message"] == "Post added successfully!"


def test_update_post(client, dummy_user, logged_in_client, dummy_post):
    update_data = {
        "title": "Updated Post Title",
        "content": "Updated Post Content"
    }

    response = client.put(f'/post/update_post/{dummy_post.id}', json=update_data, headers=logged_in_client)
    assert response.status_code == 200
    assert response.json["message"] == "Post updated successfully!"

    # Check if the post is updated correctly in the database
    updated_post = Post.objects(id=dummy_post.id).first()
    assert updated_post.title == update_data["title"]
    assert updated_post.content == update_data["content"]
 

def test_get_currentuser_posts(client, dummy_user, logged_in_client, dummy_post, dummy_comment, dummy_like):
    response = client.get('/post/get_currentuser_post', headers=logged_in_client)
    assert response.status_code == 200

    posts = response.json
    assert len(posts) > 0

    first_post = posts[0]
    assert 'id' in first_post
    assert 'title' in first_post
    assert 'content' in first_post
    assert 'author' in first_post
    assert 'firstname' in first_post
    assert 'lastname' in first_post
    assert 'likeCount' in first_post
    assert 'likes' in first_post
    assert 'created_at' in first_post

    assert first_post['author'] == dummy_user[0].username

    assert first_post['likeCount'] > 0  

    expected_date = dummy_post.created_at.strftime("%Y-%m-%d %H:%M:%S")
    assert expected_date in first_post['created_at']


def test_get_posts_by_date(client, dummy_user, logged_in_client, dummy_post, dummy_comment, dummy_like):

    start_date = datetime.strftime(dummy_post.created_at, "%Y-%m-%d")
    end_date = datetime.strftime(dummy_post.created_at, "%Y-%m-%d")


    response = client.get(f'/post/get_posts_by_date/{start_date}/{end_date}', headers=logged_in_client)
    assert response.status_code == 200

    # Check if the returned data is correct
    posts = response.json
    
    for post in posts:
        post1 = Post.objects(id=dummy_post['id']).first()
        author = Users.objects(id=post1.author).first()

        assert post['id'] == str(post1.id)
        assert post['title'] == post1.title
        assert post['content'] == post1.content
        assert author.username == dummy_user.username
        assert author.firstname == dummy_user.firstname
        assert author.lastname == dummy_user.lastname
        assert post['created_at'] == post1.created_at.strftime('%Y-%m-%d %H:%M:%S')
