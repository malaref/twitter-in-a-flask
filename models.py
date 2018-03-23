"""
The models module of the application.
Contains the declaration of the models
used in the application using the
declarative SQLAlchemy ORM.
"""

from app import db


class DynamicModelMixin(object):
    """A made-up helpful mixin to add common functionality to other modules."""

    def __init__(self, user_dict):
        self.update(user_dict)

    def __iter__(self):
        for column in self.__table__.columns:
            yield column.name, getattr(self, column.name)

    def update(self, data_dict):
        for key in data_dict:
            if hasattr(self, key):
                setattr(self, key, data_dict[key])


class User(DynamicModelMixin, db.Model):
    """A class capturing a subset of Tweeter's 'User' object."""
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime)
    url = db.Column(db.String())
    screen_name = db.Column(db.String())
    name = db.Column(db.String())
    description = db.Column(db.String())
    location = db.Column(db.String())
    followers_count = db.Column(db.Integer)
    friends_count = db.Column(db.Integer)
    listed_count = db.Column(db.Integer)
    statuses_count = db.Column(db.Integer)
    statuses = db.relationship('Status')


class Status(DynamicModelMixin, db.Model):
    """A class capturing a subset of Tweeter's 'Tweet' object."""
    id = db.Column(db.BigInteger, primary_key=True)
    created_at = db.Column(db.DateTime)
    text = db.Column(db.String())
    favorite_count = db.Column(db.Integer)
    retweet_count = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
