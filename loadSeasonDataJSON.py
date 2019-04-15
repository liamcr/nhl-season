# Creates a JSON file with the necessary information to simulate a season based
# on real regular season data from a given time frame.

from requests import get
from json import dump

filename = input("File name: ")
startDate = input("Start date (YYYY-MM-DD): ")
endDate = input("End date (YYY-MM-DD): ")
teamData = get("https://statsapi.web.nhl.com/api/v1/teams").json()
scheduleData = get("https://statsapi.web.nhl.com/api/v1/schedule?startDate=" + startDate + "&endDate=" + endDate).json()

data = {}

data["totalAwayGoals"] = 0
data["totalHomeGoals"] = 0
data["totalGames"] = 0

for team in teamData["teams"]:
    data[str(team["id"])] = {}
    data[str(team["id"])]["abbreviation"] = team["abbreviation"]
    data[str(team["id"])]["totalAwayGoals"] = 0
    data[str(team["id"])]["totalHomeGoals"] = 0
    data[str(team["id"])]["totalAwayGoalsAgainst"] = 0
    data[str(team["id"])]["totalHomeGoalsAgainst"] = 0
    data[str(team["id"])]["totalHomeGames"] = 0
    data[str(team["id"])]["totalAwayGames"] = 0

for date in scheduleData["dates"]:
    for game in date["games"]:
        if (game["gameType"] == "R"):
            data["totalGames"] += 1

            data["totalHomeGoals"] += game["teams"]["home"]["score"]
            data["totalAwayGoals"] += game["teams"]["away"]["score"]

            data[str(game["teams"]["home"]["team"]["id"])]["totalHomeGames"] += 1
            data[str(game["teams"]["home"]["team"]["id"])]["totalHomeGoals"] += game["teams"]["home"]["score"]
            data[str(game["teams"]["home"]["team"]["id"])]["totalHomeGoalsAgainst"] += game["teams"]["away"]["score"]

            data[str(game["teams"]["away"]["team"]["id"])]["totalAwayGames"] += 1
            data[str(game["teams"]["away"]["team"]["id"])]["totalAwayGoals"] += game["teams"]["away"]["score"]
            data[str(game["teams"]["away"]["team"]["id"])]["totalAwayGoalsAgainst"] += game["teams"]["home"]["score"]

data["avgAwayGoals"] = data["totalAwayGoals"] / data["totalGames"]
data["avgHomeGoals"] = data["totalHomeGoals"] / data["totalGames"]

for team in teamData["teams"]:
    if data[str(team["id"])]["totalHomeGames"] >= 1:
        data[str(team["id"])]["avgHomeGoals"] = data[str(team["id"])]["totalHomeGoals"] / data[str(team["id"])]["totalHomeGames"]
    else:
        data[str(team["id"])]["avgHomeGoals"] = data["avgHomeGoals"]
    
    if data[str(team["id"])]["totalAwayGames"] >= 1:
        data[str(team["id"])]["avgAwayGoals"] = data[str(team["id"])]["totalAwayGoals"] / data[str(team["id"])]["totalAwayGames"]
    else:
        data[str(team["id"])]["avgAwayGoals"] = data["avgAwayGoals"]

    if data[str(team["id"])]["totalHomeGames"] >= 1:
        data[str(team["id"])]["avgHomeGoalsAgainst"] = data[str(team["id"])]["totalHomeGoalsAgainst"] / data[str(team["id"])]["totalHomeGames"]
    else:
        data[str(team["id"])]["avgHomeGoalsAgainst"] = data["avgAwayGoals"]
    
    if data[str(team["id"])]["totalAwayGames"] >= 1:
        data[str(team["id"])]["avgAwayGoalsAgainst"] = data[str(team["id"])]["totalAwayGoalsAgainst"] / data[str(team["id"])]["totalAwayGames"]
    else:
        data[str(team["id"])]["avgAwayGoalsAgainst"] = data["avgHomeGoals"]

    data[str(team["id"])]["homeOffensiveStrength"] = data[str(team["id"])]["avgHomeGoals"] / data["avgHomeGoals"]
    data[str(team["id"])]["awayOffensiveStrength"] = data[str(team["id"])]["avgAwayGoals"] / data["avgAwayGoals"]
    data[str(team["id"])]["homeDefensiveStrength"] = data[str(team["id"])]["avgHomeGoalsAgainst"] / data["avgAwayGoals"]
    data[str(team["id"])]["awayDefensiveStrength"] = data[str(team["id"])]["avgAwayGoalsAgainst"] / data["avgHomeGoals"]

fp = open(filename, "w")

dump(data, fp)

fp.close()