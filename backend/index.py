from flask import Flask, jsonify
# from models.user import User
# from flask_cors import CORS
from routes import user_bp, post_bp, comment_bp

app = Flask(__name__)
# CORS(app)
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(post_bp, url_prefix='/post')
app.register_blueprint(comment_bp, url_prefix='/comment')

# @app.route("/homePage", methods=['GET', 'OPTIONS'])
# def show_the_home_page():
#     user = User("Dilek", "Yalcin")
#     response = jsonify({"data": { "firstname": "Dilek", "message": user.toPrintString()}})
#     return response


if __name__ == "__main__":
    app.run(debug = True)