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

login_data1 = {
        "username": "testuser",
        "password": "password123"
}

def test_register(client):
   
    response = client.post("/auth/register", json=data)
    assert response.status_code == 201
    assert response.json["message"] == "Registration successful!"
    

    response = client.post("/auth/register", json=data)
    assert response.status_code == 400
    

def test_login(client, dummy_user):
    login_data1 = {
        "username": dummy_user[0].username,
        "password": dummy_user[1]
}
    response = client.post("/auth/login", json=login_data1)
    assert response.status_code == 200
    assert "access_token" in response.json

    response = client.post("/auth/login", json={
        "username": "wrong_username",
        "password": "wrong_password"
    })
    assert response.status_code == 401
    assert "access_token" not in response.json
    assert response.json["message"] == "Invalid username or password!"

def test_logout(client, dummy_user, logged_in_client):
    response = client.delete('/logout', headers = logged_in_client)
    assert response.status_code == 200
    assert b"Successfully logged out" in response.data

