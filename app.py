import os

import sys
import twitter
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ['SECRET_KEY'],
    SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL'],
    SQLALCHEMY_TRACK_MODIFICATIONS=False)
db = SQLAlchemy(app)


import models


twitter_api = twitter.Api(
    consumer_key=os.environ['CONSUMER_KEY'],
    consumer_secret=os.environ['CONSUMER_SECRET'],
    access_token_key=os.environ['ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['ACCESS_TOKEN_SECRET'])


@app.route('/users/<twitter_id>/', methods=['GET'])
def user_data(twitter_id):
    try:
        user = models.User.query.get(twitter_id)
        if not request.args.get('local'):
            updated_user_dict = twitter_api.GetUser(user_id=twitter_id).AsDict()
            if user:
                user.update(updated_user_dict)
            else:
                user = models.User(updated_user_dict)
                db.session.add(user)
            db.session.commit()
        return jsonify(dict(user))
    except Exception as e:
        print >> sys.stderr, e
        abort(404)


@app.route('/users/<twitter_id>/posts/', methods=['GET'])
def user_posts(twitter_id):
    return "Posts of {}!".format(twitter_id)


if __name__ == '__main__':
    app.run()
