import datetime

class utils():
    """description of class"""
    tzOffset = (datetime.datetime.now() - datetime.datetime.utcnow()).total_seconds()/3600

    teamAbbrs = [
        'ATL', 'CHA', 'MIA', 'ORL', 'WAS',
        'BOS', 'BKN', 'NYK', 'PHI', 'TOR',
        'CHI', 'CLE', 'DET', 'IND', 'MIL',
        'GSW', 'LAC', 'LAL', 'PHX', 'SAC',
        'DAL', 'HOU', 'MEM', 'NOP', 'SAS',
        'DEN', 'MIN', 'OKC', 'POR', 'UTA'
        ]
    teamSubs = [
        'atlantahawks', 'charlottehornets', 'heat', 'orlandomagic', 'washingtonwizards', 
        'bostonceltics', 'gonets', 'nyknicks', 'sixers', 'torontoraptors', 
        'chicagobulls', 'clevelandcavs', 'detroitpistons', 'pacers', 'mkebucks', 
        'warriors', 'laclippers', 'lakers', 'suns', 'kings', 
        'mavericks', 'rockets', 'memphisgrizzlies', 'nolapelicans', 'nbaspurs', 
        'denvernuggets', 'timberwolves', 'thunder', 'ripcity', 'utahjazz'
        ]
    teamArenas = [
        'Philips Arena', 'Time Warner Cable Arena', 'American Airlines Arena', 'Amway Center', 'Verizon Center',
        'TD Garden', 'Barclays Center', 'Madison Square Garden', 'Wells Fargo Center', 'Air Canada Centre',
        'United Center', 'Quicken Loans Arena', 'The Palace of Auburn Hills', 'Bankers Life Fieldhouse', 'BMO Harris Bradley Center', 'Oracle Arena', 'Staples Center', 'Staples Center', 'Talking Stick Resort Arena', 'Golden 1 Center',
        'American Airlines Arena', 'Toyota Center', 'FedExForum', 'Smoothie King Center', 'AT&T Center',
        'Pepsi Center', 'Target Center', 'Chesapeake Energy Arena', 'Moda Center', 'Vivint Smart Home Arena'
        ]

    def boldIfClips(team, text):
        if team ==  'LAC':
            text = '**' + text + '**'
        return text

    def getOrdinalNumber(number):
        if number == 1: return '1st'
        elif number == 2: return '2nd'
        elif number == 3: return '3rd'
        else: return str(number) + 'th'

    def today():
        return datetime.datetime.now().replace(hour = 0, minute = 0, second = 0, microsecond = 0)




    ### EXTRA GAME INFO HELPERS
    def getGameStartTimeLocal(gameStartTimeUTC):
        try:
            startTimeUTC = datetime.datetime.strptime(gameStartTimeUTC, '%Y-%m-%dT%H:%M:%S.%fZ')
            return startTimeUTC + datetime.timedelta(hours=utils.tzOffset)
        except:
            return datetime.datetime.strptime(gameStartTimeUTC, '%Y-%m-%d')

    def getGameType(gameStartTimeUTC, statusNum):
        today = utils.today()
        gameType = ''

        startTimeLocal = utils.getGameStartTimeLocal(gameStartTimeUTC)
        gameDate = startTimeLocal.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        
        if gameDate == today:
            if statusNum == 3:
                return 'FINAL'
            return 'TODAY'
        elif gameDate < today:
            return 'Last Game'
        elif gameDate > today:
            return 'Next Game'

    def getGameHA(isHomeTeam):
        if isHomeTeam:
            return 'Home'
        else:
            return 'Away'

    def getGameOpponent(opp, teams):
        opponent = teams.getTeamById(opp)

        return opponent.city + ' ' + opponent.nickname

    def getGameOpponentSub(oppTricode):
        for i in range(0,30):
            if utils.teamAbbrs[i] == oppTricode:
                return '/r/' + utils.teamSubs[i]
        return '/r/NBA'

    def getGameArena(tricode):
        for i in range(0,30):
            if utils.teamAbbrs[i] == tricode:
                return utils.teamArenas[i]
        return 'Outer Space Arena'

    def getGameScore(vScore, hScore, wl, gameStartTimeUTC, statusNum):
        startTimeLocal = utils.getGameStartTimeLocal(gameStartTimeUTC)
        gameDate = startTimeLocal.replace(hour = 0, minute = 0, second = 0, microsecond = 0)

        if statusNum > 1:
            return vScore + ' - ' + hScore + ' [' + wl.upper() + ']'
        else:
            if startTimeLocal.hour == 0:
                return datetime.datetime.strftime(startTimeLocal, '%a %b %d @ TBD')
            else:
                return datetime.datetime.strftime(startTimeLocal, '%a %b %d @ %I:%M %p')