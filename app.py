import os

import twitter
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ['SECRET_KEY'],
    SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL'],
    SQLALCHEMY_TRACK_MODIFICATIONS=False)
db = SQLAlchemy(app)
NUMBER_OF_POSTS = 25

twitter_api = twitter.Api(
    consumer_key=os.environ['CONSUMER_KEY'],
    consumer_secret=os.environ['CONSUMER_SECRET'],
    access_token_key=os.environ['ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['ACCESS_TOKEN_SECRET'])

import routes
