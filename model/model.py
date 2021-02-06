import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()

class Team(db.Model):
    __tablename__ = 'Teams'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    members = db.Column(db.String())