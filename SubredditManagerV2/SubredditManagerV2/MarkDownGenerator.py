from utils import utils
import datetime

class MarkDownGenerator():
    """Generate Markdown for Schedule, Standings and GameThreads"""

    #Regular Season Standings
    def getStandingsMarkdown(teamStandings):
        i = 0

        standingsMD = '### Western Conference\r\n'
        standingsMD += 'Pos|Team|W|L|PCT|GB|STRK\r\n'
        standingsMD += ':--:|:--:|:--:|:--:|:--:|:--:|:--:|\r\n'
        for team in teamStandings:
            if i < 15:
                standingsMD += '{0}|{1}|{2}|{3}|{4}|{5}|{6}\r\n'.format(
                    utils.boldIfClips(team.tricode, str(team.confRank)),
                    utils.boldIfClips(team.tricode, team.tricode),
                    utils.boldIfClips(team.tricode, str(team.win)),
                    utils.boldIfClips(team.tricode, str(team.loss)),
                    utils.boldIfClips(team.tricode, team.winPct),
                    utils.boldIfClips(team.tricode, team.gamesBehind),
                    utils.boldIfClips(team.tricode, '[' + team.streak + '](#s' + team.streak[0:1].lower() + ')')
                )
            i += 1
        return standingsMD

    #Playoff Brackets
    def getBracketsMarkdown(brackets):
        WCBracketMD = '### Western Conference\r\n-|Series|-\r\n:--:|:--:|:--:|:--:|:--:\r\n'
        ECBracketMD = '### Eastern Conference\r\n-|Series|-\r\n:--:|:--:|:--:|:--:|:--:\r\n'

        for bracket in brackets:
            if bracket.confName == 'West':
                WCBracketMD += '^^{0} []({1}) {2}|{3} - {4}|{5} []({6}) ^^{7}\r\n'.format(
                    bracket.team1Seed,
                    utils.getGameOpponentSub(bracket.team1),
                    bracket.team1,
                    bracket.team1Wins,
                    bracket.team2Wins,
                    bracket.team2,
                    utils.getGameOpponentSub(bracket.team2),
                    bracket.team2Seed
                )
            else:
                ECBracketMD += '^^{0} []({1}) {2}|{3} - {4}|{5} []({6}) ^^{7}\r\n'.format(
                    bracket.team1Seed,
                    utils.getGameOpponentSub(bracket.team1),
                    bracket.team1,
                    bracket.team1Wins,
                    bracket.team2Wins,
                    bracket.team2,
                    utils.getGameOpponentSub(bracket.team2),
                    bracket.team2Seed
                )

        bracketMD = WCBracketMD + ECBracketMD

        return bracketMD

    #Regular Season Schedule
    def getScheduleMarkdown(schedule):
        if schedule.isPlayoffs == 1:
            return MarkDownGenerator.getPlayoffScheduleMarkdown(schedule)

        prevGameIndex = schedule.lastStandardGamePlayed
        scheduleMD = ''

        for i in range (0, 2):        
            scheduleMD += '* [{0}](#g)[{1}](#ha)[](#b)[{2}](#t)[]({3} "opp")[](/r/laclippers)[{4}](#s{5})\r\n'.format(
                schedule.games[prevGameIndex + i].gMD,
                schedule.games[prevGameIndex + i].haMD,
                schedule.games[prevGameIndex + i].tMD,
                schedule.games[prevGameIndex + i].oppMD,
                schedule.games[prevGameIndex + i].sMD,
                schedule.games[prevGameIndex + i].wlMD
            )

        scheduleMD += '* [TICKET BUYING AND SELLING THREAD](/6579rh "tickets")\r\n'

        return scheduleMD

    #Playoff Season Schedule
    def getPlayoffScheduleMarkdown(schedule):
        scheduleMD = ''
        lastSeriesIndex = len(schedule.games) - 7

        for i in range (0, 7):        
            scheduleMD += '* [{0}](#g)[{1}](#ha)[](#b)[{2}](#t)[]({3} "opp")[](/r/laclippers)[{4}](#s{5})\r\n'.format(
                "GAME " + str(i + 1),
                schedule.games[lastSeriesIndex + i].haMD,
                schedule.games[lastSeriesIndex + i].tMD,
                schedule.games[lastSeriesIndex + i].oppMD,
                schedule.games[lastSeriesIndex + i].sMD,
                schedule.games[lastSeriesIndex + i].wlMD
            )

        scheduleMD += '* [TICKET BUYING AND SELLING THREAD](/6579rh "tickets")\r\n'

        return scheduleMD

    def getPreGameThreadTitle(game, vTeam, hTeam):
        gameStartTimeLocal = utils.getGameStartTimeLocal(game.startTimeUTC)
        gameTimeMD = datetime.datetime.strftime(gameStartTimeLocal, '%I:%M %p')

        title = '[PRE GAME] {0} {1} ({2}) @ {3} {4} ({5}) (@ {6})'.format(
            vTeam.city,
            vTeam.nickname,
            vTeam.record,
            hTeam.city,
            hTeam.nickname,
            hTeam.record,
            gameTimeMD
        )

        return title

    def getGameThreadTitle(game, vTeam, hTeam):
        gameStartTimeLocal = utils.getGameStartTimeLocal(game.startTimeUTC)
        gameDate = gameStartTimeLocal.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        gameDateMD = datetime.datetime.strftime(gameDate, '%B %d, %Y')

        title = '[GAME THREAD] {0} {1} ({2}) @ {3} {4} ({5}) ({6})'.format(
            vTeam.city,
            vTeam.nickname,
            vTeam.record,
            hTeam.city,
            hTeam.nickname,
            hTeam.record,
            gameDateMD
        )

        return title

    def getGameThreadBody(gameDetail, vTeam, hTeam):
        curPeriod = int(gameDetail.currentPeriod)
        curOT = curPeriod - 4
        strPeriod = '' if curPeriod == 0 else 'Q' + str(curPeriod) if curPeriod <= 4 else 'OT' + str(curOT)
        header = '###[{0}](#tme)[{1}](#qtr)[{2}](#loc)\r\n'.format(
            '--:--' if (gameDetail.isEndOfPeriod or gameDetail.isHalftime or gameDetail.statusNum == 1) else 'FINAL' if gameDetail.statusNum == 3 else gameDetail.clock, 
            '' if gameDetail.statusNum == 3 else \
                'HALFTIME' if gameDetail.isHalftime else \
                'END ' + strPeriod if gameDetail.isEndOfPeriod else \
                strPeriod, 
            hTeam.arena
        )

        score = MarkDownHelpers.getGameThreadScore(gameDetail.vTeamScore, vTeam)
        score += MarkDownHelpers.getGameThreadScore(gameDetail.hTeamScore, hTeam) + '\r\n'

        lineScore = MarkDownHelpers.getGameThreadLineScoreTable(gameDetail, hTeam, vTeam)
        
        vTeamBox = MarkDownHelpers.getGameThreadPlayerStatsTable(gameDetail.vTeamPlayerStats, vTeam)

        hTeamBox = MarkDownHelpers.getGameThreadPlayerStatsTable(gameDetail.hTeamPlayerStats, hTeam)
        
        teamStats = MarkDownHelpers.getGameThreadTeamStatsTable(gameDetail, hTeam, vTeam)

        threadBody = header + score + lineScore + vTeamBox + hTeamBox + teamStats
        return threadBody

    def getPostGameThreadTitle(gameDetail, vTeam, hTeam):
        gameStartTimeLocal = utils.getGameStartTimeLocal(gameDetail.startTimeUTC)
        gameDate = gameStartTimeLocal.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        gameDateMD = datetime.datetime.strftime(gameDate, '%B %d, %Y')

        title = '[POST GAME THREAD] {0} {1} @ {2} {3} ({4})'.format(
            vTeam.city,
            vTeam.nickname,
            hTeam.city,
            hTeam.nickname,
            gameDateMD
        )

        return title


    def getPostGameThreadBody(gameDetail, vTeam, hTeam):
        header = '###[{0}](#tme)[{1}](#qtr)[{2}](#loc)\r\n'.format(
           'FINAL', 
            '' ,
            hTeam.arena
        )

        score = MarkDownHelpers.getGameThreadScore(gameDetail.vTeamScore, vTeam)
        score += MarkDownHelpers.getGameThreadScore(gameDetail.hTeamScore, hTeam) + '\r\n'

        lineScore = MarkDownHelpers.getGameThreadLineScoreTable(gameDetail, hTeam, vTeam)
        
        vTeamBox = MarkDownHelpers.getGameThreadPlayerStatsTable(gameDetail.vTeamPlayerStats, vTeam)

        hTeamBox = MarkDownHelpers.getGameThreadPlayerStatsTable(gameDetail.hTeamPlayerStats, hTeam)
        
        teamStats = MarkDownHelpers.getGameThreadTeamStatsTable(gameDetail, hTeam, vTeam)

        threadBody = header + score + lineScore + vTeamBox + hTeamBox + teamStats
        return threadBody

    def getAnchorOfTheGame(game, gameDetail):
        gameTime = utils.getGameStartTimeLocal(game.startTimeUTC)
        gameDate = datetime.datetime.strftime(gameTime, '%m/%d/%y')
        timeSinceGame = (datetime.datetime.today() - gameTime).total_seconds()
        aotg = gameDetail.aotg

        #if Loss or game is older than 20 hours (72000 seconds), return ''
        if timeSinceGame > 72000 or game.wlMD == 'l' or aotg.playerAlias == 'none':
            aotgMD = ''
        else: 
            aotgPts = int(aotg.points)
            aotgReb = (.7 * int(aotg.offReb)) + (.3 * int(aotg.defReb))
            aotgStl = (1 * int(aotg.steals))
            aotgAst = (.7 * int(aotg.assists))
            aotgBlk = (.7 * int(aotg.blocks)) 

            stats = [['PTS', aotgPts, aotg.points], ['REB', aotgReb, aotg.totReb], ['STL', aotgStl, aotg.steals], ['AST', aotgAst, aotg.assists], ['BLK', aotgBlk, aotg.blocks]]
            sortedStats = sorted(stats, key=lambda stat: stat[1], reverse=True)
            aotgMD = '\r\n[](#AOTG)[](#aotg_{0})[{1}](#date)[{2} | {3} | {4}](#stat)\r\n'.format(
                aotg.playerAlias,
                gameDate,
                sortedStats[0][2] + ' ' + sortedStats[0][0],
                sortedStats[1][2] + ' ' + sortedStats[1][0],
                sortedStats[2][2] + ' ' + sortedStats[2][0]
            )

        return aotgMD


class MarkDownHelpers():
    
    def getGameThreadScore(gameDetailScore, team):
        score = '* []({0})[{1}](#team)[{2}, {3}](#sub)[{4}](#sco)\r\n'.format(
            team.subreddit,
            team.city + ' ' + team.nickname,
            team.record,
            utils.getOrdinalNumber(team.confRank) + ' ' + team.confName + 'ern',
            gameDetailScore,
        ) 

        return score

    def getGameThreadLineScore(gameDetailLineScore, totalScore, team):
        lineScore = '[](' + team.subreddit + ')' + team.nickname + '|'
        for score in gameDetailLineScore:
            lineScore += score + '|'
        lineScore += totalScore + '\r\n'

        return lineScore

    def getGameThreadLineScoreTable(gameDetail, hTeam, vTeam):
        numOT = int(gameDetail.currentPeriod) - 4
        otHeader = ''
        for i in range(1, numOT+1):
            otHeader += 'OT' + str(i) + '|'

        lineScoreTable = '#####Line Score\r\n'
        lineScoreTable += 'Team|Q1|Q2|Q3|Q4|{0}{1}\r\n'.format(otHeader, 'TOTAL') #OT INFO
        lineScoreTable += ':--|:--:|:--:|:--:|:--:|:--:{0}\r\n'.format('|:--:'*numOT) #OT INFO
        lineScoreTable += MarkDownHelpers.getGameThreadLineScore(gameDetail.vTeamLineScore, gameDetail.vTeamScore, vTeam)
        lineScoreTable += MarkDownHelpers.getGameThreadLineScore(gameDetail.hTeamLineScore, gameDetail.hTeamScore, hTeam) + '\r\n'
        lineScoreTable += '##### | \r\n\r\n'

        return lineScoreTable

    def getGameThreadPlayerStats(playerStats):
        playerStatsMD = '{0}|{1}|{2}|{3}|{4}|{5}|{6}|{7}|{8}|{9}|{10}|{11}|{12}|{13}|{14}\r\n'.format(
            playerStats.playerName,
            playerStats.min,
            playerStats.points,
            playerStats.fgm + '-' + playerStats.fga + ' (' + playerStats.fgp + '%)',
            playerStats.tpm + '-' + playerStats.tpa + ' (' + playerStats.tpp + '%)',
            playerStats.ftm + '-' + playerStats.fta + ' (' + playerStats.ftp + '%)',
            playerStats.offReb,
            playerStats.totReb,
            playerStats.assists,
            playerStats.pFouls,
            playerStats.steals,
            playerStats.turnovers,
            playerStats.blocks,
            playerStats.plusMinus,
            playerStats.gmSc
        )

        return playerStatsMD

    def getGameThreadPlayerStatsTable(gameStats, team):
        playerStatsTable = '#####' + team.nickname + ' ' + 'Stats\r\n'
        playerStatsTable += team.nickname + '|MIN|PTS|FGM-A (Pct)|3PM-A (Pct)|FTM-A (Pct)|OREB|REB|AST|PF|ST|TO|BLK|+/-|GmSc\r\n'
        playerStatsTable += ':--|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:\r\n'
        for playerStats in gameStats:
            playerStatsTable += MarkDownHelpers.getGameThreadPlayerStats(playerStats)
        playerStatsTable += '\r\n##### | \r\n\r\n'

        return playerStatsTable
        

    def getGameThreadTeamStats(gameStats, team):
        if gameStats == None: return ''
        teamStats = '{0}|{1}|{2}|{3}|{4}|{5}|{6}|{7}|{8}|{9}|{10}|{11}\r\n'.format(
            '[](' + team.subreddit +') ' + team.nickname,
            gameStats.points,
            gameStats.fgm + '-' + gameStats.fga + ' (' + gameStats.fgp + '%)',
            gameStats.tpm + '-' + gameStats.tpa + ' (' + gameStats.tpp + '%)',
            gameStats.ftm + '-' + gameStats.fta + ' (' + gameStats.ftp + '%)',
            gameStats.offReb,
            gameStats.totReb,
            gameStats.assists,
            gameStats.pFouls,
            gameStats.steals,
            gameStats.turnovers,
            gameStats.blocks
        )

        return teamStats

    def getGameThreadTeamStatsTable(gameDetail, hTeam, vTeam):
        teamStatsTable = '#####Team Stats\r\n'
        teamStatsTable += 'TOTALS|PTS|FGM-A (Pct)|3PM-A (Pct)|FTM-A (Pct)|OREB|REB|AST|PF|ST|TO|BLK\r\n'
        teamStatsTable += ':--|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:\r\n'
        teamStatsTable += MarkDownHelpers.getGameThreadTeamStats(gameDetail.vTeamTotalStats, vTeam)
        teamStatsTable += MarkDownHelpers.getGameThreadTeamStats(gameDetail.hTeamTotalStats, hTeam) + '\r\n'

        return teamStatsTable