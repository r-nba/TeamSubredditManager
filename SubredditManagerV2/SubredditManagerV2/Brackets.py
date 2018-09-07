from utils import utils

class Bracket(object):

    def __init__(self, seriesId, confName, team1, team1Seed, team1Wins, team2, team2Seed, team2Wins):
        self.id = id
        self.confName = confName
        self.team1 = team1
        self.team1Seed = team1Seed
        self.team1Wins = team1Wins
        self.team2 = team2
        self.team2Seed = team2Seed
        self.team2Wins = team2Wins

class Brackets(object):

    def refresh(self, jsonBrackets, teams):
        self.brackets.clear()
        for bracket in jsonBrackets['series']:
            if bracket['roundNum'] == '1':
                self.brackets.append(Bracket(
                        bracket['seriesId'],
                        bracket['confName'],
                        teams.getTeamById(bracket['topRow']['teamId']).tricode,
                        bracket['topRow']['seedNum'],
                        bracket['topRow']['wins'],
                        teams.getTeamById(bracket['bottomRow']['teamId']).tricode,
                        bracket['bottomRow']['seedNum'],
                        bracket['bottomRow']['wins']
                    )
                )

    def __init__(self):
        self.brackets = []
        #tmpBrackets = []
        #for bracket in brackets:
        #    tmpBrackets.append(self.parseBracket(bracket))
        #self.brackets = sorted(tmpBrackets, key=attrgetter('position'))