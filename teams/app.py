import json

from flask import request

from model.model import Company, Team, User
from teams import fetch_data
from . import create_app
from db import database

app = create_app()
teams = database.get_all(Team)
users = database.get_all(User)
companies = database.get_all(Company)

@app.route('/allTeams', methods=['GET'])
def fetch_teams():
    try:
        if teams is None or users is None or companies is None:
            raise Exception()
    except ValueError as err:
        print(err, "there was a problem with the conection of the db.")
        return 404
    return __get_teams(teams, users, companies)

def __get_teams(teams, users, companies):
    new_team = fetch_data.get_all(teams, users, companies)
    return json.dumps(new_team), 200

@app.route('/selectTeam/<team_id>', methods=['GET'])
def select_values(team_id):
    sel_companies = [
        fetch_data.select_specific_company(team_id, company)
        for company in companies
    ]
    sel_companies = fetch_data.delete_nulls(sel_companies)
    sel_user = [
        fetch_data.select_specific_user(team_id, user, sel_companies)
        for user in users
    ]
    sel_user = fetch_data.delete_nulls(sel_user)
    new_team = [
        fetch_data.select_specific_team(team_id, team, sel_user)
        for team in teams
    ]
    new_team = fetch_data.delete_nulls(new_team)
    return json.dumps(new_team), 200

@app.route('/wiewTeamsWithComp/<company_id>', methods=['GET'])
def select_teams_with_companies(company_id):
    teams = select_values(company_id)
    sel_companies = [
        fetch_data.select_specific_company(company_id, company)
        for company in companies
        if company is not None
    ]
    sel_companies.append(teams)
    sel_companies = [
        company for company in sel_companies if company is not None]
    return json.dumps(sel_companies), 200

@app.route('/create', methods=['GET', 'POST'])
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
