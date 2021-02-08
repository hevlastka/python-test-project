import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()

class Team(db.Model):
    __tablename__ = 'Teams'
    TeamId = db.Column(db.Integer(), primary_key=True)
    teamName = db.Column(db.String())
    members = db.Column(db.String())

class User(db.Model):
    __tablename__ = 'Users'
    UserId = db.Column(db.Integer(), primary_key=True)
    userName = db.Column(db.String())
    email = db.Column(db.String())
    company = db.Column(db.String())
    CompanyId = db.Column(db.Integer())
    TeamId = db.Column(db.Integer())

class Company(db.Model):
    __tablename__ = 'Company'
    CompanyId = db.Column(db.Integer(), primary_key=True)
    companyName = db.Column(db.String())
