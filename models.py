from app import db


class User(db.Model):
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

    def update(self, user_dict):
        for key in user_dict:
            if hasattr(User, key):
                setattr(self, key, user_dict[key])

    def __init__(self, user_dict):
        self.update(user_dict)

    def __iter__(self):
        for column in self.__table__.columns:
            yield column.name, getattr(self, column.name)
