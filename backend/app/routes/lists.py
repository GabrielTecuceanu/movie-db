from flask import Blueprint, request, jsonify

from app.extensions import mongo
from app.services.auth_service import verify_token
from app.services.feed_service import add_to_friends_feed_thread

from app.models.feed_item import FeedItem

from datetime import datetime


lists = Blueprint("lists", __name__)


@lists.route("/watchlist/movie/add/<int:movie_id>", methods=["POST"])
def add_to_watchlist(movie_id):
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
        return jsonify({"error": "User not found"}), 404

    watchlist = user.get("movie_watchlist", [])

    if movie_id in watchlist:
        return jsonify({"error": "Movie already in watchlist"}), 400

    watchlist.append(movie_id)

    mongo.db.users.update_one(
        {"email": email},
        {"$set": {"movie_watchlist": watchlist}},
    )

    # Notify friends about the addition to the watchlist
    add_to_friends_feed_thread(
        email,
        FeedItem(
            email,
            f"added {movie_id} to their watchlist",
            datetime.now(),
        ),
    )

    return jsonify({"message": "Movie added to watchlist"}), 200


@lists.route("/finished/movie/add/<int:movie_id>", methods=["POST"])
def add_to_finished(movie_id):
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
        return jsonify({"error": "User not found"}), 404

    finished = user.get("movie_finished", [])

    for movie in finished:
        if movie.get("movie_id") == movie_id:
            return jsonify({"error": "Movie already in finished"}), 400

    watchlist = user.get("movie_watchlist", [])
    if movie_id in watchlist:
        remove_from_watchlist(movie_id)

    finished.append({"movie_id": movie_id, "rating": 0, "review": ""})

    mongo.db.users.update_one(
        {"email": email},
        {"$set": {"movie_finished": finished}},
    )

    add_to_friends_feed_thread(
        email,
        FeedItem(
            email,
            f"finished watching {movie_id}",
            datetime.now(),
        ),
    )

    return jsonify({"message": "Movie added to finished"}), 200


@lists.route("/watchlist/movie/remove/<int:movie_id>", methods=["POST"])
def remove_from_watchlist(movie_id):
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token is required"}), 400

    token = token.split(" ")[1]

    payload, error = verify_token(token)

    if error:
        return jsonify(error), 400

    email = payload["email"]

    if not movie_id:
        return jsonify({"error": "Movie ID is required"}), 400

    user = mongo.db.users.find_one({"email": email})

    if not user:
        return jsonify({"error": "User not found"}), 404

    watchlist = user.get("movie_watchlist", [])

    watchlist.remove(movie_id)

    mongo.db.users.update_one(
        {"email": email},
        {"$set": {"movie_watchlist": watchlist}},
    )

    return jsonify({"message": "Movie removed from watchlist"}), 200


@lists.route("/finished/movie/remove/<int:movie_id>", methods=["POST"])
def remove_from_finished(movie_id):
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
        return jsonify({"error": "User not found"}), 404

    finished = user.get("movie_finished", [])

    movie_to_remove = next(
        (movie for movie in finished if movie.get("movie_id") == movie_id), None
    )

    if not movie_to_remove:
        return jsonify({"error": "Movie not in finished"}), 400

    finished.remove(movie_to_remove)

    mongo.db.users.update_one(
        {"email": email},
        {"$set": {"movie_finished": finished}},
    )

    return jsonify({"message": "Movie removed from finished"}), 200


@lists.route("/watchlist/movie", methods=["GET"])
def get_watchlist():
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
        return jsonify({"error": "User not found"}), 404

    watchlist = user.get("movie_watchlist", [])

    return jsonify(watchlist), 200


@lists.route("/watchlist/movie/<int:movie_id>", methods=["GET"])
def is_on_watchlist(movie_id):
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
        return jsonify({"error": "User not found"}), 404

    watchlist = user.get("movie_watchlist", [])

    if movie_id in watchlist:
        return jsonify({"success": True}), 200

    return jsonify({"success": False}), 200


@lists.route("/finished/movie", methods=["GET"])
def get_finished():
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
        return jsonify({"error": "User not found"}), 404

    finished = user.get("movie_finished", [])

    return jsonify(finished), 200


@lists.route("/finished/movie/<int:movie_id>", methods=["GET"])
def is_finished(movie_id):
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
        return jsonify({"error": "User not found"}), 404

    finished = user.get("movie_finished", [])

    for movie in finished:
        if movie.get("movie_id") == movie_id:
            return jsonify({"success": True, "movie": movie}), 200

    return jsonify({"success": False}), 200


@lists.route("/watchlist/tv/add/<int:show_id>", methods=["POST"])
def add_tv_to_watchlist(show_id):
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
        return jsonify({"error": "User not found"}), 404

    watchlist = user.get("tv_watchlist", [])

    if show_id in watchlist:
        return jsonify({"error": "TV show already in watchlist"}), 400

    watchlist.append(show_id)

    mongo.db.users.update_one(
        {"email": email},
        {"$set": {"tv_watchlist": watchlist}},
    )

    add_to_friends_feed_thread(
        email,
        FeedItem(
            email,
            f"added {show_id} to their watchlist",
            datetime.now(),
        ),
    )

    return jsonify({"message": "TV show added to watchlist"}), 200


@lists.route("/finished/tv/add/<int:show_id>", methods=["POST"])
def add_tv_to_finished(show_id):
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
        return jsonify({"error": "User not found"}), 404

    finished = user.get("tv_finished", [])

    for show in finished:
        if show.get("show_id") == show_id:
            return jsonify({"error": "TV show already in finished"}), 400

    watchlist = user.get("tv_watchlist", [])
    if show_id in watchlist:
        remove_tv_from_watchlist(show_id)

    finished.append({"show_id": show_id, "rating": 0, "review": ""})

    mongo.db.users.update_one(
        {"email": email},
        {"$set": {"tv_finished": finished}},
    )

    add_to_friends_feed_thread(
        email,
        FeedItem(
            email,
            f"finished watching {show_id}",
            datetime.now(),
        ),
    )

    return jsonify({"message": "TV show added to finished"}), 200


@lists.route("/watchlist/tv/remove/<int:show_id>", methods=["POST"])
def remove_tv_from_watchlist(show_id):
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
        return jsonify({"error": "User not found"}), 404

    watchlist = user.get("tv_watchlist", [])

    if show_id not in watchlist:
        return jsonify({"error": "TV show not in watchlist"}), 400

    watchlist.remove(show_id)

    mongo.db.users.update_one(
        {"email": email},
        {"$set": {"tv_watchlist": watchlist}},
    )

    return jsonify({"message": "TV show removed from watchlist"}), 200


@lists.route("/finished/tv/remove/<int:show_id>", methods=["POST"])
def remove_tv_from_finished(show_id):
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
        return jsonify({"error": "User not found"}), 404

    finished = user.get("tv_finished", [])

    show_to_remove = next(
        (movie for movie in finished if movie.get("show_id") == show_id), None
    )

    if not show_to_remove:
        return jsonify({"error": "TV show not in finished"}), 400

    finished.remove(show_to_remove)

    mongo.db.users.update_one(
        {"email": email},
        {"$set": {"tv_finished": finished}},
    )

    return jsonify({"message": "TV show removed from finished"}), 200


@lists.route("/watchlist/tv", methods=["GET"])
def get_tv_watchlist():
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
        return jsonify({"error": "User not found"}), 404

    watchlist = user.get("tv_watchlist", [])

    return jsonify(watchlist), 200


@lists.route("/watchlist/tv/<int:show_id>", methods=["GET"])
def is_tv_on_watchlist(show_id):
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
        return jsonify({"error": "User not found"}), 404

    watchlist = user.get("tv_watchlist", [])

    if show_id in watchlist:
        return jsonify({"success": True}), 200

    return jsonify({"success": False}), 200


@lists.route("/finished/tv", methods=["GET"])
def get_tv_finished():
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
        return jsonify({"error": "User not found"}), 404

    finished = user.get("tv_finished", [])

    return jsonify(finished), 200


@lists.route("/finished/tv/<int:show_id>", methods=["GET"])
def is_tv_finished(show_id):
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
        return jsonify({"error": "User not found"}), 404

    finished = user.get("tv_finished", [])
    for show in finished:
        if show.get("show_id") == show_id:
            return jsonify({"success": True, "show": show}), 200

    return jsonify({"success": False}), 200


@lists.route("/favourite/people/add/<int:person_id>", methods=["POST"])
def add_favourite_person(person_id):
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
        return jsonify({"error": "User not found"}), 404

    favourite = user.get("favourite_people", [])

    if person_id in favourite:
        return jsonify({"error": "Person already favourited"}), 400

    favourite.append(person_id)

    mongo.db.users.update_one(
        {"email": email},
        {"$set": {"favourite_people": favourite}},
    )

    add_to_friends_feed_thread(
        email,
        FeedItem(
            email,
            f"added {person_id} to their favourites",
            datetime.now(),
        ),
    )

    return jsonify({"message": "Person favourited"}), 200


@lists.route("/favourite/people/remove/<int:person_id>", methods=["POST"])
def remove_favourite_person(person_id):
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
        return jsonify({"error": "User not found"}), 404

    favourite = user.get("favourite_people", [])

    if person_id not in favourite:
        return jsonify({"error": "Person not favourited"}), 400

    favourite.remove(person_id)

    mongo.db.users.update_one(
        {"email": email},
        {"$set": {"favourite_people": favourite}},
    )

    return jsonify({"message": "Person removed from favourites"}), 200


@lists.route("/favourite/people", methods=["GET"])
def get_favourite_people():
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
        return jsonify({"error": "User not found"}), 404

    people = user.get("favourite_people", [])

    return jsonify(people), 200


@lists.route("/favourite/people/<int:person_id>", methods=["GET"])
def is_favourite_person(person_id):
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
        return jsonify({"error": "User not found"}), 404

    people = user.get("favourite_people", [])

    if person_id in people:
        return jsonify({"success": True}), 200

    return jsonify({"success": False}), 200


@lists.route(
    "/finished/movie/<int:movie_id>/rate/<float(signed=False):score>",
    methods=["POST"],
)
def change_movie_rating(movie_id, score):
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
        return jsonify({"error": "User not found"}), 404

    finished = user.get("movie_finished", [])

    movie_entry = next(
        (movie for movie in finished if movie.get("movie_id") == movie_id), None
    )

    if not movie_entry:
        return jsonify({"error": "Movie not found in finished list"}), 404

    if not (0 <= score <= 10):
        return jsonify({"error": "Rating score must be between 0 and 10"}), 400

    movie_entry["rating"] = round(score, 1)

    mongo.db.users.update_one(
        {"email": email},
        {"$set": {"movie_finished": finished}},
    )

    return (
        jsonify({"message": f"Rating updated to {score} for movie {movie_id}"}),
        200,
    )


@lists.route(
    "/finished/tv/<int:show_id>/rate/<float(signed=False):score>",
    methods=["POST"],
)
def change_show_rating(show_id, score):
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
        return jsonify({"error": "User not found"}), 404

    finished = user.get("tv_finished", [])

    show_entry = next(
        (show for show in finished if show.get("show_id") == show_id), None
    )

    if not show_entry:
        return jsonify({"error": "Show not found in finished list"}), 404

    if not (0 <= score <= 10):
        return jsonify({"error": "Rating score must be between 0 and 10"}), 400

    show_entry["rating"] = score

    mongo.db.users.update_one(
        {"email": email},
        {"$set": {"tv_finished": finished}},
    )

    return (
        jsonify({"message": f"Rating updated to {score} for show {show_id}"}),
        200,
    )


@lists.route("/finished/movie/<int:movie_id>/review", methods=["POST"])
def change_movie_review(movie_id):
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
        return jsonify({"error": "User not found"}), 404

    data = request.json
    review = data.get("review")

    if not review:
        return jsonify({"error": "Review is required"}), 400

    finished = user.get("movie_finished", [])

    movie_entry = next(
        (movie for movie in finished if movie.get("movie_id") == movie_id), None
    )

    if not movie_entry:
        return jsonify({"error": "Movie not found in finished list"}), 404

    movie_entry["review"] = review

    mongo.db.users.update_one(
        {"email": email},
        {"$set": {"movie_finished": finished}},
    )

    return jsonify({"message": f"Review updated for movie {movie_id}"}), 200


@lists.route("/finished/tv/<int:show_id>/review", methods=["POST"])
def change_tv_review(show_id):
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
        return jsonify({"error": "User not found"}), 404

    data = request.json
    review = data.get("review")

    if not review:
        return jsonify({"error": "Review is required"}), 400

    finished = user.get("tv_finished", [])

    show_entry = next(
        (show for show in finished if show.get("show_id") == show_id), None
    )

    if not show_entry:
        return jsonify({"error": "Show not found in finished list"}), 404

    show_entry["review"] = review

    mongo.db.users.update_one(
        {"email": email},
        {"$set": {"tv_finished": finished}},
    )

    return jsonify({"message": f"Review updated for show {show_id}"}), 200
