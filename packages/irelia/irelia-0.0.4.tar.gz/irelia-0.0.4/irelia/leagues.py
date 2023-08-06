import requests
from irelia import params, headers


def get_leagues():
    return requests.get('https://esports-api.lolesports.com/persisted/gw/getLeagues', params=params, headers=headers).json()


def get_tournament_from_league(league_id):
    params['leagueId'] = league_id
    return requests.get('https://esports-api.lolesports.com/persisted/gw/getTournamentsForLeague', params=params, headers=headers).json()


def get_standings(tournament_id):
    params['tournamentId'] = tournament_id
    return requests.get('https://esports-api.lolesports.com/persisted/gw/getStandings', params=params, headers=headers).json()

