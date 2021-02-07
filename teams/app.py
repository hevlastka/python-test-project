import json

from flask import request


from model.model import Company, Team, User
from . import create_app
from db import database

app = create_app()


@app.route('/', methods=['GET'])
def fetch_teams():
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
            "team_name": team.teamName,
            "members": users
        }
        all_teams.append(new_team)
    return json.dumps(all_teams), 200


def __get_users(users, companies=None):
    all_users = []
    for user in users:
        new_user = {
            "id": user.UserId,
            "user_name": user.userName,
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
            "company_name": company.companyName
        }
        all_companies.append(new_company)
    return all_companies


@app.route('/create', methods=['POST'])
def create_teams():
    data = request.get_json()
    team_name = data['teamName']

    team_members = __create_user(data)

    database.add_instance(Team, teamName=team_name, members=team_members)
    return json.dumps("Added"), 200

def __create_user(data):
    user_name = data['userName']
    email = data['email']
    company = __create_company(data)
    database.add_instance(User, userName=user_name, email=email, company=company)
    return str({"userName":user_name, "email":email, "company":company})

def __create_company(data):
    company_name = data["company name"] 
    database.add_instance(Company, companyName=company_name)
    return str({"companyName":company_name})
