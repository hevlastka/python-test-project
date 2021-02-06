import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()

class Team(db.Model):
    __tablename__ = 'Teams'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    members = db.Column(db.String())

class User(db.Model):
    __tablename__ = 'User'
    UserId = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    company = db.Column(db.String())
    TeamId = db.Column(db.Integer())

class Company(db.Model):
    __tablename__ = 'Company'
    CompanyId = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    UserId = db.Column(db.Integer())