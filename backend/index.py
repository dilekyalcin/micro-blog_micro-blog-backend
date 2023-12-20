from flask import Flask, jsonify
# from models.user import User
# from flask_cors import CORS
from routes import user_bp, post_bp, comment_bp, like_bp, auth_bp
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import json
import os

app = Flask(__name__)
jwt = JWTManager(app)

current_directory = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_directory, 'config.json')


with open(config_file_path, 'r') as f:
    config_data = json.load(f)
    for key, value in config_data.items():
        app.config[key] = value

# CORS(app)
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(post_bp, url_prefix='/post')
app.register_blueprint(comment_bp, url_prefix='/comment')
app.register_blueprint(like_bp, url_prefix='/like')
app.register_blueprint(auth_bp, url_prefix='/auth')

# @app.route("/homePage", methods=['GET', 'OPTIONS'])
# def show_the_home_page():
#     user = User("Dilek", "Yalcin")
#     response = jsonify({"data": { "firstname": "Dilek", "message": user.toPrintString()}})
#     return response


if __name__ == "__main__":
    app.run(debug = True)