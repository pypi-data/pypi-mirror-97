import requests
from irelia import params, headers, s11_start_date
import datetime


def get_schedule(league_id, pageToken=None):
    params['leagueId'] = league_id
    if pageToken is not None:
        params['pageToken'] = pageToken
    return requests.get('https://esports-api.lolesports.com/persisted/gw/getSchedule', params=params, headers=headers).json()


def get_full_schedule(league_id, current=True):
    data = get_schedule(league_id)
    if "errors" in data:
        print("getFullScheduleError")
        return league_id
    else:
        pageTokens = []
        full_schedule = []
        while data['data']['schedule']['pages']['older'] is not None:
            full_schedule += data['data']['schedule']['events']
            pageToken = data['data']['schedule']['pages']['older']
            pageTokens.append(pageToken)
            data = get_schedule(league_id, pageToken)

        full_schedule += data['data']['schedule']['events']
        pageToken = data['data']['schedule']['pages']['older']
        pageTokens.append(pageToken)
        # sort the full_schedule here with a list comprehension
        ordered_schedule = sorted(full_schedule, key=lambda k: datetime.datetime.strptime(k['startTime'], "%Y-%m-%dT%H:%M:%SZ"))
        if current is False:
            return ordered_schedule
        else:
            current_schedule = []
            for match in ordered_schedule:
                if match['startTime'] >= s11_start_date:
                    current_schedule.append(match)
            return current_schedule


def get_event_details(match_id):
    params['id'] = match_id
    return requests.get("https://esports-api.lolesports.com/persisted/gw/getEventDetails", params=params, headers=headers).json()


def get_completed_events(tournament_id):
    params['tournamentId'] = tournament_id
    return requests.get("https://esports-api.lolesports.com/persisted/gw/getCompletedEvents", params=params, headers=headers).json()


# def getGames():
    #TODO: pull the games

# def getLive():
    #TODO: pull live games