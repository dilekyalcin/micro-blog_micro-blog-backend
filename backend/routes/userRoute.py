from flask import Flask, request,Blueprint
from models.dbContext import connect_to_mongodb
from models.users import Users 
import datetime

connect_to_mongodb()

user_bp = Blueprint('user', __name__)
    
@user_bp.route("/addUser", methods=['POST', 'OPTIONS'])
def add_user():
    data = request.get_json()

    new_user = Users(
        firstname=data['firstname'],
        lastname=data['lastname'],
        username=data['username'],
        password=data['password'],
        email=data['email'],
        bio=data['bio'],
        birthdate=datetime.datetime.strptime(data['birthdate'], '%Y-%m-%d') if 'birthdate' in data else None,
        created_at=datetime.datetime.now(),
    )

    new_user.save()

    return {"message": "User added."}, 201






