import sys

from flask import request, jsonify, abort

from app import app, db, twitter_api, NUMBER_OF_POSTS
import models


def paginate(query):
    # TODO implement actual pagination with parameters
    items = []
    for item in query.paginate().items:
        items.append(dict(item))
    return jsonify(items)


@app.route('/users/', methods=['GET'])
def all_users():
    try:
        return paginate(models.User.query)
    except Exception as e:
        print >> sys.stderr, e
        abort(404)


@app.route('/users/<twitter_id>/', methods=['GET'])
def user_data(twitter_id):
    try:
        user = models.User.query.get(twitter_id)
        if not request.args.get('local') or request.args.get('local') != 'true':
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
    try:
        user = models.User.query.get(twitter_id)
        if not user:
            user = models.User(twitter_api.GetUser(user_id=twitter_id).AsDict())
            db.session.add(user)
        if not request.args.get('local') or request.args.get('local') != 'true':
            statuses = twitter_api.GetUserTimeline(user_id=twitter_id, count=NUMBER_OF_POSTS)
            for status in statuses:
                new_status_dict = status.AsDict()
                new_status_dict['user_id'] = status.user.id
                old_status = models.Status.query.get(status.id)
                if old_status:
                    old_status.update(new_status_dict)
                else:
                    new_status = models.Status(new_status_dict)
                    db.session.add(new_status)
                # TODO delete extra statuses
        db.session.commit()
        return paginate(models.Status.query.with_parent(user))
    except Exception as e:
        print >> sys.stderr, e
        abort(404)
