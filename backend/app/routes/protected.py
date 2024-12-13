from flask import Blueprint, request, jsonify

from app.extensions import mongo
from app.services.auth_service import verify_token


protected = Blueprint("protected", __name__)


@protected.route("/profile", methods=["GET"])
def get_profile():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token is required"}), 400

    token = token.split(" ")[1]

    payload, error = verify_token(token)

    if error:
        return jsonify(error), 400

    email = payload["email"]

    user = mongo.db.users.find_one({"email": email}, {"password": 0, "_id": 0})

    return jsonify(user), 200

@protected.route("/token", methods=["GET"])
def username_from_token():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token is required"}), 400

    token = token.split(" ")[1]

    payload, error = verify_token(token)

    if error:
        return jsonify(error), 400

    email = payload["email"]

    user = mongo.db.users.find_one({"email": email})

    if not user:
        return jsonify({"error": "User does not exist"}), 404

    return jsonify(user['username']), 200