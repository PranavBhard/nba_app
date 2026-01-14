from nba_app.cli.collection_to_dict import import_collection
from nba_app.cli.Mongo import Mongo
from datetime import datetime, timedelta, date
from dateutil import relativedelta
# mongo = Mongo()
# db = mongo.db
# stats_collection = import_collection('stats_nba')
# home_map = stats_collection[0]
# away_map = stats_collection[1]

def avg(ls):
    return sum(ls)/float(len(ls))

def getDatesFromDate(theDate, beginDate):
    dates = [beginDate+timedelta(days=x) for x in range((theDate-beginDate).days)]
    dates = [d.strftime('%Y-%m-%d') for d in dates]
    return dates

def getTeamLastNMonthsSeasonGames(team, year, month, day, season, Nmonths, stats_collection):
    home_map = stats_collection[0][season]
    theDate = datetime(year, month, day)
    beginDate = theDate - relativedelta.relativedelta(months=Nmonths)
    dates = getDatesFromDate(theDate, beginDate)
    games = []
    for d in dates:
        if d in home_map:
            home = home_map[d]
            for homeTeam,game in home.items():
                # Use .get() to handle missing game_type field (defaults to 'regseason')
                game_type = game.get('game_type', 'regseason')
                if game_type != 'preseason' and game.get('season') == season:
                    if team == game['homeTeam']['name']:
                        games.append(game)
                    elif team == game['awayTeam']['name']:
                        games.append(game)

    return games


def getTeamSeasonGamesFromDate(team, year, month, day, season, stats_collection, retHome=False, retAway=False):
    home_map = stats_collection[0][season]
    # theDate = datetime(year, month, day)
    # beginDate = datetime(year-1, month, day)

    # dates = getDatesFromDate(theDate, beginDate)
    home_games = []
    away_games = []
    # for d in dates:
    for d,home in home_map.items():
        for homeTeam,game in home.items():
            # print (homeTeam,d)
            # Use .get() to handle missing game_type field (defaults to 'regseason')
            game_type = game.get('game_type', 'regseason')
            if game_type != 'preseason' and game.get('season') == season:
                # print ('in hereee')
                # print (team,game['homeTeam']['name'])
                if team == game.get('homeTeam', {}).get('name'):
                    home_games.append(game)
                elif team == game.get('awayTeam', {}).get('name'):
                    away_games.append(game)

    if retHome:
        return home_games
    elif retAway:
        return away_games
    else:
        return home_games + away_games

def getTeamLastNDaysSeasonGames(team, year, month, day, season, Ndays, stats_collection):
    home_map = stats_collection[0][season]
    theDate = datetime(year, month, day)
    beginDate = theDate - relativedelta.relativedelta(days=Ndays)
    dates = getDatesFromDate(theDate, beginDate)
    games = []
    for d in dates:
        if d in home_map:
            home = home_map[d]
            for homeTeam,game in home.items():
                if game['game_type'] != 'preseason' and game['season']==season:
                    if team == game['homeTeam']['name']:
                        games.append(game)
                    elif team == game['awayTeam']['name']:
                        games.append(game)

    return games

# These 2 are DEPRECATED (only used in "normalized" stats)
def getTeamSeasonWins(team, year, month, day, stats_collection):
    games = getTeamSeasonGamesFromDate(team, year, month, day, stats_collection)
    wins = 0
    for game in games:
        isHome = game['homeTeam']['name'] == team
        # side = 'homeTeam' if game['homeTeam']['name'] == team else 'awayTeam'
        if (isHome and game['homeWon']) or (not isHome and not game['homeWon']):
            wins += 1
    return wins

def getTeamSeasonAverageForStat(stat, team, year, month, day, stats_collection):
    # print team,'{}-{}-{}'.format(year, month ,day),stat
    games = getTeamSeasonGamesFromDate(team, year, month, day, stats_collection)
    if len(games)==0:
        return 'SOME BS'

    opp_stat_against = 0
    for game in games:
        against = 'awayTeam' if game['homeTeam']['name'] == team else 'homeTeam'
        opp_stat_against += game[against][stat]

    retVal = opp_stat_against

    # print team,'{}-{}-{}'.format(year, month ,day),stat

    return retVal


