import requests
from irelia import params, headers


def getTeams(teamId):
    params['id'] = teamId
    return requests.get('https://esports-api.lolesports.com/persisted/gw/getTeams', params = params, headers = headers).json()['data']['teams']

def getAllTeams():
    return requests.get('https://esports-api.lolesports.com/persisted/gw/getTeams', params = params, headers = headers).json()['data']['teams']

