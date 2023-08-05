import requests
from irelia import params, headers


def getLeagues():
    return requests.get('https://esports-api.lolesports.com/persisted/gw/getLeagues', params=params, headers=headers).json()


def getTournamentFromLeague(leagueId):
    params['leagueId'] = leagueId
    return requests.get('https://esports-api.lolesports.com/persisted/gw/getTournamentsForLeague', params=params, headers=headers).json()


def getStandings(tournamentId):
    params['tournamentId'] = tournamentId
    return requests.get('https://esports-api.lolesports.com/persisted/gw/getStandings', params=params, headers=headers).json()

