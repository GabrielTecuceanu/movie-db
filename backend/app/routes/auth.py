from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import mongo
from app.services.auth_service import generate_token
from app.services.feed_service import add_to_friends_feed_thread

from app.models.feed_item import FeedItem

from datetime import datetime

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
def register():
    data = request.json

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username:
        return jsonify({"error": "Username is required"}), 400
    if not email:
        return jsonify({"error": "Email is required"}), 400
    if not password:
        return jsonify({"error": "Password is required"}), 400

    if mongo.db.users.find_one({"email": email}):
        return jsonify({"error": "Email already exists"}), 400
    if mongo.db.users.find_one({"username": username}):
        return jsonify({"error": "Username already in use"}), 400

    hashed_password = generate_password_hash(password)

    mongo.db.users.insert_one(
        {
            "username": username,
            "email": email,
            "password": hashed_password,
            "movie_watchlist": [],
            "movie_finished": [],
            "tv_watchlist": [],
            "tv_finished": [],
            "favourite_people": [],
            "feed": [],
        }
    )

    return (
        jsonify(
            {
                "message": "User registered successfully",
                "token": generate_token(email),
            }
        ),
        201,
    )


@auth.route("/login", methods=["POST"])
def login():
    data = request.json

    email = data.get("email")
    password = data.get("password")
    print(data)

    if not email:
        return jsonify({"error": "Email is required"}), 400
    if not password:
        return jsonify({"error": "Password is required"}), 400

    user = mongo.db.users.find_one({"email": email})

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid password"}), 400

    return jsonify({"token": generate_token(email)}), 200


@auth.route("/delete_account", methods=["POST"])
def delete_account():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    if not email:
        return jsonify({"error": "Email is required"}), 400
    if not password:
        return jsonify({"error": "Password is required"}), 400

    user = mongo.db.users.find_one({"email": email})

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid password"}), 400

    # notify friends that user has deleted their account
    add_to_friends_feed_thread(
        email,
        FeedItem(email, "has deleted their account", datetime.now()),
    )

    # delete associated friendships and friend requests from the db
    mongo.db.friendship.delete_many(
        {"$or": [{"sender": email}, {"recipient": email}]}
    )
    mongo.db.fd_requests.delete_many(
        {"$or": [{"sender": email}, {"recipient": email}]}
    )

    mongo.db.users.delete_one({"email": email})

    return jsonify({"message": "User deleted successfully"}), 200