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
from routes.auth_route import create_password_hash
from models.Post import Post
from models.Comment import Comment
from models.like import Like
from models.Tag import Tags
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
def dummy_user2():
  password = "password123"
  password_salt, password_hash = create_password_hash(password)

  user = Users(
     firstname = "Test",
     lastname = "User",
     username = "testuser2",
     email = "usertest2@gmail.com",
     password_salt = password_salt,
     password_hash = password_hash 
  )
  user.save()

  yield user, password

  user.delete()
  
@pytest.fixture
def follower1(dummy_tag):
    password = "password123"
    password_salt, password_hash = create_password_hash(password)

    follower = Users(
        firstname="Follower",
        lastname="One",
        username="follower1",
        email="follower1@gmail.com",
        password_salt=password_salt,
        password_hash=password_hash
    )
    follower.save()

    post = Post(
        title="Post from follower1",
        content="This is a post from follower1.",
        author=follower,
        tag=dummy_tag,
        created_at=datetime.now()
    )
    post.save()

    yield follower

    follower.delete()
    post.delete()

@pytest.fixture
def follower2():
    password = "password123"
    password_salt, password_hash = create_password_hash(password)

    follower = Users(
        firstname="Follower",
        lastname="Two",
        username="follower2",
        email="follower2@gmail.com",
        password_salt=password_salt,
        password_hash=password_hash
    )
    follower.save()

    post = Post(
        title="Post from follower2",
        content="This is a post from follower2.",
        author=follower,
        created_at=datetime.now()
    )
    post.save()

    yield follower

    follower.delete()
    post.delete()

@pytest.fixture
def user_with_followers(follower1, follower2):
    password = "password123"
    password_salt, password_hash = create_password_hash(password)

    user = Users(
        firstname="Test2",
        lastname="User2",
        username="testuser2",
        email="usertest2@gmail.com",
        password_salt=password_salt,
        password_hash=password_hash,
        followers=[follower1, follower2],
        following=[follower1]
    )
    user.save()

    yield user, password

    user.delete()

@pytest.fixture
def dummy_post(dummy_user, dummy_tag):
   post_data= Post(
      title="Test Post",
      content="this is a test post.",
      author=dummy_user[0],
      created_at=datetime.now(),
      tag=dummy_tag
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
def logged_in_client2(client):
    login_data1={
    "username": "testuser2",
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

@pytest.fixture
def dummy_tag():
    tag = Tags(
        tag_name="Test Tag",
        popularity_score=0
    )
    tag.save()

    yield tag

    tag.delete()


@pytest.fixture
def popular_tags():
    tags = [
        Tags(tag_name="Tag1", popularity_score=10),
        Tags(tag_name="Tag2", popularity_score=20),
        Tags(tag_name="Tag3", popularity_score=30)
    ]
    for tag in tags:
        tag.save()
    yield tags
    for tag in tags:
        tag.delete()

if __name__ == "__main__":
  
  pytest.main(["-m", "not integration"])
