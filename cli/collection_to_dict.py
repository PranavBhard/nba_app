# Pull all games into dict
from pprint import pprint
from nba_app.cli.Mongo import Mongo

# Lazy initialization - connection created on first use
_mongo = None

def _get_mongo():
    global _mongo
    if _mongo is None:
        _mongo = Mongo()
    return _mongo

def import_collection(coll, query={'season': {'$exists':True}}):
    mongo = _get_mongo()
    stats = mongo.db[coll].find(query, {
        'homeTeam':1,'awayTeam':1,'homeWon':1,
        'game_type':1,'season':1,'date':1,
        'venue_guid':1,'year':1,'month':1,'day':1
    }, batch_size=2**8)
    # print 'after query'
    home_games = {}
    away_games = {}
    for game in stats:
        game['_id'] = str(game['_id'])
        home = game['homeTeam']['name']
        away = game['awayTeam']['name']

        key1 = game['season']
        key2 = game['date']
        home_games.setdefault(key1, {}).setdefault(key2, {})[home] = game
        away_games.setdefault(key1, {}).setdefault(key2, {})[away] = game

    return [home_games, away_games]

