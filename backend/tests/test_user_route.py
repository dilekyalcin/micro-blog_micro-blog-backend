from models.Users import Users
from routes.authRoute import create_password_hash, verify_password_hash

def test_update_user(client, dummy_user, logged_in_client):
    new_data = {
        "firstname": "New Firstname",
        "lastname": "New Lastname",
        "username": "new_username",
        "email": "new_email@gmail.com",
        "bio": "New Bio",
        "password": "new_password123",
    }

    response = client.put("/user", json=new_data, headers=logged_in_client)
    assert response.status_code == 200
    assert response.json == {"message": "User updated."}

    # Check if the user information is updated correctly
    updated_user = Users.objects(id=dummy_user[0].id).first()
    assert updated_user.firstname == new_data["firstname"]
    assert updated_user.lastname == new_data["lastname"]
    assert updated_user.username == new_data["username"]
    assert updated_user.email == new_data["email"]
    assert updated_user.bio == new_data["bio"]

    # Check if the password is updated correctly
    verify_password = verify_password_hash(new_data["password"], updated_user.password_salt, updated_user.password_hash)
    assert verify_password == True

    # Check if the new password can be used to log in
    login_data = {
        "username": new_data["username"],
        "password": new_data["password"]
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json



def test_get_user_info(client, dummy_user,logged_in_client):
    response = client.get('/user/user-info', headers=logged_in_client)
    assert response.status_code == 200

    user_info = response.json
    assert user_info['firstname'] == dummy_user[0].firstname
    assert user_info['lastname'] == dummy_user[0].lastname

def test_get_user_profile(client, dummy_user, dummy_post):
    # existing username
    response = client.get(f'/user/user-profile?username={dummy_user[0].username}')
    assert response.status_code == 200

    user_profile = response.json
    assert user_profile['username'] == dummy_user[0].username
    assert user_profile['bio'] == dummy_user[0].bio
    assert user_profile['posts'][0]['title'] == dummy_post.title
    assert user_profile['posts'][0]['content'] == dummy_post.content

    # non-existing username
    response = client.get('/user/user-profile?username=non_existing_user')
    assert response.status_code == 404
    assert response.json['message'] == 'User not found'


def test_search_users(client, dummy_user, logged_in_client):
    response = client.get('/user/search-users', headers=logged_in_client)
    assert response.status_code == 200

    users_list = response.json
    found = False
    for user in users_list:
        if user['username'] == dummy_user[0].username:
            found = True
            assert found, f"User '{dummy_user[0].username}' found in search results"
            break

    assert found, f"User '{dummy_user[0].username}' not found in search results"


def test_get_user_posts(client, dummy_user, dummy_post):
    # existing username
    response = client.get(f'/user/{dummy_user[0].username}/posts')
    assert response.status_code == 200

    user_posts = response.json
    assert user_posts[0]['title'] == dummy_post.title
    assert user_posts[0]['content'] == dummy_post.content

    # non-existing username
    response = client.get('/user/non-existing-user/posts')
    assert response.status_code == 404
    assert response.json['error'] == 'User not found'


