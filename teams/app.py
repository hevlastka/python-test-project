import json

from flask import request, render_template

from model.model import Company, Team, User
from . import create_app
from db import database

app = create_app()


@app.route('/', methods=['GET'])
def fetch_teams(select_team_id=None, select_company_id=1):
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
    # I do return json but I've got the posibility to create a template HTML
    if sel_team_id is not None:
        new_team = json.dumps([
            __select_specific_team(sel_team_id, team, users, companies)
            for team in teams
        ])
    else:
        new_team = json.dumps([
            __get_all_teams(team, users, companies)
            for team in teams
        ])
    # return render_template("teachers.html", teachers=all_teams), 200
    return json.dumps(new_team), 200

def __get_all_teams(team, users, companies):
    companies = json.dumps([
        __get_companies(company)
        for company in companies
    ])
    users = json.dumps([
        __get_users(user, companies)
        for user in users
    ])
    return {
        "id": team.TeamId,
        "team_name": team.teamName,
        "members": users
    }

def __select_specific_team(select_id, team, users, companies):
    companies = json.dumps([
        __get_specific_companies(select_id, company)
        for company in companies
    ])
    selected_user = json.dumps([
        __select_specific_user(select_id, user)
        for user in users
    ])
    if team.TeamId==select_id:
        return {
            "id": team.TeamId,
            "team_name": team.teamName,
            "members": selected_user
        }

def __select_specific_user(select_id, user):
    if user.UserId==select_id:
        return {
            "id": user.UserId,
            "user_name": user.userName,
            "email": user.email
        }

def __get_specific_companies(select_id, company):
    if company.CompanyId==select_id:
        return {
            "id": company.CompanyId,
            "company_name": company.companyName
        }  

def __get_users(user, companies):
        return {
            "id": user.UserId,
            "user_name": user.userName,
            "email": user.email,
            "company": companies
        }

def __get_companies(company):
    return {
        "id": company.CompanyId,
        "company_name": company.companyName
    }

def __select_teams_with_companies(select_id, teams, companies, users):
    all_companies = []
    teams = json.dumps([
        __select_specific_team(select_id, team, users, companies) 
        for team in teams
        ])
    for company in companies:
        if select_id == company.CompanyId:
            new_company = {
                "id": company.CompanyId,
                "company_name": company.companyName,
                "teams": teams
            }
            all_companies.append(new_company)
    return json.dumps(all_companies), 200


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
