import requests
from irelia import params, headers, s11_start_date
import datetime


def getSchedule(leagueId, pageToken=None):
    params['leagueId'] = leagueId
    if pageToken is not None:
        params['pageToken'] = pageToken
    return requests.get('https://esports-api.lolesports.com/persisted/gw/getSchedule', params=params, headers=headers).json()


def getFullSchedule(leagueId, current=True):
    data = getSchedule(leagueId)
    if "errors" in data:
        print("getFullScheduleError")
        return leagueId
    else:
        pageTokens = []
        full_schedule = []
        while data['data']['schedule']['pages']['older'] is not None:
            full_schedule += data['data']['schedule']['events']
            pageToken = data['data']['schedule']['pages']['older']
            pageTokens.append(pageToken)
            data = getSchedule(leagueId, pageToken)

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


def getEventDetails(matchId):
    params['id'] = matchId
    return requests.get("https://esports-api.lolesports.com/persisted/gw/getEventDetails", params=params, headers=headers).json()


def getCompletedEvents(tournamentId):
    params['tournamentId'] = tournamentId
    return requests.get("https://esports-api.lolesports.com/persisted/gw/getCompletedEvents", params=params, headers=headers).json()


# def getGames():
    #TODO: pull the games

# def getLive():
    #TODO: pull live games