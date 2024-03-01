from flask import Flask, jsonify
from models.Users import Users
from flask_cors import CORS, cross_origin
from routes import user_bp, post_bp, comment_bp, like_bp, auth_bp
from flask_jwt_extended import JWTManager, jwt_required, get_jwt
from models.db import connect_to_database
import json
import os

app = Flask(__name__)

app.config['MONGO_URL'] = os.environ.get('MONGO_URL')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_BLACKLIST_ENABLED'] = os.environ.get('JWT_BLACKLIST_ENABLED')
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = os.environ.get('JWT_BLACKLIST_TOKEN_CHECKS')
app.config['IMAGE_UPLOADS'] = os.environ.get('IMAGE_UPLOADS')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES')) if os.environ.get('JWT_ACCESS_TOKEN_EXPIRES') else 3600

cors_resources = {
    r"/*": {
        "origins": "http://localhost",
        "supports_credentials": True
    }
}
CORS(app, resources=cors_resources)


jwt = JWTManager(app)
token_blacklist = set()

@jwt.user_identity_loader
def user_identity_lookup(user):
    return str(user.id)

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Users.objects.get(id=identity)


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_data):
    jti = jwt_data["jti"]
    return jti in token_blacklist


@app.route('/logout', methods=['DELETE'])
@cross_origin()
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    token_blacklist.add(jti)

    with open("logged_out_tokens.txt", "a") as file:
        file.write(jti + "\n")
        
    return jsonify({"msg": "Successfully logged out"}), 200

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(post_bp, url_prefix='/post')
app.register_blueprint(comment_bp, url_prefix='/comment')
app.register_blueprint(like_bp, url_prefix='/like')
app.register_blueprint(auth_bp, url_prefix='/auth')


if __name__ == "__main__":
    # Connect to database
    connect_to_database(app.config['MONGO_URL'])
    app.run(host='0.0.0.0', port=5000, debug=True)