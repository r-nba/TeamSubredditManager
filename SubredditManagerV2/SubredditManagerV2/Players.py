class Players(object):
    """description of class"""

    def getPlayerById(self, playerId):
        for player in self.players:
            if player.playerId == playerId:
                return player

    def __init__(self, jsonPlayers):
        self.players = []

        for player in jsonPlayers['league']['standard']:
            self.players.append(Player(player))

class Player(object):

    def __init__(self, jsonPlayer):
        self.playerId = jsonPlayer['personId']
        self.teamId = jsonPlayer['teamId']
        self.playerName = jsonPlayer['firstName'] + ' ' + jsonPlayer['lastName']
        if self.playerName == 'Chris Paul': self.playerAlias = 'chris'
        elif self.playerName == 'Blake Griffin': self.playerAlias = 'blake'
        elif self.playerName == 'DeAndre Jordan': self.playerAlias = 'deandre'
        elif self.playerName == 'J.J. Redick': self.playerAlias = 'jj'
        elif self.playerName == 'Luc Mbah a Moute': self.playerAlias = 'luc'
        elif self.playerName == 'Austin Rivers': self.playerAlias = 'austin'
        elif self.playerName == 'Jamal Crawford': self.playerAlias = 'jamal'
        elif self.playerName == 'Marreese Speights': self.playerAlias = 'mo'
        elif self.playerName == 'Ray Felton': self.playerAlias = 'ray'
        elif self.playerName == 'Wesley Johnson': self.playerAlias = 'wes'
        else: self.playerAlias = 'none'