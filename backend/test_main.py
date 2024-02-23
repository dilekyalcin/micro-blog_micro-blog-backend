import pytest
from mongoengine import connect, disconnect
import mongomock
from index import app
from models.Users import Users
import os
from tests.test_authRoute import test_register, test_login, test_create_password_hash, test_verify_password_hash,logged_in_client,test_add_post,test_delete_post
from models.Users import Users
import secrets
import hashlib
from mongomock import MongoClient

@pytest.fixture()
def client(monkeypatch):
    disconnect(alias='default')
    connect(host='localhost', alias='default', mongo_client_class=mongomock.MongoClient)
    monkeypatch.setenv('MONGO_URL', 'mongomock://localhost')
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    app.config['DEBUG'] = True

    with app.test_client() as client:
        yield client
    
# def create_password_hash(password):
#     if password is None:
#         raise ValueError("Password cannot be None")
#     password_salt = secrets.token_hex(16)
#     password_hash = hashlib.sha256((password + password_salt).encode('utf-8')).hexdigest()
#     return password_salt, password_hash
# def verify_password_hash(password, password_salt, stored_password_hash):
#     hashed_password = hashlib.sha256((password + password_salt).encode('utf-8')).hexdigest()
    
#     return hashed_password == stored_password_hash

# def test_register(client):
#     email = "test1@gmail.com"
#     username = "test1"
#     password = "password123"
#     password_salt, password_hash = create_password_hash(password)
#     data ={
#         "firstname": "Test",
#         "lastname": "User",
#         "username": username,
#         "email": email,
#         "password": password,
#     }
#     response = client.post("/auth/register", json=data)
    
#     user = Users.objects(username=data["username"]).first()
#     assert user is not None, "User not found in the database"
#     assert user.username == data["username"]
#     assert user.email == data["email"]
#     assert user.firstname == data["firstname"]
#     assert user.lastname == data["lastname"]
#     assert user.password_salt == password_salt
#     assert user.password_hash == password_hash
#     assert response.status_code == 201
#     assert response.json["message"] == "Registration successful!"
#     response = client.post("/auth/register", json=data)
#     assert response.status_code == 400

# def test_login(client):
#     username = "test1"
#     password = "password123"
#     data = {"username": username, "password": password}
#     user = Users.objects(username=data["username"]).first()
#     print(user, data)
#     if user:
#         is_correct_password = verify_password_hash(password, user.password_salt, user.password_hash)
#         assert is_correct_password == True
        
#     response = client.post("/auth/login", json=data)
#     assert response.status_code == 200
#     assert "access_token" in response.json
#     assert "userId" in response.json
#     assert response.json["message"] == "Login successful!"

#     # wrong password
#     data = {"username": username, "password": "wrongpassword"}
#     response = client.post("/auth/login", json=data)
#     assert response.status_code == 401
#     assert response.json == {"message": "Invalid username or password!"}


# jwt_token = None
# def create_password_hash(password):
#     if password is None:
#         raise ValueError("Password cannot be None")
#     password_salt = secrets.token_hex(16)
#     password_hash = hashlib.sha256((password + password_salt).encode('utf-8')).hexdigest()
#     return password_salt, password_hash

# def verify_password_hash(password, password_salt, stored_password_hash):
#     hashed_password = hashlib.sha256((password + password_salt).encode('utf-8')).hexdigest()
    
#     return hashed_password == stored_password_hash

# mongo_client = MongoClient()
# db = mongo_client['test_db']
# collection = db['users']

# def test_register(client):
   
#     email = "test569@gmail.com"
#     username = "test579"
#     password = "password123"
#     data ={
#         "firstname": "Test",
#         "lastname": "test1",
#         "username": username,
#         "email": email,
#         "password": password,
#     }
#     password_salt, password_hash = create_password_hash(password)

#     response = client.post("/auth/register", json=data)
    

#     new_user = Users(
#         firstname=data['firstname'],
#         lastname=data['lastname'],
#         username=data['username'],
#         password_salt=password_salt,
#         password_hash=password_hash,
#         email=data['email']
#     )
#     collection.insert_one(new_user.to_mongo())

#     user = collection.find_one({"username": data["username"]})
#     assert user is not None, "User not found in the database"
#     assert user['username'] == data["username"]
#     assert user['email'] == data["email"]
#     assert user['firstname'] == data["firstname"]
#     assert user['lastname'] == data["lastname"]
#     assert user['password_salt'] ==password_salt
#     assert user['password_hash'] ==password_hash


#     assert response.status_code == 201
#     assert response.json["message"] == "Registration successful!"

#     response = client.post("/auth/register", json=data)
#     assert response.status_code == 400

# def test_login(client):
#     global jwt_token
#     try:
#         username = "test579"
#         password = "password123"
#         data = {"username": username, "password": password}
            
#         response = client.post("/auth/login", json=data)
#         print(response.json)

#         user = collection.find_one({"username": data["username"]})

#         print(user, data)

    
#         is_correct_password = verify_password_hash(password, user["password_salt"], user["password_hash"])
#         print(is_correct_password)
#         assert is_correct_password == True

#         data = response.get_json()
#         assert response.status_code == 200
#         assert 'access_token' in data
#         assert 'userId' in data
#         assert data['message'] == 'Login successful!'
#         jwt_token = data['access_token']

#         # wrong password
#         data = {"username": username, "password": "wrongpassword"}
#         response = client.post("/auth/login", json=data)
#         assert response.status_code == 401
#         assert response.json == {"message": "Invalid username or password!"}
#     except:
#         print("error")


# def test_add_post(client):
#     global jwt_token
    
#     # Add a new post
#     data = {
#         'title': 'New Post Title6',
#         'content': 'New Post Content7'
#     }
#     headers = {
#         'Authorization': f'Bearer {jwt_token}'
#     }
#     response = client.post('/post/add_post', json=data, headers=headers)
#     assert response.status_code == 201
#     assert b'Post added successfully!' in response.data

#     assert response.content_type == 'application/json' 

if __name__ == "__main__":
  
  pytest.main(["-m", "not integration"])
