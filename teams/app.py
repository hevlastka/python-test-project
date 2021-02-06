import json

from flask import Flask
import sqlite3

from model.model import Team, db
from . import create_app
from db import database

app = create_app()

@app.route('/', methods=['GET'])
def fetch():
    teams = database.get_all(Team)
    try:
        if teams is None:
            raise Exception()
    except ValueError as err:
            print(err, "there was a problem with the conection of the db.")
    return __get_users(teams)
    
def __get_users(teams):
    all_teams = []
    for team in teams:
        new_team = {
            "id": team.id,
            "name": team.name,
            "members": team.members,
        }
        all_teams.append(new_team)
    return json.dumps(all_teams), 200