from flask import Blueprint, request, jsonify

from app.extensions import mongo
from app.services.auth_service import verify_token
from app.services.feed_service import add_to_feed_thread

from app.models.feed_item import FeedItem

from datetime import datetime


friends = Blueprint("friends", __name__)


@friends.route("/friends/request", methods=["POST"])
def send_friend_request():
    data = request.get_json()
    recipient_email = data.get("email")

    if not recipient_email:
        return jsonify({"error": "Recipient email is required"}), 400

    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token is required"}), 400

    token = token.split(" ")[1]

    payload, error = verify_token(token)

    if error:
        return jsonify(error), 400

    sender_email = payload.get("email")

    if sender_email == recipient_email:
        return (
            jsonify(
                {"error": "You cannot send a friend request to yourself :("}
            ),
            400,
        )

    if mongo.db.users.find_one({"email": recipient_email}) is None:
        return jsonify({"error": "Recipient not found"}), 404

    if existing_request := mongo.db.fd_requests.find_one(
        {"sender": sender_email, "recipient": recipient_email}
    ):
        return (
            jsonify(
                {
                    "error": "Friend request already sent "
                    + existing_request.get("status")
                }
            ),
            400,
        )

    if mongo.db.friendship.find_one(
        {
            "$or": [
                {"sender": sender_email, "recipient": recipient_email},
                {"sender": recipient_email, "recipient": sender_email},
            ]
        }
    ):
        return jsonify({"error": "Friendship already exists"}), 400

    mongo.db.fd_requests.insert_one(
        {
            "sender": sender_email,
            "recipient": recipient_email,
            "status": "pending",
            "created_at": datetime.now(),
        }
    )

    # notify recipient of friend request
    add_to_feed_thread(
        recipient_email,
        FeedItem(sender_email, "sent you a friend request", datetime.now()),
    )

    return jsonify({"message": "Friend request sent"}), 200


@friends.route("/friends/get_pending_requests", methods=["GET"])
def get_pending_friend_requests():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token is required"}), 400

    token = token.split(" ")[1]

    payload, error = verify_token(token)

    if error:
        return jsonify(error), 400

    email = payload.get("email")

    requests = mongo.db.fd_requests.find(
        {"recipient": email, "status": "pending"}, {"_id": 0}
    )

    return jsonify(list(requests)), 200


@friends.route("/friends/respond", methods=["POST"])
def respond_to_friend_request():
    data = request.get_json()
    sender_email = data.get("email")
    response = data.get("response")

    if not sender_email:
        return jsonify({"error": "Sender email is required"}), 400

    if response not in ["accept", "reject"]:
        return jsonify({"error": "Invalid response"}), 400

    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token is required"}), 400

    token = token.split(" ")[1]

    payload, error = verify_token(token)

    if error:
        return jsonify(error), 400

    recipient_email = payload.get("email")

    if not mongo.db.fd_requests.find_one(
        {
            "sender": sender_email,
            "recipient": recipient_email,
            "status": "pending",
        }
    ):
        return jsonify({"error": "Friend request not found"}), 404

    if mongo.db.friendship.find_one(
        {
            "$or": [
                {
                    "sender": sender_email,
                    "recipient": recipient_email,
                    "$or": [{"status": "accepted"}, {"status": "rejected"}],
                },
                {
                    "sender": recipient_email,
                    "recipient": sender_email,
                    "$or": [{"status": "accepted"}, {"status": "rejected"}],
                },
            ]
        }
    ):
        return jsonify({"error": "Already responded to request"}), 400

    if response == "accept":
        mongo.db.fd_requests.update_one(
            {"sender": sender_email, "recipient": recipient_email},
            {"$set": {"status": "accepted"}},
        )
        mongo.db.friendship.insert_one(
            {
                "sender": sender_email,
                "recipient": recipient_email,
                "since": datetime.now(),
            }
        )
    else:
        mongo.db.fd_requests.update_one(
            {"sender": sender_email, "recipient": recipient_email},
            {"$set": {"status": "rejected"}},
        )

    add_to_feed_thread(
        sender_email,
        FeedItem(
            recipient_email,
            "has " + response + "ed your friend request",
            datetime.now(),
        ),
    )

    return jsonify({"message": "Friend request " + response + "ed"}), 200


@friends.route("/friends/get_friends", methods=["GET"])
def get_friends():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token is required"}), 400

    token = token.split(" ")[1]

    payload, error = verify_token(token)

    if error:
        return jsonify(error), 400

    email = payload.get("email")

    friends = mongo.db.friendship.find(
        {"$or": [{"sender": email}, {"recipient": email}]}, {"_id": 0}
    )

    return jsonify(list(friends)), 200


@friends.route("/friends/remove", methods=["POST"])
def remove_friend():
    data = request.get_json()
    friend_email = data.get("email")

    if not friend_email:
        return jsonify({"error": "Friend email is required"}), 400

    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token is required"}), 400

    token = token.split(" ")[1]

    payload, error = verify_token(token)

    if error:
        return jsonify(error), 400

    email = payload.get("email")

    if not mongo.db.friendship.find_one(
        {
            "$or": [
                {"sender": email, "recipient": friend_email},
                {"sender": friend_email, "recipient": email},
            ]
        }
    ):
        return jsonify({"error": "Friendship not found"}), 404

    mongo.db.friendship.delete_one(
        {
            "$or": [
                {"sender": email, "recipient": friend_email},
                {"sender": friend_email, "recipient": email},
            ]
        }
    )

    add_to_feed_thread(
        friend_email,
        FeedItem(email, "has removed you as a friend", datetime.now()),
    )

    return jsonify({"message": "Friend removed"}), 200


@friends.route("/friends/is_friend", methods=["POST"])
def is_friend():
    data = request.get_json()
    friend_email = data.get("email")

    if not friend_email:
        return jsonify({"error": "Friend email is required"}), 400

    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token is required"}), 400

    token = token.split(" ")[1]

    payload, error = verify_token(token)

    if error:
        return jsonify(error), 400

    email = payload.get("email")

    if mongo.db.friendship.find_one(
        {
            "$or": [
                {"sender": email, "recipient": friend_email},
                {"sender": friend_email, "recipient": email},
            ]
        }
    ):
        return jsonify({"status": True}), 200

    return jsonify({"status": False}), 200


@friends.route("/friends/get_friend_profile", methods=["POST"])
def get_friend_profile():
    data = request.get_json()
    friend_email = data.get("email")

    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token is required"}), 400

    token = token.split(" ")[1]

    payload, error = verify_token(token)
    if error:
        return jsonify(error), 400

    email = payload.get("email")

    if not mongo.db.users.find_one({"email": friend_email}):
        return jsonify({"error": "Friend not found"}), 404

    if not mongo.db.friendship.find_one(
        {
            "$or": [
                {"sender": email, "recipient": friend_email},
                {"sender": friend_email, "recipient": email},
            ]
        }
    ):
        return jsonify({"error": "Friendship does not exist"}), 404

    friend = mongo.db.users.find_one(
        {"email": friend_email},
        {
            "_id": 0,
            "password": 0,
            "email": 0,
        },
    )

    return jsonify(friend), 200
