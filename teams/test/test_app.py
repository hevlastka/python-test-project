import json
import unittest
import requests
from teams import app
import tempfile

URL='http://0.0.0.0:5000'

class TestApi(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def test_successful_request(self):
        with self.app as client:
            result = client.get('/allTeams')
            assert result.status_code == 200

    def test_unsuccessful_request(self):
        with self.app as client:
            result = client.get('/allTeams324')
            assert result.status_code == 404

    def test_view_all_teams(self):
        r = requests.get(URL+'/allTeams')
        data = r.json()
        assert r.status_code == 200
        fields = list(data)
        assert fields[0]['team_name'] == "Engineering"
        assert fields[1]['team_name'] == "Customer Support"

    def test_view_teams_comp_id_1(self):
        r = requests.get(URL+'/wiewTeamsWithComp/1')
        data = r.json()
        assert r.status_code == 200
        fields = list(data)
        assert fields[0]['company_name'] == "Acme"
        assert fields[0]['id'] == 1

    def test_select_team_id_1(self):
        r = requests.get(URL+'/selectTeam/1')
        data = r.json()
        assert r.status_code == 200
        fields = list(data)
        assert fields[0]['team_name'] == "Engineering"
        assert fields[0]['id'] == 1
        assert fields[0]['members'][0]["email"] == "mike@mike.com"
        assert fields[0]['members'][0]["company"][0]["id"] == 1