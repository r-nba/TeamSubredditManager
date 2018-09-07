from utils import utils

class Game(object):

    def __init__(self, jsonGame, teams):
        opp = jsonGame['vTeam']['teamId'] if jsonGame['isHomeTeam'] else jsonGame['hTeam']['teamId']
        wl = ''
        if jsonGame['hTeam']['score'] != '':
            hScore = int(jsonGame['hTeam']['score'])
            vScore = int(jsonGame['vTeam']['score'])
            home = jsonGame['isHomeTeam']
            wl = 'w' if (hScore > vScore and home) or (vScore > hScore and not home) else 'l' if (vScore > hScore and home) or (hScore > vScore and not home) else ''

        self.seasonStageId = jsonGame['seasonStageId']
        self.gameId = jsonGame['gameId']
        self.statusNum = jsonGame['statusNum']
        self.startTimeUTC = jsonGame['startTimeUTC']
        self.isHomeTeam = jsonGame['isHomeTeam']
        self.vTeamId = jsonGame['vTeam']['teamId']
        self.vTeamScore = jsonGame['vTeam']['score']
        self.hTeamId = jsonGame['hTeam']['teamId']
        self.hTeamScore = jsonGame['hTeam']['score']
        self.opponentTeamId = opp

        self.gMD = utils.getGameType(jsonGame['startTimeUTC'], jsonGame['statusNum'])
        self.haMD = utils.getGameHA(jsonGame['isHomeTeam'])
        self.tMD = utils.getGameOpponent(opp, teams)
        self.oppMD = utils.getGameOpponentSub(teams.getTeamById(opp).tricode)
        self.sMD = utils.getGameScore(jsonGame['vTeam']['score'], jsonGame['hTeam']['score'], wl, jsonGame['startTimeUTC'], jsonGame['statusNum'])
        self.wlMD = wl

class Schedule(object):
    """Schedule of Games for the Season"""
    isPlayoffs = 0

    def getNextGame(self):
        if self.games[self.lastStandardGamePlayed].gMD == 'TODAY':
            return self.games[self.lastStandardGamePlayed]
        return self.games[self.lastStandardGamePlayed + 1]

    def refresh(self, jsonSchedule, teams):
        lastGamePlayedIndex = 0
        self.games.clear()

        for jsonGame in jsonSchedule['league']['standard']:
            self.games.append(Game(jsonGame, teams))
            if jsonGame['statusNum'] == 3:
                lastGamePlayedIndex += 1
            if jsonGame['seasonStageId'] == 4:
                self.isPlayoffs = 1
            
        #lastGameIndex =  jsonSchedule['league']['lastStandardGamePlayedIndex']
        lastGameIndex = -1 #Force Game Played
        if lastGameIndex >= 0:
            self.lastStandardGamePlayed = lastGameIndex  
        else:
            self.lastStandardGamePlayed = lastGamePlayedIndex-1

    def __init__(self):
        self.lastStandardGamePlayed = 0
        self.games = []

        