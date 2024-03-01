from models.Users import Users
from models.Post import Post
from models.Comment import Comment
import datetime


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


user.liked_posts.append(post)
user.comments.append(comment)
user.posts.append(post)
post.likes.append(user)
post.comments.append(comment)
user.save()
post.save()
