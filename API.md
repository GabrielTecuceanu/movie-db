<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

- [API Reference](#api-reference)
  - [Authentication](#authentication)
    - [`POST /register`](#post-register)
    - [`POST /login`](#post-login)
    - [`POST /delete_account`](#post-delete_account)
  - [Server Info](#server-info)
    - [`GET /`](#get-)
    - [`GET /get_all`](#get-get_all)
    - [`GET /get_user/username/<string:username>`](#get-get_userusernamestringusername)
    - [`GET /get_user/email/<string:email>`](#get-get_useremailstringemail)
  - [Protected](#protected)
    - [`GET /profile`](#get-profile)
  - [TMDB integration](#tmdb-integration)
  - [Configuration](#configuration)
    - [`GET /configuration`](#get-configuration)
    - [`GET /genre/movie/list`](#get-genremovielist)
    - [`GET /genre/tv/list`](#get-genretvlist)
  - [Movies](#movies)
    - [`GET /movie/details/{movie_id}`](#get-moviedetailsmovie_id)
    - [`GET /movie/popular/{page}`](#get-moviepopularpage)
    - [`GET /movie/top_rated/{page}`](#get-movietop_ratedpage)
    - [`GET /movie/upcoming/{page}`](#get-movieupcomingpage)
    - [`GET /movie/{movie_id}/images`](#get-moviemovie_idimages)
    - [`GET /movie/{movie_id}/videos`](#get-moviemovie_idvideos)
    - [`GET /movie/{movie_id}/recommendations`](#get-moviemovie_idrecommendations)
    - [`GET /movie/{movie_id}/similar`](#get-moviemovie_idsimilar)
  - [TV Shows](#tv-shows)
    - [`GET /tv/popular/{page}`](#get-tvpopularpage)
    - [`GET /tv/top_rated/{page}`](#get-tvtop_ratedpage)
    - [`GET /tv/details/{show_id}`](#get-tvdetailsshow_id)
    - [`GET /tv/{show_id}/images`](#get-tvshow_idimages)
    - [`GET /tv/{show_id}/recommendations`](#get-tvshow_idrecommendations)
    - [`GET /tv/{show_id}/similar`](#get-tvshow_idsimilar)
  - [People](#people)
    - [`GET /person/details/{person_id}`](#get-persondetailsperson_id)
    - [`GET /person/popular`](#get-personpopular)
    - [`GET /person/{person_id}/images`](#get-personperson_idimages)
    - [`GET /person/{person_id}/credits`](#get-personperson_idcredits)
    - [`GET /person/{person_id}/tagged_images`](#get-personperson_idtagged_images)
  - [Search](#search)
    - [`GET /search/multi/{query}/{page}`](#get-searchmultiquerypage)
    - [`GET /search/movie/{query}/{page}`](#get-searchmoviequerypage)
    - [`GET /search/tv/{query}/{page}`](#get-searchtvquerypage)
  - [Lists](#lists)
    - [`POST /watchlist/movie/add/<int:movie_id>`](#post-watchlistmovieaddintmovie_id)
    - [`POST /finished/movie/add/<int:movie_id>`](#post-finishedmovieaddintmovie_id)
    - [`POST /watchlist/movie/remove/<int:movie_id>`](#post-watchlistmovieremoveintmovie_id)
    - [`POST /finished/movie/remove/<int:movie_id>`](#post-finishedmovieremoveintmovie_id)
    - [`GET /watchlist/movie`](#get-watchlistmovie)
    - [`GET /watchlist/movie/<int:movie_id>`](#get-watchlistmovieintmovie_id)
    - [`GET /finished/movie`](#get-finishedmovie)
    - [`GET /finished/movie/<int:movie_id>`](#get-finishedmovieintmovie_id)
    - [`POST /watchlist/tv/add/<int:show_id>`](#post-watchlisttvaddintshow_id)
    - [`POST /finished/tv/add/<int:show_id>`](#post-finishedtvaddintshow_id)
    - [`POST /watchlist/tv/remove/<int:show_id>`](#post-watchlisttvremoveintshow_id)
    - [`POST /finished/tv/remove/<int:show_id>`](#post-finishedtvremoveintshow_id)
    - [`GET /watchlist/tv`](#get-watchlisttv)
    - [`GET /finished/tv`](#get-finishedtv)
    - [`POST /favourite/people/add/<int:person_id>`](#post-favouritepeopleaddintperson_id)
    - [`POST /favourite/people/remove/<int:person_id>`](#post-favouritepeopleremoveintperson_id)
    - [`GET /favourite/people`](#get-favouritepeople)
    - [`GET /favourite/people/<int:person_id>`](#get-favouritepeopleintperson_id)
    - [`POST /finished/movie/<int:movie_id>/rate/<float(signed=False):score>`](#post-finishedmovieintmovie_idratefloatsignedfalsescore)
    - [`POST /finished/show/<int:show_id>/rate/<float(signed=False):score>`](#post-finishedshowintshow_idratefloatsignedfalsescore)
    - [`POST /finished/movie/<int:movie_id>/review`](#post-finishedmovieintmovie_idreview)
  - [Friends](#friends)
    - [`POST /friends/request`](#post-friendsrequest)
    - [`GET /friends/get_pending_requests`](#get-friendsget_pending_requests)
    - [`POST /friends/respond`](#post-friendsrespond)
    - [`GET /friends/get_friends`](#get-friendsget_friends)
    - [`POST /friends/remove`](#post-friendsremove)
    - [`POST /friends/is_friend`](#post-friendsis_friend)
    - [`POST /friends/get_friend_profile`](#post-friendsget_friend_profile)

<!-- TOC end -->

<!-- TOC --><a name="api-reference"></a>

# API Reference

<!-- TOC --><a name="authentication"></a>

## Authentication

<!-- TOC --><a name="post-register"></a>

### `POST /register`

**Description:** Registers a new user.

**Parameters:**

- `username` (string): The username of the new user.
- `email` (string): The email of the new user.
- `password` (string): The password of the new user.

**Body:**

```json
{
  "username": "exampleuser",
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**

- **201 Created:**
  ```json
  {
    "message": "User registered successfully",
    "token": "generated_token"
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Username is required"
  }
  ```
  ```json
  {
    "error": "Email is required"
  }
  ```
  ```json
  {
    "error": "Password is required"
  }
  ```
  ```json
  {
    "error": "Email already exists"
  }
  ```

---

<!-- TOC --><a name="post-login"></a>

### `POST /login`

**Description:** Logs in an existing user.

**Parameters:**

- `email` (string): The email of the user.
- `password` (string): The password of the user.

**Body:**

```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**

- **200 OK:**
  ```json
  {
    "token": "generated_token"
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Email is required"
  }
  ```
  ```json
  {
    "error": "Password is required"
  }
  ```
  ```json
  {
    "error": "Invalid password"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "User not found"
  }
  ```

---

<!-- TOC --><a name="post-delete_account"></a>

### `POST /delete_account`

**Description:** Deletes an existing user account.

**Parameters:**

- `email` (string): The email of the user.
- `password` (string): The password of the user.

**Body:**

```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**

- **200 OK:**
  ```json
  {
    "message": "User deleted successfully"
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Email is required"
  }
  ```
  ```json
  {
    "error": "Password is required"
  }
  ```
  ```json
  {
    "error": "Invalid password
  ```

<!-- TOC --><a name="server-info"></a>

## Server Info

<!-- TOC --><a name="get-"></a>

### `GET /`

**Description:** Checks if the server is online.

**Response:**

- **200 OK:**
  ```json
  {
    "message": "server is online"
  }
  ```

---

<!-- TOC --><a name="get-get_all"></a>

### `GET /get_all`

**Description:** Retrieves a list of all users without sensitive information.

**Response:**

- **200 OK:**
  ```json
  [
    {
      "username": "exampleuser"
    },
    ...
  ]
  ```

<!-- TOC --><a name="get-get_userusernamestringusername"></a>

### `GET /get_user/username/<string:username>`

**Description:** Retrieves a user's information.

**Response:**

- **200 OK:**
  ```json
  {
    "username": "exampleuser",
    "email": "email@bla.com",
    "movie_watchlist": [],
    "tv_watchlist": [],
    "movie_finished": [],
    "tv_finished": [],
    "favourite_people": [],
    "feed": []
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Username does not exist"
  }
  ```

---

<!-- TOC --><a name="get-get_useremailstringemail"></a>

## `GET /get_user/email/<string:email>`

**Description:** Retrieves a user's information.

**Response:**

- **200 OK:**
  ```json
  {
    "username": "exampleuser",
    "email": "email@bla.com",
    "movie_watchlist": [],
    "tv_watchlist": [],
    "movie_finished": [],
    "tv_finished": [],
    "favourite_people": [],
    "feed": []
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Email is not registered"
  }
  ```

<!-- TOC --><a name="protected"></a>

## Protected

<!-- TOC --><a name="get-profile"></a>

### `GET /profile`

**Description:** Retrieves the profile information of the authenticated user.

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Response:**

- **200 OK:**
  ```json
  {
    "username": "exampleuser",
    "other_field": "value",
    ...
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Token is required"
  }
  ```
  ```json
  {
    "error": "Invalid token"
  }
  ```

<!-- TOC --><a name="tmdb-integration"></a>

## TMDB integration

<!-- TOC --><a name="configuration"></a>

## Configuration

<!-- TOC --><a name="get-configuration"></a>

### `GET /configuration`

**Description:** Retrieves TMDB API configuration information.
**Response:**

- **200 OK:**
  ```json
  {
    // TMDB configuration data
  }
  ```

---

<!-- TOC --><a name="get-genremovielist"></a>

### `GET /genre/movie/list`

**Description:** Retrieves a list of all movie genres.
**Response:**

- **200 OK:**
  ```json
  {
    "genres": [
      {
        "id": 28,
        "name": "Action"
      }
      ...
    ]
  }
  ```

---

<!-- TOC --><a name="get-genretvlist"></a>

### `GET /genre/tv/list`

**Description:** Retrieves a list of all TV show genres.
**Response:**

- **200 OK:**
  ```json
  {
    "genres": [
      {
        "id": 10759,
        "name": "Action & Adventure"
      }
      ...
    ]
  }
  ```

<!-- TOC --><a name="movies"></a>

## Movies

<!-- TOC --><a name="get-moviedetailsmovie_id"></a>

### `GET /movie/details/{movie_id}`

**Description:** Retrieves detailed information about a specific movie.
**Parameters:**

- `movie_id` (integer): The ID of the movie.

---

<!-- TOC --><a name="get-moviepopularpage"></a>

### `GET /movie/popular/{page}`

**Description:** Retrieves a list of popular movies with runtime information.
**Parameters:**

- `page` (integer): The page number for pagination.

---

<!-- TOC --><a name="get-movietop_ratedpage"></a>

### `GET /movie/top_rated/{page}`

**Description:** Retrieves a list of top-rated movies.
**Parameters:**

- `page` (integer): The page number for pagination.

---

<!-- TOC --><a name="get-movieupcomingpage"></a>

### `GET /movie/upcoming/{page}`

**Description:** Retrieves a list of upcoming movies.
**Parameters:**

- `page` (integer): The page number for pagination.

---

<!-- TOC --><a name="get-moviemovie_idimages"></a>

### `GET /movie/{movie_id}/images`

**Description:** Retrieves images associated with a specific movie.
**Parameters:**

- `movie_id` (integer): The ID of the movie.

---

<!-- TOC --><a name="get-moviemovie_idvideos"></a>

### `GET /movie/{movie_id}/videos`

**Description:** Retrieves videos associated with a specific movie.
**Parameters:**

- `movie_id` (integer): The ID of the movie.

---

<!-- TOC --><a name="get-moviemovie_idrecommendations"></a>

### `GET /movie/{movie_id}/recommendations`

**Description:** Retrieves movie recommendations based on a specific movie.
**Parameters:**

- `movie_id` (integer): The ID of the movie.

---

<!-- TOC --><a name="get-moviemovie_idsimilar"></a>

### `GET /movie/{movie_id}/similar`

**Description:** Retrieves movies similar to a specific movie.
**Parameters:**

- `movie_id` (integer): The ID of the movie.

<!-- TOC --><a name="tv-shows"></a>

## TV Shows

<!-- TOC --><a name="get-tvpopularpage"></a>

### `GET /tv/popular/{page}`

**Description:** Retrieves a list of popular TV shows.
**Parameters:**

- `page` (integer): The page number for pagination.

---

<!-- TOC --><a name="get-tvtop_ratedpage"></a>

### `GET /tv/top_rated/{page}`

**Description:** Retrieves a list of top-rated TV shows.
**Parameters:**

- `page` (integer): The page number for pagination.

---

<!-- TOC --><a name="get-tvdetailsshow_id"></a>

### `GET /tv/details/{show_id}`

**Description:** Retrieves detailed information about a specific TV show.
**Parameters:**

- `show_id` (integer): The ID of the TV show.

---

<!-- TOC --><a name="get-tvshow_idimages"></a>

### `GET /tv/{show_id}/images`

**Description:** Retrieves images associated with a specific TV show.
**Parameters:**

- `show_id` (integer): The ID of the TV show.

---

<!-- TOC --><a name="get-tvshow_idrecommendations"></a>

### `GET /tv/{show_id}/recommendations`

**Description:** Retrieves TV show recommendations based on a specific show.
**Parameters:**

- `show_id` (integer): The ID of the TV show.

---

<!-- TOC --><a name="get-tvshow_idsimilar"></a>

### `GET /tv/{show_id}/similar`

**Description:** Retrieves TV shows similar to a specific show.
**Parameters:**

- `show_id` (integer): The ID of the TV show.

<!-- TOC --><a name="people"></a>

## People

<!-- TOC --><a name="get-persondetailsperson_id"></a>

### `GET /person/details/{person_id}`

**Description:** Retrieves detailed information about a specific person.
**Parameters:**

- `person_id` (integer): The ID of the person.

---

<!-- TOC --><a name="get-personpopular"></a>

### `GET /person/popular`

**Description:** Retrieves a list of popular people.

---

<!-- TOC --><a name="get-personperson_idimages"></a>

### `GET /person/{person_id}/images`

**Description:** Retrieves images of a specific person.
**Parameters:**

- `person_id` (integer): The ID of the person.

---

<!-- TOC --><a name="get-personperson_idcredits"></a>

### `GET /person/{person_id}/credits`

**Description:** Retrieves combined credits for a specific person.
**Parameters:**

- `person_id` (integer): The ID of the person.

---

<!-- TOC --><a name="get-personperson_idtagged_images"></a>

### `GET /person/{person_id}/tagged_images`

**Description:** Retrieves images where a specific person is tagged.
**Parameters:**

- `person_id` (integer): The ID of the person.

<!-- TOC --><a name="search"></a>

## Search

<!-- TOC --><a name="get-searchmultiquerypage"></a>

### `GET /search/multi/{query}/{page}`

**Description:** Searches across movies, TV shows, and people.
**Parameters:**

- `query` (string): The search query.
- `page` (integer): The page number for pagination.

---

<!-- TOC --><a name="get-searchmoviequerypage"></a>

### `GET /search/movie/{query}/{page}`

**Description:** Searches for movies with optional genre filtering.
**Parameters:**

- `query` (string): The search query.
- `page` (integer): The page number for pagination.
- `genres` (string, optional): Comma-separated list of genre IDs.

---

<!-- TOC --><a name="get-searchtvquerypage"></a>

### `GET /search/tv/{query}/{page}`

**Description:** Searches for TV shows with optional genre filtering.
**Parameters:**

- `query` (string): The search query.
- `page` (integer): The page number for pagination.
- `genres` (string, optional): Comma-separated list of genre IDs.

<!-- TOC --><a name="lists"></a>

## Lists

<!-- TOC --><a name="post-watchlistmovieaddintmovie_id"></a>

### `POST /watchlist/movie/add/<int:movie_id>`

**Description:** Adds a movie to the user's watchlist.

**Parameters:**

- `movie_id` (integer): The ID of the movie to be added to the watchlist.

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:** None

**Response:**

- **200 OK:**
  ```json
  {
    "message": "Movie added to watchlist"
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Token is required"
  }
  ```
  ```json
  {
    "error": "Movie already in watchlist"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "User not found"
  }
  ```

---

<!-- TOC --><a name="post-finishedmovieaddintmovie_id"></a>

### `POST /finished/movie/add/<int:movie_id>`

**Description:** Adds a movie to the user's finished list.

**Parameters:**

- `movie_id` (integer): The ID of the movie to be added to the finished list.

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:** None

**Response:**

- **200 OK:**
  ```json
  {
    "message": "Movie added to finished"
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Token is required"
  }
  ```
  ```json
  {
    "error": "Movie already in finished"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "User not found"
  }
  ```

---

<!-- TOC --><a name="post-watchlistmovieremoveintmovie_id"></a>

### `POST /watchlist/movie/remove/<int:movie_id>`

**Description:** Removes a movie from the user's watchlist.

**Parameters:**

- `movie_id` (integer): The ID of the movie to be removed from the watchlist.

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:** None

**Response:**

- **200 OK:**
  ```json
  {
    "message": "Movie removed from watchlist"
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Token is required"
  }
  ```
  ```json
  {
    "error": "Movie ID is required"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "User not found"
  }
  ```

---

<!-- TOC --><a name="post-finishedmovieremoveintmovie_id"></a>

### `POST /finished/movie/remove/<int:movie_id>`

**Description:** Removes a movie from the user's finished list.

**Parameters:**

- `movie_id` (integer): The ID of the movie to be removed from the finished list.

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:** None

**Response:**

- **200 OK:**
  ```json
  {
    "message": "Movie removed from finished"
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Token is required"
  }
  ```
  ```json
  {
    "error": "Movie not in finished"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "User not found"
  }
  ```

---

<!-- TOC --><a name="get-watchlistmovie"></a>

### `GET /watchlist/movie`

**Description:** Retrieves the user's movie watchlist.

**Parameters:** None

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:** None

**Response:**

- **200 OK:**
  ```json
  [
    movie_id_1,
    movie_id_2,
    ...
  ]
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Token is required"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "User not found"
  }
  ```

---

<!-- TOC --><a name="get-watchlistmovieintmovie_id"></a>

### `GET /watchlist/movie/<int:movie_id>`

**Description:** Checks if a movie is in the user's watchlist.

**Parameters:**

- `movie_id` (integer): The ID of the movie to check.

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:** None

**Response:**

- **200 OK:**
  ```json
  {
    "success": False
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Token is required"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "User not found"
  }
  ```

---

<!-- TOC --><a name="get-finishedmovie"></a>

### `GET /finished/movie`

**Description:** Retrieves the user's finished movies list.

**Parameters:** None

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:** None

**Response:**

- **200 OK:**
  ```json
  [
    {
      "movie_id": movie_id_1,
      "rating": 0,
      "review": ""
    },
    {
      "movie_id": movie_id_2,
      "rating": 0,
      "review": ""
    },
    ...
  ]
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Token is required"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "User not found"
  }
  ```

---

<!-- TOC --><a name="get-finishedmovieintmovie_id"></a>

### `GET /finished/movie/<int:movie_id>`

**Description:** Checks if a movie is in the user's finished list.

**Parameters:**

- `movie_id` (integer): The ID of the movie to check.

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:** None

**Response:**

- **200 OK:**
  ```json
  {
    "success": True,
    "movie": {
      "movie_id": movie_id,
      "rating": 0,
      "review": ""
    }
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Token is required"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "User not found"
  }
  ```

---

<!-- TOC --><a name="post-watchlisttvaddintshow_id"></a>

### `POST /watchlist/tv/add/<int:show_id>`

**Description:** Adds a TV show to the user's watchlist.

**Parameters:**

- `show_id` (integer): The ID of the TV show to be added to the watchlist.

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:** None

**Response:**

- **200 OK:**
  ```json
  {
    "message": "TV show added to watchlist"
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Token is required"
  }
  ```
  ```json
  {
    "error": "TV show already in watchlist"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "User not found"
  }
  ```

---

<!-- TOC --><a name="post-finishedtvaddintshow_id"></a>

### `POST /finished/tv/add/<int:show_id>`

**Description:** Adds a TV show to the user's finished list.

**Parameters:**

- `show_id` (integer): The ID of the TV show to be added to the finished list.

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:** None

**Response:**

- **200 OK:**
  ```json
  {
    "message": "TV show added to finished"
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Token is required"
  }
  ```
  ```json
  {
    "error": "TV show already in finished"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "User not found"
  }
  ```

<!-- TOC --><a name="post-watchlisttvremoveintshow_id"></a>

### `POST /watchlist/tv/remove/<int:show_id>`

**Description:** Removes a TV show from the user's watchlist.

**Parameters:**

- `show_id` (integer): The ID of the TV show to be removed from the watchlist.

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:** None

**Response:**

- **200 OK:**
  ```json
  {
    "message": "TV show removed from watchlist"
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Token is required"
  }
  ```
  ```json
  {
    "error": "TV show not in watchlist"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "User not found"
  }
  ```

---

<!-- TOC --><a name="post-finishedtvremoveintshow_id"></a>

### `POST /finished/tv/remove/<int:show_id>`

**Description:** Removes a TV show from the user's finished list.

**Parameters:**

- `show_id` (integer): The ID of the TV show to be removed from the finished list.

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:** None

**Response:**

- **200 OK:**
  ```json
  {
    "message": "TV show removed from finished"
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Token is required"
  }
  ```
  ```json
  {
    "error": "TV show not in finished"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "User not found"
  }
  ```

---

<!-- TOC --><a name="get-watchlisttv"></a>

### `GET /watchlist/tv`

**Description:** Retrieves the user's TV watchlist.

**Parameters:** None

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:** None

**Response:**

- **200 OK:**
  ```json
  [
    show_id_1,
    show_id_2,
    ...
  ]
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Token is required"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "User not found"
  }
  ```

---

<!-- TOC --><a name="get-finishedtv"></a>

### `GET /finished/tv`

**Description:** Retrieves the user's finished TV shows list.

**Parameters:** None

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:** None

**Response:**

- **200 OK:**
  ```json
  [
    {
      "show_id": show_id_1,
      "rating": 0,
      "review": ""
    },
    {
      "show_id": show_id_2,
      "rating": 0,
      "review": ""
    },
    ...
  ]
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Token is required"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "User not found"
  }
  ```

---

<!-- TOC --><a name="post-favouritepeopleaddintperson_id"></a>

### `POST /favourite/people/add/<int:person_id>`

**Description:** Adds a person to the user's favourite list.

**Parameters:**

- `person_id` (integer): The ID of the person to be added to favourites.

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:** None

**Response:**

- **200 OK:**
  ```json
  {
    "message": "Person favourited"
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Token is required"
  }
  ```
  ```json
  {
    "error": "Person already favourited"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "User not found"
  }
  ```

---

<!-- TOC --><a name="post-favouritepeopleremoveintperson_id"></a>

### `POST /favourite/people/remove/<int:person_id>`

**Description:** Removes a person from the user's favourite list.

**Parameters:**

- `person_id` (integer): The ID of the person to be removed from favourites.

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:** None

**Response:**

- **200 OK:**
  ```json
  {
    "message": "Person removed from favourites"
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Token is required"
  }
  ```
  ```json
  {
    "error": "Person not favourited"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "User not found"
  }
  ```

---

<!-- TOC --><a name="get-favouritepeople"></a>

### `GET /favourite/people`

**Description:** Retrieves the user's favourite people list.

**Parameters:** None

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:** None

**Response:**

- **200 OK:**
  ```json
  [
    person_id_1,
    person_id_2,
    ...
  ]
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Token is required"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "User not found"
  }
  ```

---

<!-- TOC --><a name="get-favouritepeopleintperson_id"></a>

### `GET /favourite/people/<int:person_id>`

**Description:** Checks if a person is in the user's favourite list.

**Parameters:**

- `person_id` (integer): The ID of the person to check.

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:** None

**Response:**

- **200 OK:**
  ```json
  {
    "success": True
  }
  ```
  ```json
  {
    "success": False
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Token is required"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "User not found"
  }
  ```

---

<!-- TOC --><a name="post-finishedmovieintmovie_idratefloatsignedfalsescore"></a>

### `POST /finished/movie/<int:movie_id>/rate/<float(signed=False):score>`

**Description:** Changes the rating of a finished movie.

**Parameters:**

- `movie_id` (integer): The ID of the movie to be rated.
- `score` (float): The rating score (must be between 0 and 10).

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:** None

**Response:**

- **200 OK:**
  ```json
  {
    "message": "Rating updated to <score> for movie <movie_id>"
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Token is required"
  }
  ```
  ```json
  {
    "error": "Rating score must be between 0 and 10"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "User not found"
  }
  ```
  ```json
  {
    "error": "Movie not found in finished list"
  }
  ```

---

<!-- TOC --><a name="post-finishedshowintshow_idratefloatsignedfalsescore"></a>

### `POST /finished/show/<int:show_id>/rate/<float(signed=False):score>`

**Description:** Changes the rating of a finished TV show.

**Parameters:**

- `show_id` (integer): The ID of the show to be rated.
- `score` (float): The rating score (must be between 0 and 10).

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:** None

**Response:**

- **200 OK:**
  ```json
  {
    "message": "Rating updated to <score> for show <show_id>"
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Token is required"
  }
  ```
  ```json
  {
    "error": "Rating score must be between 0 and 10"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "User not found"
  }
  ```
  ```json
  {
    "error": "Show not found in finished list"
  }
  ```

---

<!-- TOC --><a name="post-finishedmovieintmovie_idreview"></a>

### `POST /finished/movie/<int:movie_id>/review`

**Description:** Changes the review of a finished movie.

**Parameters:**

- `movie_id` (integer): The ID of the movie to be reviewed.

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:**

```json
{
  "review": "This is my review of the movie."
}
```

**Response:**

- **200 OK:**
  ```json
  {
    "message": "Review updated for movie <movie_id>"
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Token is required"
  }
  ```
  ```json
  {
    "error": "Review is required"
  }
  ```
  <!-- TOC --><a name="friends"></a>

## Friends

<!-- TOC --><a name="post-friendsrequest"></a>

### `POST /friends/request`

**Description:** Sends a friend request to the specified email address.

**Parameters:**

- `email` (string): The email of the recipient.

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:**

```json
{
  "email": "recipient@example.com"
}
```

**Response:**

- **200 OK:**
  ```json
  {
    "message": "Friend request sent"
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Recipient email is required"
  }
  ```
  ```json
  {
    "error": "Token is required"
  }
  ```
  ```json
  {
    "error": "You cannot send a friend request to yourself :("
  }
  ```
  ```json
  {
    "error": "Friend request already sent <status>"
  }
  ```
  ```json
  {
    "error": "Friendship already exists"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "Recipient not found"
  }
  ```

---

<!-- TOC --><a name="get-friendsget_pending_requests"></a>

### `GET /friends/get_pending_requests`

**Description:** Retrieves all pending friend requests for the authenticated user.

**Parameters:** None

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:** None

**Response:**

- **200 OK:**
  ```json
  [
    {
      "sender": "sender@example.com",
      "recipient": "recipient@example.com",
      "status": "pending",
      "created_at": "datetime"
    },
    ...
  ]
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Token is required"
  }
  ```

---

<!-- TOC --><a name="post-friendsrespond"></a>

### `POST /friends/respond`

**Description:** Responds to a friend request.

**Parameters:**

- `email` (string): The email of the sender.
- `response` (string): The response to the friend request, either "accept" or "reject".

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:**

```json
{
  "email": "sender@example.com",
  "response": "accept"
}
```

**Response:**

- **200 OK:**
  ```json
  {
    "message": "Friend request accepted"
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Sender email is required"
  }
  ```
  ```json
  {
    "error": "Invalid response"
  }
  ```
  ```json
  {
    "error": "Token is required"
  }
  ```
  ```json
  {
    "error": "Already responded to request"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "Friend request not found"
  }
  ```

---

<!-- TOC --><a name="get-friendsget_friends"></a>

### `GET /friends/get_friends`

**Description:** Retrieves the list of friends for the authenticated user.

**Parameters:** None

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:** None

**Response:**

- **200 OK:**
  ```json
  [
    {
      "sender": "user@example.com",
      "recipient": "friend@example.com",
      "since": "datetime"
    },
    ...
  ]
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Token is required"
  }
  ```

---

<!-- TOC --><a name="post-friendsremove"></a>

### `POST /friends/remove`

**Description:** Removes a friend from the user's friend list.

**Parameters:**

- `email` (string): The email of the friend to be removed.

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:**

```json
{
  "email": "friend@example.com"
}
```

**Response:**

- **200 OK:**
  ```json
  {
    "message": "Friend removed"
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Friend email is required"
  }
  ```
  ```json
  {
    "error": "Token is required"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "Friendship not found"
  }
  ```

---

<!-- TOC --><a name="post-friendsis_friend"></a>

### `POST /friends/is_friend`

**Description:** Checks if a user is friends with another user.

**Parameters:**

- `email` (string): The email of the friend to check.

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:**

```json
{
  "email": "friend@example.com"
}
```

**Response:**

- **200 OK:**
  ```json
  {
    "message": "Friendship exists"
  }
  ```
  ```json
  {
    "message": "Friendship does not exist"
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Friend email is required"
  }
  ```
  ```json
  {
    "error": "Token is required"
  }
  ```

---

<!-- TOC --><a name="post-friendsget_friend_profile"></a>

### `POST /friends/get_friend_profile`

**Description:** Retrieves the profile of a friend.

**Parameters:**

- `email` (string): The email of the friend whose profile is being retrieved.

**Headers:**

- `Authorization` (string): Bearer token for user authentication.

**Body:**

```json
{
  "email": "friend@example.com"
}
```

**Response:**

- **200 OK:**
  ```json
  {
    "username": "friendusername",
    "other_field": "value",
    ...
  }
  ```

**Possible Errors:**

- **400 Bad Request:**
  ```json
  {
    "error": "Token is required"
  }
  ```
- **404 Not Found:**
  ```json
  {
    "error": "Friend not found"
  }
  ```
  ```json
  {
    "error": "Friendship does not exist"
  }
  ```
