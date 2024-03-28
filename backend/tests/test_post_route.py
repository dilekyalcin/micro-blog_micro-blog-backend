from routes.post_route import Post
from models.Users import Users
from datetime import datetime

def assert_post_fields(post):
    assert 'id' in post
    assert 'title' in post
    assert 'content' in post
    assert 'author' in post
    assert 'firstname' in post
    assert 'lastname' in post
    assert 'likeCount' in post
    assert 'likes' in post
    assert 'tag' in post
    assert 'created_at' in post

def test_get_following_posts(client, user_with_followers, logged_in_client2, dummy_like):
    response = client.get('/post/following-posts', headers=logged_in_client2)
    assert response.status_code == 200

    posts = response.json

    assert len(posts) > 0

    for post in posts:
        assert_post_fields(post)


def test_add_post(client, dummy_user, logged_in_client):
    data1 = {
    'title': 'New Post Title',
    'content': 'New Post Content'
    }
    response = client.post('/post', json=data1, headers=logged_in_client)
    assert response.status_code == 201
    assert response.json["message"] == "Post added successfully!"


def test_update_post(client, dummy_user, logged_in_client, dummy_post):
    update_data = {
        "title": "Updated Post Title",
        "content": "Updated Post Content"
    }

    response = client.put(f'/post/{dummy_post.id}', json=update_data, headers=logged_in_client)
    assert response.status_code == 200
    assert response.json["message"] == "Post updated successfully!"

    # Check if the post is updated correctly in the database
    updated_post = Post.objects(id=dummy_post.id).first()
    assert updated_post.title == update_data["title"]
    assert updated_post.content == update_data["content"]

def test_delete_post(client, dummy_user, logged_in_client, dummy_post):
    post_id = str(dummy_post.id)

    # Attempt to delete the post
    response = client.delete(f'/post/{post_id}', headers=logged_in_client)
    assert response.status_code == 200

    # Check if the post has been deleted
    deleted_post = Post.objects(id=post_id).first()
    assert deleted_post is None

    # Attempt to delete the post again
    response = client.delete(f'/post/{post_id}', headers=logged_in_client)
    assert response.status_code == 404
    data = response.json
    assert data["message"] == "Post not found or you do not have permission to delete it!"
 
def test_get_currentuser_posts(client, dummy_user, logged_in_client, dummy_post, dummy_comment, dummy_like):
    response = client.get('/post/currentuser-post', headers=logged_in_client)
    assert response.status_code == 200

    posts = response.json
    assert len(posts) > 0

    first_post = posts[0]
    assert_post_fields(first_post)

    assert first_post['author'] == dummy_user[0].username

    assert first_post['likeCount'] > 0  

    expected_date = dummy_post.created_at.strftime("%Y-%m-%d %H:%M:%S")
    assert expected_date in first_post['created_at']


def test_get_posts_by_date(client, dummy_user, logged_in_client, dummy_post, dummy_comment, dummy_like):

    start_date = datetime.strftime(dummy_post.created_at, "%Y-%m-%d")
    end_date = datetime.strftime(dummy_post.created_at, "%Y-%m-%d")


    response = client.get(f'/post/posts-by-date/{start_date}/{end_date}', headers=logged_in_client)
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
