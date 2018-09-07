from Data import Data
from Teams import Teams
from Players import Players
from Schedule import Schedule
from MarkDownGenerator import MarkDownGenerator
from Reddit import Reddit
from GameDetail import GameDetail
from Brackets import Brackets

from utils import utils

import datetime
import time

class ClipperBot(object):
    """Run ClipperBot Scheduled Routines"""

    #Team Settings:
    myConference = 'West'
    myTeam = 'clippers'
    mySubreddit = 'LAClippers'
    
    #Helper Variables
    dailyWakeup = datetime.time(5) #5 am
    currentGameThreadID = ''
    currentPostGameThreadID = ''

    def wakeUp(self):

        nextGame = self.schedule.getNextGame()
        nextGameTime = utils.getGameStartTimeLocal(nextGame.startTimeUTC)
        nextGameDate = nextGameTime.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        timeBeforeNextGame = (nextGameTime - datetime.datetime.today()).total_seconds()

        if nextGameDate > datetime.datetime.today(): #No game today.
            print('no game today, update sidebar, going to sleep until tomorrow')
            self.currentGameThreadID = ''
            self.currentPostGameThreadID = ''
            self.refreshAllData()
            self.updateSidebar()

            self.sleep(self.getSecondsUntilWakeup(self.dailyWakeup))
        elif timeBeforeNextGame > 3610: #Game is on today, but it's not gametime yet.
            print('game today, going to sleep til an hour before scheduled start time')
            self.currentGameThreadID = ''
            self.currentPostGameThreadID = ''
            self.refreshAllData()
            self.updateSidebar()

            self.createPreGameThread(nextGame)

            self.sleep(timeBeforeNextGame - 3600)
        elif 0 < timeBeforeNextGame <= 3610: #Hour from game start
            print('hour before the game starts, create game thread, sleep til start time')
            self.refreshAllData()
            self.updateSidebar()
            self.currentGameThreadID = self.createGameThread(nextGame)
            
            gameDetail = self.getGameDetail(nextGame.gameId)
            self.updateGameThread(self.currentGameThreadID, gameDetail)
            
            self.sleep(300) #sleep for 5 min
        elif timeBeforeNextGame < 0 and self.currentPostGameThreadID == '': #Game On
            print('game on, start updating the game thread')
            if self.currentGameThreadID == '':
                self.currentGameThreadID = self.createGameThread(nextGame)
            
            #self.updateSidebar()    
            gameDetail = self.getGameDetail(nextGame.gameId)

            if gameDetail.statusNum == 3:
                print('game over, post postgame thread')
                self.currentPostGameThreadID = self.createPostGameThread(nextGame, gameDetail)
                self.sleep(300)
                self.refreshAllData()
                self.updateSidebar()
                self.updatePostGameThread(self.currentPostGameThreadID, gameDetail)

            self.updateGameThread(self.currentGameThreadID, gameDetail)
            self.sleep(60) #sleep 1 min
        else:
            self.currentGameThreadID = ''
            self.currentPostGameThreadID = ''
            self.sleep(self.getSecondsUntilWakeup(self.dailyWakeup))


    def updateSidebar(self):
        print('helper call: updateSidebar()')
        
        lastGame = self.schedule.games[self.schedule.lastStandardGamePlayed]
        lastGameTime = utils.getGameStartTimeLocal(lastGame.startTimeUTC)
        lastGameDate = datetime.datetime.strftime(lastGameTime, '%Y%m%d')
                
        self.data.refreshGameDetail(lastGameDate, lastGame.gameId)
        
        lastGameDetail = GameDetail(self.data.jsonGameDetail, self.players)
        aotgMD = MarkDownGenerator.getAnchorOfTheGame(lastGame, lastGameDetail)
        
        scheduleMD = MarkDownGenerator.getScheduleMarkdown(self.schedule) + aotgMD
        if self.schedule.isPlayoffs:
            standingsMD = MarkDownGenerator.getBracketsMarkdown(self.brackets.brackets)
        else:
            standingsMD = MarkDownGenerator.getStandingsMarkdown(self.teams.getStandingsByConfName(self.myConference))

        self.reddit.updateSidebar(scheduleMD, standingsMD)

    def createPreGameThread(self, game):
        print('helper call: createPreGameThread()')
        vTeam = self.teams.getTeamById(game.vTeamId)
        hTeam = self.teams.getTeamById(game.hTeamId)

        titleMD = MarkDownGenerator.getPreGameThreadTitle(game, vTeam, hTeam)

        return self.reddit.createThread(titleMD, '', 'pregame')

    def createGameThread(self, game):
        print('helper call: createGameThread()')
        vTeam = self.teams.getTeamById(game.vTeamId)
        hTeam = self.teams.getTeamById(game.hTeamId)

        titleMD = MarkDownGenerator.getGameThreadTitle(game, vTeam, hTeam)

        return self.reddit.createThread(titleMD, 'Go Clippers!', 'game')

    def createPostGameThread(self, game, gameDetail):
        print('helper call: createPostGameThread()')
        vTeam = self.teams.getTeamById(gameDetail.vTeamId)
        hTeam = self.teams.getTeamById(gameDetail.hTeamId)

        titleMD = MarkDownGenerator.getPostGameThreadTitle(game, vTeam, hTeam)
        bodyMD = MarkDownGenerator.getPostGameThreadBody(gameDetail, vTeam, hTeam)

        return self.reddit.createThread(titleMD, bodyMD, 'postgame')

    def updateGameThread(self, threadID, gameDetail):
        print('helper call: updateGameThread()')
        vTeam = self.teams.getTeamById(gameDetail.vTeamId)
        hTeam = self.teams.getTeamById(gameDetail.hTeamId)

        bodyMD = MarkDownGenerator.getGameThreadBody(gameDetail, vTeam, hTeam)

        bodyMD += '^^For ^^an ^^auto-refreshing ^^version ^^of ^^this ^^thread, ^^join ^^our ^^[reddit-stream](http://reddit-stream.com/comments/' + threadID + '/)'

        self.reddit.updateThread(threadID, bodyMD)

    def updatePostGameThread(self, threadID, gameDetail):
        print('helper call: updatePostGameThread()')
        vTeam = self.teams.getTeamById(gameDetail.vTeamId)
        hTeam = self.teams.getTeamById(gameDetail.hTeamId)

        bodyMD = MarkDownGenerator.getPostGameThreadBody(gameDetail, vTeam, hTeam)

        self.reddit.updateThread(threadID, bodyMD)
        
    def sleep(self, numSeconds):
        print('helper call: sleep()')
        curTime = datetime.datetime.now()

        print('Waking at ' + str(curTime + datetime.timedelta(seconds=numSeconds)))
        time.sleep(numSeconds)

    def getSecondsUntilWakeup(self, tm):
        print('helper call: getSecondsUntilWakeup()')
        dtTomorrow = datetime.date.today() + datetime.timedelta(days=1)
        wakeupTime = datetime.datetime.combine(dtTomorrow, tm)

        return (wakeupTime - datetime.datetime.now()).total_seconds()

    def getGameDetail(self, gameId):
        print('helper call: getGameDetail()')
        gameDate = datetime.datetime.strftime(utils.today(), '%Y%m%d')
        self.data.refreshGameDetail(gameDate, gameId)
        return GameDetail(self.data.jsonGameDetail, self.players)
    
    #Refresh All Data
    def refreshAllData(self):
        print('helper call: refreshAllData()')
        self.data.refreshAll()
        self.teams.refresh(self.data.jsonTeams, self.data.jsonStandings)
        self.schedule.refresh(self.data.jsonSchedule, self.teams)
        self.brackets.refresh(self.data.jsonBrackets, self.teams)

    #Instantiate
    def __init__(self):
        #print(self.myString)
        print('starting up ClipperBot')
        self.reddit = Reddit(self.mySubreddit)
        self.data = Data(self.myTeam)
        self.teams = Teams()
        self.brackets = Brackets()
        self.players = Players(self.data.jsonPlayers)
        self.schedule = Schedule()
        self.refreshAllData()