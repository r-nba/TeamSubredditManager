import urllib
import requests
import json

class Data(object):
    """Data from source provider"""
    
    def refreshTeams(self):
        url = 'https://data.nba.com/data/10s/prod/v1/2016/teams.json'
        rawTeams = urllib.request.urlopen(url).read()
        self.jsonTeams = json.loads(rawTeams.decode('utf-8'))

    def refreshStandings(self):
        url = 'https://data.nba.com/data/10s/prod/v1/current/standings_conference.json'
        rawStandings = urllib.request.urlopen(url).read()
        self.jsonStandings = json.loads(rawStandings.decode('utf-8'))

    def refreshBrackets(self):
        url = 'https://data.nba.com/data/10s/prod/v1/2016/playoffsBracket.json'
        rawBrackets = urllib.request.urlopen(url).read()
        self.jsonBrackets = json.loads(rawBrackets.decode('utf-8'))

    def refreshSchedule(self, team):
        url = 'https://data.nba.com/data/10s/prod/v1/2016/teams/' + team + '/schedule.json'
        rawSchedule = urllib.request.urlopen(url).read()
        self.jsonSchedule = json.loads(rawSchedule.decode('utf-8'))

    def refreshGameDetail(self, gameDate, gameId):
        url = 'https://data.nba.com/data/10s/prod/v1/' + gameDate + '/' + gameId + '_boxscore.json'
        rawGameDetail = urllib.request.urlopen(url).read()
        self.jsonGameDetail = json.loads(rawGameDetail.decode('utf-8'))

    def refreshPlayers(self):
        playersFileLoc = 'D:\\Dev\\SubredditManagerV2\\players.json'
        with open(playersFileLoc, 'r') as playersFile:
            self.jsonPlayers = json.loads(playersFile.read())

        print('done')


    def refreshAll(self):
        self.refreshTeams()
        self.refreshStandings()
        self.refreshBrackets()
        self.refreshSchedule(self.myTeam)

    def __init__(self, team):
        print('starting data')
        
        self.myTeam = team
        self.jsonTeams = None
        self.jsonStandings = None
        self.jsonSchedule = None
        self.jsonBrackets = None
        self.jsonGameDetail = None
        self.jsonPlayers = None
        self.refreshPlayers()
