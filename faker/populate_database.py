"""
This script is used to populate the database with random data. It creates users,
friendships between them and populates their watchlists and favourite people lists
with random movies, tv shows and people. It also adds some of them to the
finished lists with a rating and a review. It uses the Faker library to generate
random data, and logs the operations to a file.
"""

from faker import Faker

import requests
import time
import os

BASE_URL = os.environ.get("BASE_URL")
USER_COUNT = int(os.environ.get("USER_COUNT", 10))


fake = Faker()

log = open("/app/logs/faker_log.txt", "w")

users = []


def create_user():
    """Create a new user, add it to the users list and log the operation."""

    username = fake.user_name()
    email = fake.email()
    password = fake.password()

    body = {"username": username, "email": email, "password": password}

    response = requests.post(f"{BASE_URL}/register", json=body)

    if response.status_code != 201:
        log.write(
            f"Failed to create user {username} with email {email} and password {password}\n"
        )
        return

    log.write(f"User {username} created with email {email} and password {password}\n")

    users.append(body)


def create_users():
    """Create USER_COUNT number of users."""

    for _ in range(USER_COUNT):
        create_user()


def login(email, password):
    """Login and return the authentication token.

    Parameters:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        str: The authentication token or None.
    """

    body = {"email": email, "password": password}

    response = requests.post(f"{BASE_URL}/login", json=body)

    if response.status_code != 200:
        return None

    return response.json()["token"]


fd_requests = []


def send_friend_request(sender, receiver, token):
    """Send a friend request from sender to receiver, add the request to
    fd_requests and log the operation.

    Parameters:
        sender (dict): The sender of the friend request (must contain email).
        receiver (dict): The receiver of the friend request (must contain email).
        token (str): The authentication token of the sender.
    """

    body = {
        "email": receiver["email"],
    }

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(f"{BASE_URL}/friends/request", json=body, headers=headers)

    if response.status_code != 200:
        log.write(
            f"{sender['email']} couldn't send friend request to {receiver['email']}\n"
        )
        return

    log.write(f"{sender['email']} sent friend request to {receiver['email']}\n")

    fd_requests.append({"sender": sender, "recipient": receiver})


def process_friend_request(request):
    """Chose randomly to accept or reject the friend request and log the
    operation.

    Parameters:
        request (dict): The friend request to process.
    """

    sender = request["sender"]
    recipient = request["recipient"]

    token = login(recipient["email"], recipient["password"])

    if token is None:
        return

    decision = fake.random_element(["accept", "reject"])

    body = {
        "email": sender["email"],
        "response": decision,
    }

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(f"{BASE_URL}/friends/respond", json=body, headers=headers)

    if response.status_code != 200:
        log.write(
            f"couldn't process request between {sender['email']} and {recipient['email']}\n"
        )
        return

    if decision == "accept":
        log.write(
            f"Friend request between {sender['email']} and {recipient['email']} accepted\n"
        )
        return

    log.write(
        f"Friend request between {sender['email']} and {recipient['email']} rejected\n"
    )


def create_frienships():
    """Iterate over the users list and send friend requests to random users.
    After that iterate over fd_requests and process the them."""

    for user in users:
        token = login(user["email"], user["password"])
        if token is None:
            continue

        for _ in range(USER_COUNT // 4):
            friend = fake.random_element(users)
            send_friend_request(user, friend, token)

    for request in fd_requests:
        process_friend_request(request)


def add_movie_to_list(token, movie):
    """Add a movie to the watchlist of the user who owns the token

    Parameters:
        token (str): The authentication token of the user.
        movie (dict): The movie to add to the watchlist.
    """

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(
        f"{BASE_URL}/watchlist/movie/add/{movie["id"]}", headers=headers
    )

    if response.status_code != 200:
        log.write(f"Couldn't add movie {movie['title']} to watchlist\n")
        return

    log.write(f"Movie {movie['title']} added to watchlist\n")


def add_tv_show_to_list(token, tv_show):
    """Add a tv show to the watchlist of the user who owns the token

    Parameters:
        token (str): The authentication token of the user.
        tv_show (dict): The tv show to add to the watchlist.
    """

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(
        f"{BASE_URL}/watchlist/tv/add/{tv_show["id"]}", headers=headers
    )

    if response.status_code != 200:
        log.write(f"Couldn't add tv show {tv_show['name']} to watchlist\n")
        return

    log.write(f"Tv show {tv_show['name']} added to watchlist\n")


def add_person_to_list(token, person):
    """Add a person to the favourites list of the user who owns the token

    Parameters:
        token (str): The authentication token of the user.
        person (dict): The person to add to the favourites list.
    """

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(
        f"{BASE_URL}/favourite/people/add/{person["id"]}", headers=headers
    )

    if response.status_code != 200:
        log.write(f"Couldn't add person {person['name']} to favourites\n")
        return

    log.write(f"Person {person['name']} added to favourites\n")


def add_movie_to_finished_list(token, movie):
    """Add a movie to the finished list of the user who owns the token, also
    add a rating and a review for that movie

    Parameters:
        token (str): The authentication token of the user.
        movie (dict): The movie to add to the finished list.
    """

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(
        f"{BASE_URL}/finished/movie/add/{movie["id"]}", headers=headers
    )

    if response.status_code != 200:
        log.write(f"Couldn't add movie {movie['title']} to finished list\n")
        return

    rating = float(fake.random_int(0, 10))

    response = requests.post(
        f"{BASE_URL}/finished/movie/{movie['id']}/rate/{rating}",
        headers=headers,
    )

    if response.status_code != 200:
        log.write(f"Couldn't rate movie {movie['title']}, {response.json}\n")

    body = {
        "review": fake.text(),
    }

    response = requests.post(
        f"{BASE_URL}/finished/movie/{movie['id']}/review", json=body, headers=headers
    )

    if response.status_code != 200:
        log.write(f"Couldn't review movie {movie['title']}\n")
        return

    log.write(f"Movie {movie['title']} added to finished list\n")


def add_tv_show_to_finished_list(token, tv_show):
    """Add a tv show to the finished list of the user who owns the token, also
    add a rating and a review for that tv show

    Parameters:
        token (str): The authentication token of the user.
        tv_show (dict): The tv show to add to the finished list.
    """

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(
        f"{BASE_URL}/finished/tv/add/{tv_show["id"]}", headers=headers
    )

    if response.status_code != 200:
        log.write(f"Couldn't add tv show {tv_show['name']} to finished list\n")
        return

    rating = float(fake.random_int(0, 10))

    response = requests.post(
        f"{BASE_URL}/finished/show/{tv_show['id']}/rate/{rating}",
        headers=headers,
    )

    if response.status_code != 200:
        log.write(f"Couldn't rate tv show {tv_show['name']}\n")
        return

    body = {
        "review": fake.text(),
    }

    response = requests.post(
        f"{BASE_URL}/finished/show/{tv_show['id']}/review", json=body, headers=headers
    )

    if response.status_code != 200:
        log.write(f"Couldn't review tv show {tv_show['name']}\n")
        return

    log.write(f"Tv show {tv_show['name']} added to finished list\n")


def populate_users_lists():
    """Iterate over the users list and add random movies, tv shows and people
    to their lists. Randomly add some of them to the finished lists."""

    movies = (
        requests.get(f"{BASE_URL}/movie/popular/{fake.random_int(1, 10)}")
        .json()
        .get("results")
    )
    tv_shows = (
        requests.get(f"{BASE_URL}/tv/popular/{fake.random_int(1, 10)}")
        .json()
        .get("results")
    )
    people = requests.get(f"{BASE_URL}/person/popular").json().get("results")

    for user in users:
        token = login(user["email"], user["password"])
        if token is None:
            continue

        for _ in range(5):
            movie = fake.random_element(movies)
            tv_show = fake.random_element(tv_shows)
            person = fake.random_element(people)

            add_movie_to_list(token, movie)
            add_tv_show_to_list(token, tv_show)
            add_person_to_list(token, person)

            if fake.boolean(10):
                add_movie_to_finished_list(token, movie)
            if fake.boolean(10):
                add_tv_show_to_finished_list(token, tv_show)


def populate_database():
    """Create users, friendships and populate the users lists."""

    create_users()
    create_frienships()
    populate_users_lists()
    pass


def wait_for_backend():
    """Wait for the backend to become available."""

    BACKEND_WAIT_TIME = 5
    WAIT_FOR_BACKEND_RETRIES = 10

    retries = 0
    while retries < WAIT_FOR_BACKEND_RETRIES:
        try:
            response = requests.get(f"{BASE_URL}/")
            if response.status_code == 200:
                log.write("Backend is online.\n")
                return
        except requests.ConnectionError:
            log.write("Backend is not reachable. Retrying...\n")
        time.sleep(BACKEND_WAIT_TIME)
        retries += 1

    raise Exception("Backend did not become available in time.")


if __name__ == "__main__":
    wait_for_backend()
    populate_database()
    pass
