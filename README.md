# twitter-in-a-flask
A Twitter tweets querier in Python using Flask.

## Endpoints

**>> as documented in [routes.py](https://github.com/muhammad-alaref/twitter-in-a-flask/blob/master/routes.py).**

```http
GET /users/
```
returns a list of saved users in the database.

```http
GET /users/<twitter_id>/
```
scraps user data and saves them to the database, updates it if needed. If query param `?local=true` was provided, it just returns saved data from the database.

```http
GET /users/<twitter_id>/posts/
```
fetches the last 25 tweets of the user and puts them into the database. If called a second time, it compares tweets in the database with the ones from Twitter, updates with more recent tweets if needed. If query param `?local=true` was provided, it just returns saved data from the database.

## Demo

A deployed version of the application is available on [Heroku](https://twitter-in-a-flask.herokuapp.com/).
