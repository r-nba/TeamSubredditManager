from ClipperBot import ClipperBot
import sys


import datetime
from GameDetail import GameDetail
from MarkDownGenerator import MarkDownGenerator
from MarkDownGenerator import MarkDownHelpers
from Players import Players
from Reddit import Reddit

def testPostGameThread():
    gameDate = '20161027'
    cb.data.refreshGameDetail(gameDate, '0021600017')
    gameDetail = GameDetail(cb.data.jsonGameDetail, cb.players)
    vTeam = cb.teams.getTeamById(gameDetail.vTeamId)
    hTeam = cb.teams.getTeamById(gameDetail.hTeamId)
    mdg = MarkDownGenerator.getGameThreadBody(gameDetail, vTeam, hTeam)
    mdpg = MarkDownGenerator.getPostGameThreadBody(gameDetail, vTeam, hTeam)

    print('done')

def testAOTG():
    tmp = MarkDownHelpers.getAnchorOfTheGame(cb.schedule.games[cb.schedule.lastStandardGamePlayed])

    print ('done')

def testPlayerData():
    cb.data.refreshPlayers()
    players = Players(cb.data.jsonPlayers)

    print('done')

def testReddit():
    reddit = Reddit('lapiedpipers')
    reddit.unstickyGameThreads()
    submission = reddit.createThread('reddit testing again', 'more test stuff', 'pregame')
    reddit.updateThread(submission, 'updated thread body')
    reddit.updateSidebar('', '')

    print('done')


#cb = ClipperBot()
#testAOTG()
#testPostGameThread()
#testPlayerData()
testReddit()


