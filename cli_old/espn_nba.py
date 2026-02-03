#!/usr/bin/env python3
"""
ESPN NBA Game Stats Scraper

Scrapes game box scores from ESPN and stores them in MongoDB.
Optionally also scrapes individual player stats.

Usage:
    python espn_nba.py                              # Scrape today's games + players
    python espn_nba.py --date 2025-03-13            # Scrape specific date + players
    python espn_nba.py --date-range 2025-03-01,2025-03-15  # Scrape date range + players
    python espn_nba.py --no-players                 # Scrape team stats only (no player stats)
"""

import argparse
import re
from lxml import html
import requests
from datetime import date, timedelta, datetime
from pprint import pprint
from nba_app.core.mongo import Mongo
from bs4 import BeautifulSoup as BSoup
from nba_app.cli_old.espn_nba_players import scrape_player_stats

mongo = Mongo()
db = mongo.db

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


def parse_game_id(espn_link: str) -> str:
    """Extract game_id from ESPN link."""
    if not espn_link:
        return None
    match = re.search(r'gameId/(\d+)', espn_link)
    if match:
        return match.group(1)
    return None


def scrape_date(target_date: date, update: bool = True, scrape_players: bool = True):
    """
    Scrape all games for a specific date.
    
    Args:
        target_date: Date to scrape
        update: If True, update database
        scrape_players: If True, also scrape individual player stats
    """
    y = str(target_date.year)
    m = str(target_date.month).zfill(2)
    d = str(target_date.day).zfill(2)
    datestr = f"{y}-{m}-{d}"
    
    url = f'http://www.espn.com/nba/scoreboard/_/date/{y}{m}{d}'
    boxscore = requests.get(url, headers=headers)
    
    boxStr = boxscore.content
    linkBase = 'https://www.espn.com/'
    linkStr = 'nba/boxscore/_/gameId/'
    
    gamesData = boxStr.decode('utf-8')
    
    currentIndex = gamesData.find(linkStr)
    
    games_scraped = 0
    
    if currentIndex != -1:
        boxscoreLinks = []
        while gamesData.find(linkStr, currentIndex) != -1:
            currentIndex = gamesData.find(linkStr, currentIndex)
            gameIdIndex = currentIndex + len(linkStr)
            if gamesData[gameIdIndex:gameIdIndex+9].isdigit():
                full_link = linkBase + linkStr + gamesData[gameIdIndex:gameIdIndex+9]
                if full_link not in boxscoreLinks:
                    boxscoreLinks.append(full_link)
                currentIndex += len(linkStr)
        
        for link in boxscoreLinks:
            statLink = link.replace('boxscore', 'matchup')
            
            try:
                statReq = requests.get(statLink, headers=headers)
                game_view = BSoup(statReq.content.decode('utf-8'), features="lxml")
                
                names = game_view.find_all('div', {"class": "ZkLST"})
                name_exists = len(names) > 1
                
                if name_exists:
                    desc = game_view.find('div', {'class': 'ubPuV'})
                    if desc:
                        desc = desc.get_text()
                        game_type = None
                    else:
                        desc = 'Regular Season'
                        game_type = 'regseason'
                    
                    if 'preseason' in desc.lower():
                        game_type = 'preseason'
                        continue
                    elif '- game' in desc.lower():
                        game_type = 'playoffs'
                    elif 'play-in' in desc.lower():
                        game_type = 'playin'
                    elif 'all-star' in desc.lower() or 'star' in desc.lower():
                        game_type = 'allstar'
                        continue
                    elif 'in-season' in desc.lower():
                        game_type = 'regseason'
                    elif game_type is None:
                        game_type = 'regseason'
                    
                    if int(m) > 8:
                        if game_type == 'playoffs':
                            season = f'{int(y)-1}-{int(y)}'
                        else:
                            season = f'{int(y)}-{int(y)+1}'
                    else:
                        season = f'{int(y)-1}-{int(y)}'
                    
                    # Parse game_id from link
                    game_id = parse_game_id(link)
                    
                    game_data = {
                        'homeTeam': {}, 'awayTeam': {}, 'espn_link': link,
                        'game_id': game_id,
                        'description': desc, 'game_type': game_type, 'season': season, 'date': datestr,
                    }
                    
                    game_data['awayTeam']['name'] = names[0].get_text()
                    game_data['homeTeam']['name'] = names[1].get_text()
                    
                    game_data['year'] = int(y)
                    game_data['month'] = int(m)
                    game_data['day'] = int(d)
                    
                    # Get team stats div
                    team_stats_soup = game_view.find_all('div', {'class': 'PageLayout__Main'})[0]
                    stats_table = team_stats_soup.find_all('tbody', {'class': 'Table__TBODY'})
                    if stats_table:
                        stats_table = stats_table[0]
                    else:
                        continue
                    
                    rows = stats_table.find_all('tr', {'class': 'Table__TR'})
                    
                    # FGs
                    fgs = rows[0]
                    away_fgs = fgs.find_all('td')[1].get_text()
                    game_data['awayTeam']['FG_made'] = int(away_fgs.split('-')[0])
                    game_data['awayTeam']['FG_att'] = int(away_fgs.split('-')[1])
                    game_data['awayTeam']['FGp'] = game_data['awayTeam']['FG_made'] / float(game_data['awayTeam']['FG_att'])
                    
                    home_fgs = fgs.find_all('td')[2].get_text()
                    game_data['homeTeam']['FG_made'] = int(home_fgs.split('-')[0])
                    game_data['homeTeam']['FG_att'] = int(home_fgs.split('-')[1])
                    game_data['homeTeam']['FGp'] = game_data['homeTeam']['FG_made'] / float(game_data['homeTeam']['FG_att'])
                    
                    # Threes
                    threes = rows[2]
                    away_threes = threes.find_all('td')[1].get_text()
                    game_data['awayTeam']['three_made'] = int(away_threes.split('-')[0])
                    game_data['awayTeam']['three_att'] = int(away_threes.split('-')[1])
                    game_data['awayTeam']['three_percent'] = game_data['awayTeam']['three_made'] / float(game_data['awayTeam']['three_att']) if game_data['awayTeam']['three_att'] > 0 else 0
                    
                    home_threes = threes.find_all('td')[2].get_text()
                    game_data['homeTeam']['three_made'] = int(home_threes.split('-')[0])
                    game_data['homeTeam']['three_att'] = int(home_threes.split('-')[1])
                    game_data['homeTeam']['three_percent'] = game_data['homeTeam']['three_made'] / float(game_data['homeTeam']['three_att']) if game_data['homeTeam']['three_att'] > 0 else 0
                    
                    # Free throws
                    free_throws = rows[4]
                    away_frees = free_throws.find_all('td')[1].get_text()
                    game_data['awayTeam']['FT_made'] = int(away_frees.split('-')[0])
                    game_data['awayTeam']['FT_att'] = int(away_frees.split('-')[1])
                    game_data['awayTeam']['FTp'] = game_data['awayTeam']['FT_made'] / float(game_data['awayTeam']['FT_att']) if game_data['awayTeam']['FT_att'] > 0 else 0
                    
                    home_frees = free_throws.find_all('td')[2].get_text()
                    game_data['homeTeam']['FT_made'] = int(home_frees.split('-')[0])
                    game_data['homeTeam']['FT_att'] = int(home_frees.split('-')[1])
                    game_data['homeTeam']['FTp'] = game_data['homeTeam']['FT_made'] / float(game_data['homeTeam']['FT_att']) if game_data['homeTeam']['FT_att'] > 0 else 0
                    
                    # Rebounds
                    game_data['awayTeam']['total_reb'] = int(rows[6].find_all('td')[1].get_text())
                    game_data['awayTeam']['off_reb'] = int(rows[7].find_all('td')[1].get_text())
                    game_data['awayTeam']['def_reb'] = int(rows[8].find_all('td')[1].get_text())
                    
                    game_data['homeTeam']['total_reb'] = int(rows[6].find_all('td')[2].get_text())
                    game_data['homeTeam']['off_reb'] = int(rows[7].find_all('td')[2].get_text())
                    game_data['homeTeam']['def_reb'] = int(rows[8].find_all('td')[2].get_text())
                    
                    # Assists/steals/blocks
                    game_data['awayTeam']['assists'] = int(rows[9].find_all('td')[1].get_text())
                    game_data['awayTeam']['steals'] = int(rows[10].find_all('td')[1].get_text())
                    game_data['awayTeam']['blocks'] = int(rows[11].find_all('td')[1].get_text())
                    
                    game_data['homeTeam']['assists'] = int(rows[9].find_all('td')[2].get_text())
                    game_data['homeTeam']['steals'] = int(rows[10].find_all('td')[2].get_text())
                    game_data['homeTeam']['blocks'] = int(rows[11].find_all('td')[2].get_text())
                    
                    # TO/pts off/fast break/paint/PF
                    game_data['awayTeam']['TO'] = int(rows[12].find_all('td')[1].get_text())
                    game_data['awayTeam']['pts_off_TO'] = int(rows[13].find_all('td')[1].get_text())
                    game_data['awayTeam']['fast_break_pts'] = int(rows[14].find_all('td')[1].get_text())
                    game_data['awayTeam']['pts_in_paint'] = int(rows[15].find_all('td')[1].get_text())
                    game_data['awayTeam']['PF'] = int(rows[16].find_all('td')[1].get_text())
                    
                    game_data['homeTeam']['TO'] = int(rows[12].find_all('td')[2].get_text())
                    game_data['homeTeam']['pts_off_TO'] = int(rows[13].find_all('td')[2].get_text())
                    game_data['homeTeam']['fast_break_pts'] = int(rows[14].find_all('td')[2].get_text())
                    game_data['homeTeam']['pts_in_paint'] = int(rows[15].find_all('td')[2].get_text())
                    game_data['homeTeam']['PF'] = int(rows[16].find_all('td')[2].get_text())
                    
                    # Computed metrics
                    game_data['homeTeam']['shooting_metric'] = (game_data['homeTeam']['FG_made'] + (0.5 * game_data['homeTeam']['three_made'])) / float(game_data['homeTeam']['FG_att'])
                    game_data['awayTeam']['shooting_metric'] = (game_data['awayTeam']['FG_made'] + (0.5 * game_data['awayTeam']['three_made'])) / float(game_data['awayTeam']['FG_att'])
                    
                    possessions_home = game_data['homeTeam']['FG_att'] - game_data['homeTeam']['off_reb'] + game_data['homeTeam']['TO'] + (0.4 * game_data['homeTeam']['FT_att'])
                    possessions_away = game_data['awayTeam']['FG_att'] - game_data['awayTeam']['off_reb'] + game_data['awayTeam']['TO'] + (0.4 * game_data['awayTeam']['FT_att'])
                    possessions = (possessions_home + possessions_away) / 2.0
                    
                    game_data['homeTeam']['TO_metric'] = game_data['homeTeam']['TO'] / float(possessions)
                    game_data['awayTeam']['TO_metric'] = game_data['awayTeam']['TO'] / float(possessions)
                    game_data['homeTeam']['off_reb_metric'] = game_data['homeTeam']['off_reb'] / float(game_data['homeTeam']['off_reb'] + game_data['awayTeam']['def_reb'])
                    game_data['awayTeam']['off_reb_metric'] = game_data['awayTeam']['off_reb'] / float(game_data['awayTeam']['off_reb'] + game_data['homeTeam']['def_reb'])
                    
                    # Points
                    points_rows = game_view.find('table', {'class': 'XTxDn'}).find('tbody').find_all('tr')
                    away_points = points_rows[0].find_all('td')
                    home_points = points_rows[1].find_all('td')
                    
                    game_data['awayTeam']['points'] = int(away_points[-1].get_text())
                    game_data['awayTeam']['points1q'] = int(away_points[1].get_text())
                    game_data['awayTeam']['points2q'] = int(away_points[2].get_text())
                    game_data['awayTeam']['points3q'] = int(away_points[3].get_text())
                    game_data['awayTeam']['points4q'] = int(away_points[4].get_text())
                    
                    # OT
                    game_data['OT'] = len(away_points) > 6
                    game_data['awayTeam']['pointsOT'] = 0
                    if game_data['OT']:
                        OT_periods = len(away_points) - 6
                        for i in range(5, 5 + OT_periods):
                            game_data['awayTeam']['pointsOT'] += int(away_points[i].get_text())
                    
                    game_data['homeTeam']['points'] = int(home_points[-1].get_text())
                    game_data['homeTeam']['points1q'] = int(home_points[1].get_text())
                    game_data['homeTeam']['points2q'] = int(home_points[2].get_text())
                    game_data['homeTeam']['points3q'] = int(home_points[3].get_text())
                    game_data['homeTeam']['points4q'] = int(home_points[4].get_text())
                    
                    game_data['homeTeam']['pointsOT'] = 0
                    if game_data['OT']:
                        OT_periods = len(home_points) - 6
                        for i in range(5, 5 + OT_periods):
                            game_data['homeTeam']['pointsOT'] += int(home_points[i].get_text())
                    
                    # Winner
                    game_data['homeWon'] = game_data['awayTeam']['points'] < game_data['homeTeam']['points']
                    
                    # Validate and save
                    validassists = game_data['homeTeam']['assists'] >= 0 and game_data['awayTeam']['assists'] >= 0
                    
                    if validassists:
                        query = {
                            'year': int(y),
                            'month': int(m),
                            'day': int(d),
                            'homeTeam.name': game_data['homeTeam']['name']
                        }

                        if update:
                            # Convert nested objects to dot notation to preserve existing nested fields
                            # Using $set with nested objects like {homeTeam: {...}} replaces the ENTIRE
                            # nested object. Dot notation like {'homeTeam.points': 100} merges instead.
                            flat_update = {}
                            for key, value in game_data.items():
                                if key in ('homeTeam', 'awayTeam') and isinstance(value, dict):
                                    for nested_key, nested_value in value.items():
                                        flat_update[f'{key}.{nested_key}'] = nested_value
                                else:
                                    flat_update[key] = value
                            db.stats_nba.update_one(query, {'$set': flat_update}, upsert=True)
                        
                        games_scraped += 1
                        print(f"** {y}-{m}-{d} {game_data['awayTeam']['name']}({game_data['awayTeam']['points']}) @ {game_data['homeTeam']['name']}({game_data['homeTeam']['points']}) [game_id: {game_id}]")
                        
                        # Scrape player stats if enabled
                        if scrape_players and update:
                            try:
                                player_count = scrape_player_stats(game_data, update=True)
                                print(f"   └── Scraped {player_count} player stats")
                            except Exception as pe:
                                print(f"   └── Error scraping players: {pe}")
                
            except Exception as e:
                print(f"Error scraping {link}: {e}")
                continue
    else:
        print(f'{y}-{m}-{d} no games played')
    
    return games_scraped


def main():
    parser = argparse.ArgumentParser(
        description='ESPN NBA Game Stats Scraper',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python espn_nba.py                              # Scrape today's games + player stats
  python espn_nba.py --date 2025-03-13            # Scrape specific date + player stats
  python espn_nba.py --date-range 2025-03-01,2025-03-15  # Scrape date range
  python espn_nba.py --no-players                 # Scrape team stats only (skip players)
  python espn_nba.py --date 2025-03-13 --no-players  # Specific date, no players
        """
    )
    
    parser.add_argument(
        '--date', '-d',
        type=str,
        help='Date to scrape in YYYY-MM-DD format (default: today)'
    )
    
    parser.add_argument(
        '--date-range', '-r',
        type=str,
        help='Date range to scrape in YYYY-MM-DD,YYYY-MM-DD format (start,end)'
    )
    
    parser.add_argument(
        '--no-update',
        action='store_true',
        help='Do not update database (dry run)'
    )
    
    parser.add_argument(
        '--no-players',
        action='store_true',
        help='Do not scrape individual player stats (team stats only)'
    )
    
    args = parser.parse_args()
    
    update = not args.no_update
    scrape_players = not args.no_players
    
    if args.date_range:
        # Parse date range
        try:
            start_str, end_str = args.date_range.split(',')
            start_date = datetime.strptime(start_str.strip(), '%Y-%m-%d').date()
            end_date = datetime.strptime(end_str.strip(), '%Y-%m-%d').date()
        except ValueError:
            print("Error: Invalid date range format. Use YYYY-MM-DD,YYYY-MM-DD")
            return
        
        print(f"Scraping games from {start_date} to {end_date}")
        if not scrape_players:
            print("(Player stats disabled)")
        
        total_games = 0
        current_date = start_date
        while current_date <= end_date:
            games = scrape_date(current_date, update=update, scrape_players=scrape_players)
            total_games += games
            current_date += timedelta(days=1)
        
        print(f"\nTotal games scraped: {total_games}")
    
    elif args.date:
        # Parse single date
        try:
            target_date = datetime.strptime(args.date, '%Y-%m-%d').date()
        except ValueError:
            print("Error: Invalid date format. Use YYYY-MM-DD")
            return
        
        print(f"Scraping games for {target_date}")
        if not scrape_players:
            print("(Player stats disabled)")
        games = scrape_date(target_date, update=update, scrape_players=scrape_players)
        print(f"Games scraped: {games}")
    
    else:
        # Default: today
        target_date = date.today()
        print(f"Scraping games for {target_date}")
        if not scrape_players:
            print("(Player stats disabled)")
        games = scrape_date(target_date, update=update, scrape_players=scrape_players)
        print(f"Games scraped: {games}")


if __name__ == '__main__':
    main()



