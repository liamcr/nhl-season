from requests import get
from json import load
from numpy.random import poisson
from random import randint
import sys

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} seasonDataFile.json")
    sys.exit(1)

# Loads in necessary data from a json file created using loadSeasonDataJSON.py
filename = sys.argv[1]

fp = open(filename, "r")

seasonData = load(fp)

fp.close()

# Team class
# Member variables:
#     id - NHL API's corresponding team id (Integer)
# Methods:
#     predictGoalsFor - Predicts the amount of goals
#         the team will score based on the opponent and whether the
#         team is at home or not
class Team:
    # Team(teamId)
    # Arguments:
    #     teamId: NHL API's corresponding team id
    def __init__(self, teamId):
        self.id = teamId

    # predictGoalsFor(opponentId, home)
    # Arguments:
    #     opponentId - Team ID for the opposing team (Integer)
    #     home - Boolean value, true if the team is the home team
    # Return Value:
    #     An integer representing how many goals were scored by the team
    def predictGoalsFor(self, opponentId, home):
        if (home):
            lamb = seasonData["avgHomeGoals"] * seasonData[str(
                self.id)]["homeOffensiveStrength"] * seasonData[str(opponentId)]["awayDefensiveStrength"]
        else:
            lamb = seasonData["avgAwayGoals"] * seasonData[str(
                self.id)]["awayOffensiveStrength"] * seasonData[str(opponentId)]["homeDefensiveStrength"]

        return poisson(lam=lamb)

# Standings class
# Member Variables:
#     teamData - Dictionary keeping track of each team's W-L-OTL record and points
# Methods:
#     getStandings - Returns a sorted version of the teamData, sorted by points
#     printStandings - Prints the standings in decreasing order
class Standings:
    def __init__(self):
        teamIds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17,
                   18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 29, 30, 52, 53, 54]

        self.teamData = {}

        for teamId in teamIds:
            self.teamData[str(teamId)] = {}
            self.teamData[str(teamId)]["W"] = 0
            self.teamData[str(teamId)]["L"] = 0
            self.teamData[str(teamId)]["OTL"] = 0
            self.teamData[str(teamId)]["P"] = 0

    # getStandings()
    # Return Value:
    #     A list representation of the teamData dictionary sorted in decreasing order
    #     of points
    def getStandings(self):
        return sorted(self.teamData.items(), key=lambda x: x[1]["P"], reverse=True)

    # printStandings()
    # Prints the standins in decreasing order of points
    def printStandings(self):
        standings = sorted(self.teamData.items(),
                           key=lambda x: x[1]["P"], reverse=True)

        for i in range(len(standings)):
            print(
                f"{i + 1}.\t{seasonData[standings[i][0]]['abbreviation']}\t{standings[i][1]['W']}-{standings[i][1]['L']}-{standings[i][1]['OTL']} \t{standings[i][1]['P']} pts")

# Game class
# Member Variables:
#     homeTeam - Team object representing the game's home team
#     awayTeam - Team object representing the game's away team
#     homeScore - Integer representing the home team's goals for
#     awayScore - Integer representing the away team's goals for
#     ot - Boolean value, true if the game finished in overtime
#     losingTeam - Team object representing the eventual losers of the game
#     winningTeam - Team object representing the eventual winners of the game
# Methods:
#     predictFinalScore - Uses each team's predictGoalsFor method to predict the
#         final score of the game
#     printFinalScore - Prints the final score in the following format:
#         [Home team] [Home score] - [Away score] [Away team]
class Game:
    # Game(homeTeam, awayTeam)
    # Arguments:
    #     homeTeam - Team object representing the game's home team
    #     awayTeam - Team object representing the game's away team
    def __init__(self, homeTeam, awayTeam):
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.homeScore = 0
        self.awayScore = 0
        self.ot = False

    # predictFinalScore()
    # Uses each team's predictGoalsFor() method to predict the final score of
    # the game
    def predictFinalScore(self):
        self.ot = False
        self.homeScore = self.homeTeam.predictGoalsFor(self.awayTeam.id, True)
        self.awayScore = self.awayTeam.predictGoalsFor(self.homeTeam.id, False)

        if self.homeScore == self.awayScore:
            if randint(0, 1) == 0:
                self.homeScore += 1
            else:
                self.awayScore += 1
            self.ot = True

        if self.homeScore > self.awayScore:
            self.losingTeam = self.awayTeam
            self.winningTeam = self.homeTeam
        else:
            self.losingTeam = self.homeTeam
            self.winningTeam = self.awayTeam

    # printFinalScore([lineEnd])
    # Arguments:
    #     lineEnd - Optional, sets the character displayed at the end of the line.
    #         By default, it is the newline character
    def printFinalScore(self, lineEnd="\n"):
        print(f"{seasonData[str(self.homeTeam.id)]['abbreviation']} {self.homeScore} - {self.awayScore} {seasonData[str(self.awayTeam.id)]['abbreviation']}", end="")

        print(" (OT)", end=lineEnd) if self.ot else print("     ", end=lineEnd)

# Season class
# Member Variables:
#     scheduleJSON - Dictionary representing the NHL's 2018-19 schedule
#     standings - Standings object representing the standings for the season
# Methods:
#     simSeason - Simulates an entire regular season and updates the standings accordingly
class Season:
    def __init__(self):
        schedule = get(
            "https://statsapi.web.nhl.com/api/v1/schedule?startDate=2018-10-03&endDate=2019-04-06")
        self.scheduleJSON = schedule.json()

        self.standings = Standings()

    # simSeason()
    # Simulates an entire regular season and updates the standings accordingly
    def simSeason(self):
        for date in self.scheduleJSON["dates"]:
            for game in date["games"]:
                if (game["gameType"] == "R"):
                    finalScore = Game(Team(game["teams"]["home"]["team"]["id"]), Team(
                        game["teams"]["away"]["team"]["id"]))
                    finalScore.predictFinalScore()
                    finalScore.printFinalScore()

                    self.standings.teamData[str(
                        finalScore.winningTeam.id)]["W"] += 1
                    self.standings.teamData[str(
                        finalScore.winningTeam.id)]["P"] += 2

                    if finalScore.ot:
                        self.standings.teamData[str(
                            finalScore.losingTeam.id)]["OTL"] += 1
                        self.standings.teamData[str(
                            finalScore.losingTeam.id)]["P"] += 1
                    else:
                        self.standings.teamData[str(
                            finalScore.losingTeam.id)]["L"] += 1

# Series class
# Member Variables:
#     topSeed - Team object representing the top-seeded team in the series
#     bottomSeed - Team object representing the bottom-seeded team in the series
#     topSeedWins - Integer representing number of games the top-seeded team
#         has won in the series
#     bottomSeedWins - Integer representing number of games the bottom-seeded team
#         has won in the series
#     gameNum - Integer representing which game in the series is next to be played (1 to 7)
#     seriesWinner - Team object representing the team that won the series
# Methods:
#     simSeries - Simulates each game of the series, prints the results
class Series:
    # Series(topSeed, bottomSeed)
    # Arguments:
    #     topSeed: Team object representing the top seed of the series
    #     bottomSeed: Team object representing the bottom seed in the series
    def __init__(self, topSeed, bottomSeed):
        self.topSeed = topSeed
        self.bottomSeed = bottomSeed
        self.topSeedWins = 0
        self.bottomSeedWins = 0
        self.gameNum = 1

    # simSeries()
    # Simulates each game of the series and updates the seriesWinner
    def simSeries(self):
        while self.topSeedWins < 4 and self.bottomSeedWins < 4:
            if self.gameNum in [1, 2, 5, 7]:
                finalScore = Game(Team(self.topSeed.id),
                                  Team(self.bottomSeed.id))
            else:
                finalScore = Game(Team(self.bottomSeed.id),
                                  Team(self.topSeed.id))

            finalScore.predictFinalScore()
            finalScore.printFinalScore(lineEnd="")

            if finalScore.winningTeam.id == self.topSeed.id:
                self.topSeedWins += 1
            else:
                self.bottomSeedWins += 1

            print(f" [{seasonData[str(self.topSeed.id)]['abbreviation']} {self.topSeedWins} - {self.bottomSeedWins} {seasonData[str(self.bottomSeed.id)]['abbreviation']}]")

            self.gameNum += 1

        if self.topSeedWins == 4:
            self.seriesWinner = self.topSeed
        else:
            self.seriesWinner = self.bottomSeed

        print(
            f"{seasonData[str(self.seriesWinner.id)]['abbreviation']} wins the series 4-{min(self.topSeedWins, self.bottomSeedWins)}")
        print("------------------------------")

# Playoff class
# Member Variables:
#     playoffInfo: Dictionary with information on how teams are seeded and
#         matched up in the playoffs. The 'order' key has an ordered list of team
#         ids representing the matchups, and there is a key for each team id,
#         with the value representing the team's seed in the regular season
# Methods:
#     simPlayoffs - Simulates all series in the playoffs based on teams in playoffInfo
class Playoff:
    # Playoff(standings)
    # Arguments:
    #     standings: A Standings object representing the standings of the regular season
    def __init__(self, standings):
        self.playoffInfo = {"order": [0, 0, 0, 0,
                                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
        spotsInWest = 0
        spotsInEast = 0
        sortedStandings = standings.getStandings()

        for i in range(len(sortedStandings)):
            if seasonData[sortedStandings[i][0]]['abbreviation'] in ['WSH', 'NYI', 'PIT', "TBL", 'BOS', 'TOR', 'CAR', 'CBJ', 'MTL', 'FLA', 'PHI', 'NYR', 'BUF', 'DET', 'NJD', 'OTT']:
                if spotsInEast < 8:
                    if spotsInEast == 0:
                        self.playoffInfo["order"][8] = int(
                            sortedStandings[i][0])
                    elif spotsInEast == 1:
                        self.playoffInfo["order"][12] = int(
                            sortedStandings[i][0])
                    elif spotsInEast == 2:
                        self.playoffInfo["order"][14] = int(
                            sortedStandings[i][0])
                    elif spotsInEast == 3:
                        self.playoffInfo["order"][10] = int(
                            sortedStandings[i][0])
                    elif spotsInEast == 4:
                        self.playoffInfo["order"][11] = int(
                            sortedStandings[i][0])
                    elif spotsInEast == 5:
                        self.playoffInfo["order"][15] = int(
                            sortedStandings[i][0])
                    elif spotsInEast == 6:
                        self.playoffInfo["order"][13] = int(
                            sortedStandings[i][0])
                    elif spotsInEast == 7:
                        self.playoffInfo["order"][9] = int(
                            sortedStandings[i][0])

                    spotsInEast += 1
            elif spotsInWest < 8:
                if spotsInWest == 0:
                    self.playoffInfo["order"][0] = int(sortedStandings[i][0])
                elif spotsInWest == 1:
                    self.playoffInfo["order"][4] = int(sortedStandings[i][0])
                elif spotsInWest == 2:
                    self.playoffInfo["order"][6] = int(sortedStandings[i][0])
                elif spotsInWest == 3:
                    self.playoffInfo["order"][2] = int(sortedStandings[i][0])
                elif spotsInWest == 4:
                    self.playoffInfo["order"][3] = int(sortedStandings[i][0])
                elif spotsInWest == 5:
                    self.playoffInfo["order"][7] = int(sortedStandings[i][0])
                elif spotsInWest == 6:
                    self.playoffInfo["order"][5] = int(sortedStandings[i][0])
                elif spotsInWest == 7:
                    self.playoffInfo["order"][1] = int(sortedStandings[i][0])

                spotsInWest += 1

            self.playoffInfo[sortedStandings[i][0]] = i + 1

    # simPlayoffs()
    # Simulates each game of the playoffs and prints the Stanley Cup Champion
    def simPlayoffs(self):
        series = [None] * 15

        for i in range(15):
            series[i] = Series(Team(0), Team(0))

        for teamNum in range(16):
            if series[teamNum // 2].topSeed.id == 0:
                series[teamNum //
                       2].topSeed = Team(self.playoffInfo["order"][teamNum])
            else:
                series[teamNum //
                       2].bottomSeed = Team(self.playoffInfo["order"][teamNum])
        for i in range(8):
            if self.playoffInfo[str(series[i].topSeed.id)] > self.playoffInfo[str(series[i].bottomSeed.id)]:
                series[i].topSeed, series[i].bottomSeed = series[i].bottomSeed, series[i].topSeed

        for i in range(8):
            series[i].simSeries()

            if series[(i // 2) + 8].topSeed.id == 0:
                series[(i // 2) + 8].topSeed = series[i].seriesWinner
            else:
                series[(i // 2) + 8].bottomSeed = series[i].seriesWinner

        for i in range(8, 12):
            if self.playoffInfo[str(series[i].topSeed.id)] > self.playoffInfo[str(series[i].bottomSeed.id)]:
                series[i].topSeed, series[i].bottomSeed = series[i].bottomSeed, series[i].topSeed

        for i in range(8, 12):
            series[i].simSeries()

            if series[((i - 8) // 2) + 12].topSeed.id == 0:
                series[((i - 8) // 2) + 12].topSeed = series[i].seriesWinner
            else:
                series[((i - 8) // 2) + 12].bottomSeed = series[i].seriesWinner

        for i in range(12, 14):
            if self.playoffInfo[str(series[i].topSeed.id)] > self.playoffInfo[str(series[i].bottomSeed.id)]:
                series[i].topSeed, series[i].bottomSeed = series[i].bottomSeed, series[i].topSeed

        for i in range(12, 14):
            series[i].simSeries()

            if series[14].topSeed.id == 0:
                series[14].topSeed = series[i].seriesWinner
            else:
                series[14].bottomSeed = series[i].seriesWinner

        if self.playoffInfo[str(series[14].topSeed.id)] > self.playoffInfo[str(series[14].bottomSeed.id)]:
            series[14].topSeed, series[14].bottomSeed = series[14].bottomSeed, series[14].topSeed

        series[14].simSeries()

        print(
            f"Stanley Cup Champions: {seasonData[str(series[14].seriesWinner.id)]['abbreviation']}")

# Simulate the regular season
regularSeason = Season()
regularSeason.simSeason()
regularSeason.standings.printStandings()

# Simulate the playoffs based on the data from the regular season
stanleyCupPlayoffs = Playoff(regularSeason.standings)
stanleyCupPlayoffs.simPlayoffs()
