from utils import utils
from operator import itemgetter
from operator import attrgetter

class Team(object):
    isNBAFranchise = None
    city = ''
    altCityName = ''
    tricode = ''
    teamId = ''
    nickname = ''
    confName = ''
    divName = ''
    subreddit = ''
    arena = ''
    confRank = 0
    win = 0
    loss = 0
    record = ''
    winPct = ''
    gamesBehind = ''
    streak = ''

    def updateStanding(self, jsonStanding):
        self.confRank = int(jsonStanding['confRank'])
        self.win = jsonStanding['win']
        self.loss = jsonStanding['loss']
        self.record = self.win + '-' + self.loss
        self.winPct = jsonStanding['winPct']
        self.gamesBehind = jsonStanding['gamesBehind']
        streakType = 'W' if jsonStanding['isWinStreak'] == True else 'L'
        self.streak = streakType + jsonStanding['streak']

    def __init__(self, jsonTeam):
        self.isNBAFranchise = jsonTeam['isNBAFranchise']
        self.city = jsonTeam['city']
        self.altCityName = jsonTeam['altCityName']
        self.tricode = jsonTeam['tricode']
        self.teamId = jsonTeam['teamId']
        self.nickname = jsonTeam['nickname']
        self.confName = jsonTeam['confName']
        self.divName = jsonTeam['divName']
        self.subreddit = utils.getGameOpponentSub(jsonTeam['tricode'])
        self.arena = utils.getGameArena(jsonTeam['tricode'])
        
class Teams(object):
    """Collection of League Teams"""

    #Return team by Id
    def getTeamById(self, teamId):
        for team in self.teams:
            if team.teamId == teamId:
                return team

    #Return sorted list of teams by confRank
    def getStandingsByConfName(self, confName):
        confTeams = []

        for team in self.teams:
            if team.confName == confName:
                confTeams.append(team)

        standings = sorted(confTeams, key=attrgetter('confRank'))
        return standings

    def refresh(self, jsonTeams, jsonStandings):
        self.teams.clear()
        for jsonTeam in jsonTeams['league']['standard']:
            if jsonTeam['isNBAFranchise'] == True:
                self.teams.append(Team(jsonTeam))

        for jsonStanding in jsonStandings['league']['standard']['conference']['west']:
            self.getTeamById(jsonStanding['teamId']).updateStanding(jsonStanding)
        for jsonStanding in jsonStandings['league']['standard']['conference']['east']:
            self.getTeamById(jsonStanding['teamId']).updateStanding(jsonStanding)

    #Populate teams
    def __init__(self):
        self.teams = []