import json

from flask import request, render_template

from model.model import Company, Team, User
from . import create_app
from db import database

app = create_app()


@app.route('/', methods=['GET'])
# Change Ids of 'select_team_id' or 'select_company_id' 
# to cover the last two points of the project
def fetch_teams(select_team_id=None, select_company_id=None):
    teams = database.get_all(Team)
    users = database.get_all(User)
    companies = database.get_all(Company)
    try:
        if teams is None or users is None or companies is None:
            raise Exception()
    except ValueError as err:
        print(err, "there was a problem with the conection of the db.")
        return 404
    if select_company_id is not None:
        return __select_teams_with_companies(select_company_id, teams, companies, users)
    return __get_teams(teams, select_team_id, users, companies)

def __get_teams(teams, sel_team_id, users, companies):
    if sel_team_id is not None:
        new_team = __select_values(teams, sel_team_id, users, companies)
    else:
        new_team = __get_all(teams, users, companies)
    # I do return json but I've got the posibility to create a template HTML
    # return render_template("teachers.html", teachers=all_teams), 200
    return json.dumps(new_team), 200

def __select_values(teams, sel_team_id, users, companies):
    sel_companies = [
        __select_specific_company(sel_team_id, company)
        for company in companies
    ]
    sel_companies = delete_nulls(sel_companies)
    sel_user = [
        __select_specific_user(sel_team_id, user, sel_companies)
        for user in users
    ]
    sel_user = delete_nulls(sel_user)
    new_team = [
        __select_specific_team(sel_team_id, team, sel_user)
        for team in teams
    ]
    new_team = delete_nulls(new_team)
    return new_team

def __select_specific_team(select_id, team, selected_user):
    if team.TeamId == select_id:
        return {
            "id": team.TeamId,
            "team_name": team.teamName,
            "members": selected_user
        }

def __select_specific_user(select_id, user, sel_companies):
    if user.TeamId == select_id:
        return {
            "id": user.UserId,
            "user_name": user.userName,
            "email": user.email,
            "company": sel_companies
        }

def __select_specific_company(select_id, company):
    if company.CompanyId == select_id:
        return {
            "id": company.CompanyId,
            "company_name": company.companyName
        }

def __get_all(teams, users, companies):
    all_teams = []
    for team in teams:
        sel_companies = [
            __select_specific_company(team.TeamId, company)
            for company in companies
        ]
        sel_companies = delete_nulls(sel_companies)
        sel_user = [
            __select_specific_user(team.TeamId, user, sel_companies)
            for user in users
        ]
        sel_user = delete_nulls(sel_user)
        new_team = {
            "id": team.TeamId,
            "team_name": team.teamName,
            "members": sel_user
        }

        all_teams.append(new_team)
    return all_teams

def __select_teams_with_companies(select_id, teams, companies, users):
    teams = __select_values(teams, select_id, users, companies)
    sel_companies = [
        __select_specific_company(select_id, company)
        for company in companies
        if company is not None
    ]
    sel_companies.append(teams)
    sel_companies = [company for company in sel_companies if company is not None]
    return json.dumps(sel_companies), 200

def delete_nulls(inputs):
    return [item for item in inputs if item is not None]

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
    database.add_instance(User, userName=user_name,
                          email=email, company=company)
    return str({"userName": user_name, "email": email, "company": company})

def __create_company(data):
    company_name = data["company name"]
    database.add_instance(Company, companyName=company_name)
    return str({"companyName": company_name})
