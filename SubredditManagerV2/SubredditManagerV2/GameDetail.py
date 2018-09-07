class GameDetail(object):
    """Detailed stats about the game"""
    
    def __init__(self, jsonGameDetail, players):
        self.vTeamLineScore = []
        self.hTeamLineScore = []
        self.vTeamTotalStats = None
        self.hTeamTotalStats = None
        self.vTeamPlayerStats = []
        self.hTeamPlayerStats = []

        self.gameId = jsonGameDetail['basicGameData']['gameId']
        self.statusNum = jsonGameDetail['basicGameData']['statusNum']
        self.currentPeriod = jsonGameDetail['basicGameData']['period']['current']
        self.clock = jsonGameDetail['basicGameData']['clock']
        self.isHalftime = jsonGameDetail['basicGameData']['period']['isHalftime']
        self.isEndOfPeriod = jsonGameDetail['basicGameData']['period']['isEndOfPeriod']

        self.vTeamId = jsonGameDetail['basicGameData']['vTeam']['teamId']
        self.hTeamId = jsonGameDetail['basicGameData']['hTeam']['teamId']
        self.vTeamScore = jsonGameDetail['basicGameData']['vTeam']['score']
        self.hTeamScore = jsonGameDetail['basicGameData']['hTeam']['score']
        
        for period in jsonGameDetail['basicGameData']['vTeam']['linescore']:
            self.vTeamLineScore.append(period['score'])
        for period in jsonGameDetail['basicGameData']['hTeam']['linescore']:
            self.hTeamLineScore.append(period['score'])
        
        if 'stats' in jsonGameDetail:
            self.vTeamTotalStats = GameStats(jsonGameDetail['stats']['vTeam']['totals'])
            self.hTeamTotalStats = GameStats(jsonGameDetail['stats']['hTeam']['totals'])

            for player in jsonGameDetail['stats']['activePlayers']:
                if player['teamId'] == self.vTeamId:
                    self.vTeamPlayerStats.append(GameStats(player, players))
                else:
                    self.hTeamPlayerStats.append(GameStats(player, players))

        self.aotg = self.getAOTG() if self.statusNum == 3 else ''
        
    def getAOTG(self):
        myTeamId = '1610612746'
        myTeamStats = self.vTeamPlayerStats if myTeamId == self.vTeamId else self.hTeamPlayerStats 

        aotgList = sorted(myTeamStats, key=lambda x: float('0' if x.gmSc == '' else x.gmSc), reverse=True)

        aotg = aotgList[0]

        return aotg



class GameStats(object):

    def getGameScore(self):
        try:
            gameScore = int(self.points) + \
                (.4 * int(self.fgm)) + \
                (-.7 * int(self.fga)) + \
                (-.4 * int(self.fta)) + \
                (.4 * int(self.ftm)) + \
                (.7 * int(self.offReb)) + \
                (.3 * int(self.defReb)) + \
                (1 * int(self.steals)) + \
                (.7 * int(self.assists)) + \
                (.7 * int(self.blocks)) + \
                (.4 * int(self.pFouls)) + \
                (-1 * int(self.turnovers))
            gmSc = '{:.1f}'.format(gameScore)
        except:
            gmSc = ''

        return gmSc

    def __init__(self, jsonGameStats, players = None):
        if 'personId' in jsonGameStats: 
            self.playerId = jsonGameStats['personId']
            self.playerName = players.getPlayerById(jsonGameStats['personId']).playerName
            self.playerAlias = players.getPlayerById(jsonGameStats['personId']).playerAlias
        self.points = jsonGameStats['points']
        self.fgm =  jsonGameStats['fgm']
        self.fga =  jsonGameStats['fga']
        self.fgp =  jsonGameStats['fgp']
        self.ftm =  jsonGameStats['ftm']
        self.fta =  jsonGameStats['fta']
        self.ftp =  jsonGameStats['ftp']
        self.tpm =  jsonGameStats['tpm']
        self.tpa =  jsonGameStats['tpa']
        self.tpp =  jsonGameStats['tpp']
        self.offReb =  jsonGameStats['offReb']
        self.defReb =  jsonGameStats['defReb']
        self.totReb =  jsonGameStats['totReb']
        self.assists =  jsonGameStats['assists']
        self.pFouls =  jsonGameStats['pFouls']
        self.steals =  jsonGameStats['steals']
        self.turnovers =  jsonGameStats['turnovers']
        self.blocks =  jsonGameStats['blocks']
        self.plusMinus =  jsonGameStats['plusMinus']
        self.min =  jsonGameStats['min']
        self.gmSc = self.getGameScore()