from flask import Flask, jsonify
from models.User import User
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route("/homePage", methods=['GET', 'OPTIONS'])
def show_the_home_page():
    user = User("Dilek", "Yalcin")
    response = jsonify({"data": { "firstname": "Dilek", "message": user.toPrintString()}})
    return response


if __name__ == "__main__":
    app.run(debug = True)