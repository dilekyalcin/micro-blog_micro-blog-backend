from flask import Flask, jsonify
from models.users import Users
# from flask_cors import CORS
from routes import user_bp, post_bp, comment_bp, like_bp, auth_bp
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import json
import os

app = Flask(__name__)
jwt = JWTManager(app)

# token_blacklist = set()

current_directory = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_directory, 'config.json')


with open(config_file_path, 'r') as f:
    config_data = json.load(f)
    for key, value in config_data.items():  
        app.config[key] = value

@jwt.user_identity_loader
def user_identity_lookup(user):
    return str(user.id)

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Users.objects.get(id=identity)

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(post_bp, url_prefix='/post')
app.register_blueprint(comment_bp, url_prefix='/comment')
app.register_blueprint(like_bp, url_prefix='/like')
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == "__main__":
    app.run(debug = True)