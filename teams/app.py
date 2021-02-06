import json

from flask import Flask

from model.model import Company, Team, User
from . import create_app
from db import database

app = create_app()


@app.route('/', methods=['GET'])
def fetch():
    teams = database.get_all(Team)
    users = database.get_all(User)
    companies = database.get_all(Company)
    try:
        if teams is None or users is None or companies is None:
            raise Exception()
    except ValueError as err:
        print(err, "there was a problem with the conection of the db.")
    companies_result = __get_companies(companies)
    users_result = __get_users(users, companies_result)
    return __get_teams(teams, users_result)


def __get_teams(teams, users=None):
    all_teams = []
    for team in teams:
        new_team = {
            "id": team.TeamId,
            "name": team.name,
            "members": users
        }
        all_teams.append(new_team)
    return json.dumps(all_teams), 200


def __get_users(users, companies=None):
    all_users = []
    for user in users:
        new_user = {
            "id": user.UserId,
            "name": user.name,
            "email": user.email,
            "company": companies
        }
        all_users.append(new_user)
    return all_users


def __get_companies(companies):
    all_companies = []
    for company in companies:
        new_company = {
            "id": company.CompanyId,
            "name": company.name
        }
        all_companies.append(new_company)
    return all_companies
