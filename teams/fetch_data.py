def get_all(teams, users, companies):
    all_teams = []
    for team in teams:
        sel_companies = [
            select_specific_company(team.TeamId, company)
            for company in companies
        ]
        sel_companies = delete_nulls(sel_companies)
        sel_user = [
            select_specific_user(team.TeamId, user, sel_companies)
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

def select_specific_team(select_id, team, selected_user):
    if team.TeamId == int(select_id):
        return {
            "id": team.TeamId,
            "team_name": team.teamName,
            "members": selected_user
        }

def select_specific_user(select_id, user, sel_companies):
    if user.TeamId == int(select_id):
        return {
            "id": user.UserId,
            "user_name": user.userName,
            "email": user.email,
            "company": sel_companies
        }

def select_specific_company(select_id, company):
    if company.CompanyId == int(select_id):
        return {
            "id": company.CompanyId,
            "company_name": company.companyName
        }

def delete_nulls(inputs):
    return [item for item in inputs if item is not None]
