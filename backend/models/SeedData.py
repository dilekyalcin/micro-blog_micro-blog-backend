from models.users import Users
from models.post import Post
from models.comment import Comment
from models.dbContext import connect_to_mongodb
import datetime


connect_to_mongodb()


user = Users(
    firstname="Dilek",
    lastname="Yalcin",
    username="dilekyalcin",
    password="dilek123",
    email="dilek@gmail.com",
    bio="Lorem ipsum dolor sit amet.",
    birthdate=datetime.datetime(1999, 2, 4),
    created_at=datetime.datetime.now()
)
user.save()


post = Post(
    title="Python MongoDB Post",
    content="Lorem ipsum dolor sit amet.",
    author=user,
    created_at=datetime.datetime.now()
)
post.save()


comment = Comment(
    content="Good post!",
    author=user,
    post=post,
    created_at=datetime.datetime.now()
)
comment.save()


# user.liked_posts.append(post)
# user.comments.append(comment)
# user.posts.append(post)
# post.likes.append(user)
# post.comments.append(comment)
# user.save()
# post.save()
