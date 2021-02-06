from flask import Flask

from model.model import Team, db
from . import create_app

app = create_app()

@app.route('/')

@app.route('/test_db')
def test_db():
    user = Team.query.first()
    return "Team: '{} ' and members: '{}' from database".format(user.name, user.members)