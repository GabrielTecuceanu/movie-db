# Team members:

- Constantin Darius-Andrei 321CA
- Tecuceanu Gabriel-Cristian 321CA

# Introduction

The project is a Svelte-Flask web application that allows users to:

- Search for and discover information about movies, TV shows, and people in the 
industry.
- Add movies and shows to their watchlists, or mark them as finished along with 
a rating and a review. Favourite actors can also be followed.
- Create friendships with other users.
- View the profiles of friends.
- View a live feed which contains the latest activities of the user's friends

# Usage

To start the application run:

```bash
docker compose up
```

It will take a while to build and start all the containers, and run the database 
population script.

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
- Redis: caching requests to the TMDB API

# Members contributions

- Constantin Darius-Andrei:
  - frontend:
    - dynamic routing for individual movies, shows, and people
    - authentication interface and other various components, such as the Titled 
    Carousel
    - profile pages for users
    - added confetti when following an actor!
  - backend:
    - routes that handle adding, removing, and getting lists (movie/TV watchlist,
      favorite people watchlist)
- Tecuceanu Gabriel-Cristian:
  - backend:
    - auth system
    - friend system
    - live feed
    - TMDB integration
    - TMDB requests caching
    - database cleanup script
  - containerization
  - script that populates the database with fake data

# Architecture

Each component of the application lives in its own container:

- frontend
- backend
- mongo
- redis
- faker

Docker Compose is used to manage containers and link them together, creating 
networks and volumes.

The frontend and backend communicate through a REST API.

The frontend is a single page application built using Svelte.

The backend communicates with the TMDB API to get movie and TV show data, 
acting as an intermediary between the frontend and the TMDB API.

We use Redis to cache requests to the TMDB API.

We use MongoDB to store user data, friendships, and friend requests.

We use Faker to populate the database. The backend drops the database every time 
the Flask app is run. Faker waits for the backend to be online and then generates 
users, friendship relationships between the users, and adds movies/TV shows/people 
to the users' lists. All operations are logged in the `/log/faker_log.txt` file 
(here you can find the passwords of the generated users).

Friend requests can have 3 states: pending, accepted, rejected. To clear 
processed requests (accepted or rejected) we have a script that runs every 12 
hours and deletes requests that are older than 1 day. For this, we use the 
APScheduler library.

Received friend requests are displayed in the live feed. Also, when a friend 
makes a change to their lists, a message is added to the live feed.

# Encountered difficulties

- Darius
  - Using a web framework and TypeScript for the first time proved rather difficult
  without any prior experience, but once I understood the structure Svelte works 
  with, development quickly sped up. (This, however, means that I was not using 
  TypeScript until I was half done.)
  - I quickly found out that a frontend-backend split between us was more cumbersome 
  than useful, so I ended up writing backend functions on the fly as they became 
  necessary for the project.
  - Frontend design and centering divs is hell on earth.
- Gabi
  - Learning how to fit together all the services of the application proved to be 
  quite challenging (managin containers, the way they interact, figuring out
  how to only run the database population script once the database is up and running).
