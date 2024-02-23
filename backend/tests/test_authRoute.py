from routes.authRoute import create_password_hash, verify_password_hash
from models.Users import Users
import pytest

def test_create_password_hash():
    password = "password123"
    salt, hashed_password = create_password_hash(password)
    assert len(salt) == 32  
    assert len(hashed_password) == 64 

def test_verify_password_hash():
    password = "password123"
    salt, hashed_password = create_password_hash(password)
    assert verify_password_hash(password, salt, hashed_password) == True 

email = "test1@example.com"
username = "test1"
password = "password123"
data ={
    "firstname": "Test",
    "lastname": "User",
    "username": username,
    "email": email,
    "password": password,
}
login_data={
    "username": username,
    "password": password
}

data1 = {
    'title': 'New Post Title',
    'content': 'New Post Content'
}

def test_register(client):
   
    response = client.post("/auth/register", json=data)
    assert response.status_code == 201
    assert response.json["message"] == "Registration successful!"
    

    response = client.post("/auth/register", json=data)
    assert response.status_code == 400
  

# def test_login(client):
   
#     # correct username and password
#     response = client.post("/auth/login", json=login_data)
#     assert response.status_code == 200
#     assert "access_token" in response.json
#     assert response.json["message"] == "Login successful!"

#     # wrong username and password
#     response = client.post("/auth/login", json={
#         "username": "wrong_username",
#         "password": "wrong_password"
#     })
#     assert response.status_code == 401
#     assert "access_token" not in response.json
#     assert response.json["message"] == "Invalid username or password!"
    

def test_login(client):
    # Register a new user
    response = client.post("/auth/register", json=data)
    assert response.status_code == 201
    assert response.json["message"] == "Registration successful!"

    # Login with the registered user
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json
    jwt_token = response.json["access_token"]

    response = client.post("/auth/login", json={
        "username": "wrong_username",
        "password": "wrong_password"
    })
    assert response.status_code == 401
    assert "access_token" not in response.json
    assert response.json["message"] == "Invalid username or password!"

@pytest.fixture
def logged_in_client(client):
    client.post("/auth/register", json=data)

    response = client.post("/auth/login", json=login_data)
    
    jwt_token = response.json["access_token"]
    
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        "Content-Type": "application/json",
    }
    return headers

def test_add_post(client, logged_in_client):
    response = client.post('/post/add_post', json=data1, headers=logged_in_client)
    assert response.status_code == 201
    assert response.json["message"] == "Post added successfully!"

def test_delete_post(client, logged_in_client):
    response = client.post('/post/add_post', json=data1, headers=logged_in_client)
    assert response.status_code == 201
    post_id = response.json.get("post_id")

    response = client.delete(f'/post/delete_post/{post_id}', headers=logged_in_client)
    assert response.status_code == 200


# def test_add_post(client):
#     response = client.post("/auth/register", json=data)
#     assert response.status_code == 201
#     assert response.json["message"] == "Registration successful!"

#     # Login with the registered user
#     response = client.post("/auth/login", json=login_data)
#     assert response.status_code == 200
#     assert "access_token" in response.json
#     jwt_token = response.json["access_token"]

#     headers = {
#         'Authorization': f'Bearer {jwt_token}',
#         "Content-Type": "application/json",
#     }

#     response = client.post('/post/add_post', json=data1, headers=headers)

#     assert response.status_code == 201
#     assert response.json["message"] == "Post added successfully!"

# def test_delete_post(client):
#     response = client.post("/auth/register", json=data)
#     assert response.status_code == 201
#     assert response.json["message"] == "Registration successful!"

#     response = client.post("/auth/login", json=login_data)
#     assert response.status_code == 200
#     assert "access_token" in response.json
#     jwt_token = response.json["access_token"]

#     headers = {
#         'Authorization': f'Bearer {jwt_token}',
#         "Content-Type": "application/json",
#     }

#     response = client.post('/post/add_post', json=data1, headers=headers)
#     assert response.status_code == 201

#     post_id = response.json.get("post_id")

#     response = client.delete(f'/post/delete_post/{post_id}', headers=headers)
#     assert response.status_code == 200

