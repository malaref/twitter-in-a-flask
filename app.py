from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ['SECRET_KEY'],
    SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL'],
    SQLALCHEMY_TRACK_MODIFICATIONS=False)
db = SQLAlchemy(app)


@app.route('/users/<twitterId>/', methods=['GET'])
def user(twitter_id):
    return "Hello {}!".format(twitter_id)


@app.route('/users/<twitterId>/posts/', methods=['GET'])
def posts(twitter_id):
    return "Posts of {}!".format(twitter_id)


if __name__ == '__main__':
    app.run()
