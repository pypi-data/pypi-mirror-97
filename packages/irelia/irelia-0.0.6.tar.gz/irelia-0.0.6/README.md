# Irelia
A python wrapper for the Lolesports api that can be found here: https://vickz84259.github.io/lolesports-api-docs/.
With the exception of some functions that aren't in the original api, all of these functions have their functionality explained in the link above.

Current Functionality:
- Leagues
  - getLeagues()
  - getTournamentFromLeague(leagueId)
  - getStandings(tournamentId)
- Events
  - getSchedule(leagueId, pageToken=None)
  - getFullSchedule(leagueId, current=True)
  - getEventDetails(matchId)
  - getCompletedEvents(tournamentId)
- Teams
  - getTeams(teamId)
  - getAllTeams()
- Match Details
  - getWindow()

To Do: 
- Leagues:
- Events: 
  - getGames()
  - getLive()
- Teams:
- Match Details:
  - getFullGameWindow()
  - getDetails()