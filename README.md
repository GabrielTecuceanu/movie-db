github link: https://github.com/TecuceanuGabriel/iap4-movie-db

# Team members:

- Constantin Darius-Andrei 321CA
- Tecuceanu Gabriel-Cristian 321CA

# Introduction

The project is a Svelte-Flask web application that allows users to:

- Search for and discover information about movies, TV shows, and people of
  the industry.
- Add movies and shows to their watchlists, or mark them as finished along
  with a rating and a review. Favourite actors can also be followed.
- Create friendships with other users.
- View the profiles of friends.
- View a live feed which contains the latests activities of the user's friends

# Usage

To start the application run:

```bash
docker compose up
```

It will take a while to build and start all the containers, and run the
database population script.

To modify the number of users the script will create, modify the `USERS_COUNT`
environment variable in the `docker-compose.yml` file.

WARNING!!!: The server drops the database every time it starts.

## MONGO credentials

- username: root
- password: root

# Technologies used

- Svelte: the frontend (single page application)
- Flask: the backend
- Faker: generating fake data to populate the database
- APScheduler: scheduling tasks (script that cleans the database)
- JWT: authorization
- TMDB (external API): for information about the cinema industry
- MongoDB: the database
- Docker and docker-compose: containerization, and as a development environment
- Redis: caching requests to the TMDB api

# Members contributions

- Constantin Darius-Andrei:
  - frontend:
    - dynamic routing for individual movies, shows, and people
    - authentifcation interface and other various components, such as the Titled Carousel
    - profile pages for users
    - added confetti when following an actor!
  - backend:
    - routes that handle adding, removing and getting lists (movie/tv watchlist,
      favorite people watchlist)
- Tecuceanu Gabriel-Cristian:
  - backend:
    - auth system
    - friend system
    - live feed
    - tmdb integration
    - tmdb requests caching
    - database cleanup script
  - containerization
  - script that populates the database with fake data

# Architecture

each component of the application lives in its own container:

- frontend
- backend
- mongo
- redis
- faker

docker compose is used to manage containers and link them together,
creating networks and volumes.

The frontend and backend communicate through a REST API.

The frontend is a single page application built using Svelte.

The backend communicates with the TMDB api to get movie and tv show data,
acting as an intermediary between the frontend and the TMDB api.

We use Redis to cache requests to the TMDB api.

We use MongoDB to store user data, friendships, and friend requests.

We use faker to populate the database. The backend drops the database every
time the flask app is run. Faker waits for the backend to be online and than
it generates users, friendship relationships between the users, and adds
movies/tv shows/people to the users lists. All operations are logged in the
/log/faker_log.txt file (here you can find the passwords of the generated users).

Friend requests can have 3 states: pending, accepted, rejected. To clear
processed requests (accepted or rejected) we have a script that runs every
12 hours and deletes requests that are older than 1 day. For this we use
the APScheduler library.

Received friend requests are displayed in the live feed. Also when a friend
makes a change to their lists, a message is added to the live feed.

# Encoutered difficulties

??
