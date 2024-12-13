from flask import Blueprint, jsonify, request

from app.extensions import mongo

info = Blueprint("info", __name__)


@info.route("/", methods=["GET"])
def index():
    return jsonify({"message": "server is online"}), 200


@info.route("/get_all", methods=["GET"])
def get_all_users():
    users = mongo.db.users.find(
        {},
        {
            "_id": 0,
            "password": 0,
            "email": 0,
            "favourite_people": 0,
            "movie_finished": 0,
            "movie_watchlist": 0,
            "tv_finished": 0,
            "tv_watchlist": 0,
            "feed": 0,
        },
    )

    return jsonify(list(users)), 200

@info.route("/get_user/username/<string:username>", methods=["GET"])
def user_by_username(username):

    user = mongo.db.users.find_one({"username": username}, {"_id": 0, "password": 0,})
    if not user:
        return jsonify({"error": "Username does not exist"}), 400

    return jsonify(user), 200

@info.route("/get_user/email/<string:email>", methods=["GET"])
def user_by_email(email):

    user = mongo.db.users.find_one({"email": email}, {"_id": 0, "password": 0,})
    if not user:
        return jsonify({"error": "Email is not registered"}), 400

    return jsonify(user), 200
