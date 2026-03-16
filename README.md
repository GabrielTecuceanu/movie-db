<div align="center">

# MovieDB

</div>

A full-stack movie and TV show discovery platform with social features. Browse films, track what you've watched, rate and review content, and see what your friends are into.

Built with **SvelteKit**, **Flask**, **MongoDB**, and **Redis**, powered by the [TMDB API](https://www.themoviedb.org/documentation/api).

## Features

- **Discover** - Browse popular, top-rated, and upcoming movies and TV shows. Search across movies, shows, and actors.
- **Watchlists** - Save movies and shows you want to watch. Mark them as finished with a rating and review.
- **Favorite People** - Follow actors and creators you like.
- **Friends & Feed** - Add friends, view their profiles, and see a live feed of their activity (new ratings, reviews, list updates).
- **User Profiles** - Tab-based profile pages with watchlists, finished content, and favorite people. Accessible at `/profile/<username>`.

## Quick Start

```bash
docker compose up
```

This builds and starts all services (frontend, backend, MongoDB, Redis) and seeds the database with sample data.

> The backend **drops and re-seeds the database on every restart** - this is development-mode behavior.

### Configuration

| Variable      | Location             | Description                                 |
| ------------- | -------------------- | ------------------------------------------- |
| `USERS_COUNT` | `docker-compose.yml` | Number of fake users to generate on startup |

## Architecture

```
┌─────────────┐     REST API     ┌──────────────┐     ┌───────────┐
│  SvelteKit  │ ◄──────────────► │    Flask     │ ◄──►│  MongoDB  │
│  Frontend   │                  │   Backend    │     └───────────┘
└─────────────┘                  │              │     ┌───────────┐
                                 │              │ ◄──►│   Redis   │
                                 │              │     │  (cache)  │
                                 │              │     └───────────┘
                                 │              │     ┌───────────┐
                                 │              │ ◄──►│ TMDB API  │
                                 └──────────────┘     └───────────┘
```

Each service runs in its own Docker container, orchestrated with Docker Compose.

- **Frontend** - SvelteKit SPA with TailwindCSS, Bits UI components, and Embla Carousel.
- **Backend** - Flask with blueprint-based routing, JWT authentication, and APScheduler for background tasks.
- **MongoDB** - Stores users, friendships, friend requests, and activity feed data.
- **Redis** - Caches TMDB API responses to reduce external calls and improve latency.
- **Faker** - A one-shot container that populates the database with realistic test data (users, friendships, watchlists). Credentials are logged to `/logs/faker_log.txt`.

## API

The backend exposes the following route groups:

| Prefix       | Description                                                            |
| ------------ | ---------------------------------------------------------------------- |
| `/auth`      | Registration, login, account deletion                                  |
| `/protected` | Authenticated user profile and token info                              |
| `/tmdb`      | Movies, TV shows, people, search, recommendations (proxied from TMDB)  |
| `/lists`     | Watchlists, finished lists, favorite people — with ratings and reviews |
| `/friends`   | Friend requests, friend list, friend profiles                          |
| `/info`      | Health check, user lookup                                              |

Full endpoint documentation is in [`API.md`](API.md).

## Tech Stack

| Layer          | Technology                                             |
| -------------- | ------------------------------------------------------ |
| Frontend       | SvelteKit, TailwindCSS, Bits UI, Embla Carousel, Axios |
| Backend        | Flask, PyJWT, Flask-PyMongo, Flask-APScheduler         |
| Database       | MongoDB                                                |
| Cache          | Redis                                                  |
| External API   | TMDB                                                   |
| Infrastructure | Docker, Docker Compose                                 |
