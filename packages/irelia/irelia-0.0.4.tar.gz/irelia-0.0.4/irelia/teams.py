import requests
from irelia import params, headers


def get_teams(team_id):
    params['id'] = team_id
    return requests.get('https://esports-api.lolesports.com/persisted/gw/getTeams', params = params, headers = headers).json()['data']['teams']

def getAllTeams():
    return requests.get('https://esports-api.lolesports.com/persisted/gw/getTeams', params = params, headers = headers).json()['data']['teams']

