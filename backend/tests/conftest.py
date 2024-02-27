import sys
import os
sys.path.append(os.path.abspath(
   os.path.join(os.path.dirname(__file__), os.path.pardir)
))
from index import app
import pytest
from mongoengine import connect, disconnect
import mongomock
from models.Users import Users
import os
from routes.authRoute import create_password_hash
from models.Post import Post
from models.Comment import Comment
from models.like import Like
from datetime import datetime

@pytest.fixture()
def client(monkeypatch):
  monkeypatch.setenv('MONGO_URL', 'localhost')
  mongo_url = os.environ.get('MONGO_URL')
  connect(host=mongo_url, alias='default', mongo_client_class=mongomock.MongoClient)
  
  app.config['TESTING'] = True
  app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
  app.config['DEBUG'] = True

  with app.test_client() as client:
        yield client
    
@pytest.fixture
def dummy_user():
  password = "password123"
  password_salt, password_hash = create_password_hash(password)

  user = Users(
     firstname = "Test",
     lastname = "User",
     username = "testuser",
     email = "usertest@gmail.com",
     password_salt = password_salt,
     password_hash = password_hash
  
  )
  user.save()

  yield user, password

  user.delete()
  

@pytest.fixture
def dummy_post(dummy_user):
   post_data= Post(
      title="Test Post",
      content="this is a test post.",
      author = dummy_user[0],
      created_at=datetime.now()
   )
   post_data.save()

   yield post_data

   post_data.delete()
 
@pytest.fixture
def logged_in_client(client):
    login_data1={
    "username": "testuser",
    "password": "password123"
    }

    response = client.post("/auth/login", json=login_data1)
    
    jwt_token = response.json["access_token"]
    
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        "Content-Type": "application/json",
    }
    yield headers
    


@pytest.fixture
def dummy_comment(dummy_user, dummy_post):
    comment = Comment(
        content="Test Comment",
        author=dummy_user[0],
        post=dummy_post,
        created_at=datetime.now()
    )
    comment.save()

    yield comment

    comment.delete()

@pytest.fixture
def dummy_like(dummy_user, dummy_post):
    like = Like(
        user=dummy_user[0],
        post=dummy_post
    )
    like.save()
    yield like

    like.delete()


if __name__ == "__main__":
  
  pytest.main(["-m", "not integration"])
