#!/usr/bin/env python3

"""
ESPN NBA Player Stats Scraper

Scrapes individual player box score stats from ESPN and stores them in MongoDB.

Usage:
    python espn_nba_players.py                     # Scrape player stats for all games
    python espn_nba_players.py --date 2025-03-13   # Scrape player stats for games on a specific date
    python espn_nba_players.py --game-id 401809801 # Scrape player stats for a specific game
    python espn_nba_players.py --async             # Run in async mode with chunked threading
"""

import argparse
import re
import requests
import time
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
from typing import List, Dict, Tuple
from pymongo import MongoClient, UpdateOne
from pymongo.errors import AutoReconnect, ConnectionFailure
from nba_app.cli.Mongo import Mongo
from nba_app.config import config
from bs4 import BeautifulSoup as BSoup

# Global connection for non-async mode
mongo = Mongo()
db = mongo.db

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Async mode settings
CHUNK_SIZE = 500
MAX_WORKERS = 4  # Number of parallel threads
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds


class MongoConnectionPool:
    """
    Thread-safe MongoDB connection pool for async operations.
    Minimizes connection instantiation and handles reconnection.
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self._client = None
        self._db = None
        self._connection_lock = threading.Lock()
        self._connect()
    
    def _connect(self):
        """Establish MongoDB connection."""
        try:
            self._client = MongoClient(
                config["mongo_conn_str"],
                maxPoolSize=50,
                minPoolSize=5,
                maxIdleTimeMS=30000,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                retryWrites=True
            )
            self._db = self._client.heroku_jrgd55fg
            # Test connection
            self._client.admin.command('ping')
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise
    
    def get_db(self):
        """Get database with automatic reconnection on failure."""
        with self._connection_lock:
            try:
                # Test if connection is alive
                self._client.admin.command('ping')
            except (AutoReconnect, ConnectionFailure) as e:
                print(f"MongoDB connection lost, reconnecting... ({e})")
                time.sleep(RETRY_DELAY)
                self._connect()
        return self._db
    
    def execute_with_retry(self, operation, *args, **kwargs):
        """Execute a database operation with retry logic."""
        for attempt in range(MAX_RETRIES):
            try:
                db = self.get_db()
                return operation(db, *args, **kwargs)
            except (AutoReconnect, ConnectionFailure) as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"  Retry {attempt + 1}/{MAX_RETRIES} after error: {e}")
                    time.sleep(RETRY_DELAY * (attempt + 1))
                else:
                    raise
    
    def close(self):
        """Close the connection pool."""
        if self._client:
            self._client.close()


def parse_player_id(player_link: str) -> str:
    """Extract player_id from ESPN player link."""
    if not player_link:
        return None
    # Pattern: /id/4065732/deandre-hunter or /id/4065732
    match = re.search(r'/id/(\d+)', player_link)
    if match:
        return match.group(1)
    return None


def parse_game_id(espn_link: str) -> str:
    """Extract game_id from ESPN link."""
    if not espn_link:
        return None
    match = re.search(r'gameId/(\d+)', espn_link)
    if match:
        return match.group(1)
    return None


def parse_stat_split(stat_str: str) -> tuple:
    """Parse a stat like '6-9' into (made, att)."""
    if '-' in stat_str:
        parts = stat_str.split('-')
        try:
            return int(parts[0]), int(parts[1])
        except ValueError:
            return 0, 0
    return 0, 0


def parse_plus_minus(pm_str: str) -> int:
    """Parse plus/minus string like '+15' or '-3' into integer."""
    try:
        pm_str = pm_str.strip()
        if pm_str.startswith('+'):
            return int(pm_str[1:])
        return int(pm_str)
    except ValueError:
        return 0


def scrape_player_stats_data(game: dict) -> Tuple[List[dict], str]:
    """
    Scrape player stats for a single game WITHOUT database operations.
    
    Args:
        game: MongoDB document with espn_link field
        
    Returns:
        Tuple of (list of player stat dicts, game_id)
    """
    espn_link = game.get('espn_link')
    if not espn_link:
        return [], None
    
    game_id = game.get('game_id') or parse_game_id(espn_link)
    if not game_id:
        return [], None
    
    # Convert to boxscore URL
    boxscore_url = espn_link.replace('matchup', 'boxscore')
    if 'boxscore' not in boxscore_url:
        boxscore_url = f"https://www.espn.com/nba/boxscore/_/gameId/{game_id}"
    
    try:
        response = requests.get(boxscore_url, headers=headers, timeout=30)
        soup = BSoup(response.content.decode('utf-8'), features="lxml")
    except Exception as e:
        return [], game_id
    
    player_stats = []
    
    # Find the main content area with player tables
    main_content = soup.find('div', {'class': 'PageLayout__Main'})
    if not main_content:
        return [], game_id
    
    # Find the boxscore wrapper - it contains both teams
    boxscore_wrapper = main_content.find('div', {'class': 'Boxscore__ResponsiveWrapper'})
    if not boxscore_wrapper:
        return [], game_id
    
    # Find the Wrapper divs - each contains one team's boxscore
    team_wrappers = boxscore_wrapper.find_all('div', {'class': 'Wrapper'}, recursive=False)
    
    if len(team_wrappers) < 2:
        team_wrappers = boxscore_wrapper.find_all('div', {'class': 'BoxscoreItem__TeamName'})
        if len(team_wrappers) >= 2:
            team_wrappers = [t.find_parent('div', {'class': 'Wrapper'}) for t in team_wrappers]
            team_wrappers = [w for w in team_wrappers if w is not None]
    
    if len(team_wrappers) < 2:
        return [], game_id
    
    for team_idx, wrapper in enumerate(team_wrappers[:2]):
        is_home = team_idx == 1
        
        team_name_elem = wrapper.find('div', {'class': 'BoxscoreItem__TeamName'})
        section_team_name = team_name_elem.get_text().strip() if team_name_elem else "Unknown"
        
        home_team_name = game.get('homeTeam', {}).get('name', '')
        away_team_name = game.get('awayTeam', {}).get('name', '')
        
        if section_team_name and home_team_name and away_team_name:
            if section_team_name.upper() in home_team_name.upper() or home_team_name.upper() in section_team_name.upper():
                is_home = True
            elif section_team_name.upper() in away_team_name.upper() or away_team_name.upper() in section_team_name.upper():
                is_home = False
        
        section = wrapper.find('div', {'class': 'Boxscore'})
        if not section:
            section = wrapper
        
        tables = section.find_all('table', {'class': 'Table'})
        if len(tables) < 2:
            continue
        
        player_table = tables[0]
        stats_table = tables[1]
        
        player_tbody = player_table.find('tbody', {'class': 'Table__TBODY'})
        if not player_tbody:
            continue
        
        player_rows = player_tbody.find_all('tr', {'class': 'Table__TR'})
        stats_tbody = stats_table.find('tbody', {'class': 'Table__TBODY'})
        if not stats_tbody:
            continue
        
        stats_rows = stats_tbody.find_all('tr', {'class': 'Table__TR'})
        is_starter = True
        
        for row_idx, (player_row, stats_row) in enumerate(zip(player_rows, stats_rows)):
            header_cell = player_row.find('td', {'class': 'Table__customHeader'})
            if header_cell:
                header_text = header_cell.get_text().strip().lower()
                if 'starters' in header_text:
                    is_starter = True
                elif 'bench' in header_text:
                    is_starter = False
                continue
            
            dnp_cell = stats_row.find('td', {'class': 'BoxscoreItem__DNP'})
            if dnp_cell:
                continue
            
            player_link_elem = player_row.find('a', {'class': 'AnchorLink'})
            if not player_link_elem:
                continue
            
            player_href = player_link_elem.get('href', '')
            player_id = parse_player_id(player_href)
            if not player_id:
                continue
            
            name_elem = player_link_elem.find('span', {'class': 'Boxscore__AthleteName--long'})
            player_name = name_elem.get_text() if name_elem else 'Unknown'
            
            stat_cells = stats_row.find_all('td', {'class': 'Table__TD'})
            if len(stat_cells) < 14:
                continue
            
            try:
                min_val = int(stat_cells[0].get_text()) if stat_cells[0].get_text().isdigit() else 0
                pts = int(stat_cells[1].get_text()) if stat_cells[1].get_text().isdigit() else 0
                fg_made, fg_att = parse_stat_split(stat_cells[2].get_text())
                three_made, three_att = parse_stat_split(stat_cells[3].get_text())
                ft_made, ft_att = parse_stat_split(stat_cells[4].get_text())
                reb = int(stat_cells[5].get_text()) if stat_cells[5].get_text().isdigit() else 0
                ast = int(stat_cells[6].get_text()) if stat_cells[6].get_text().isdigit() else 0
                to = int(stat_cells[7].get_text()) if stat_cells[7].get_text().lstrip('-').isdigit() else 0
                stl = int(stat_cells[8].get_text()) if stat_cells[8].get_text().isdigit() else 0
                blk = int(stat_cells[9].get_text()) if stat_cells[9].get_text().isdigit() else 0
                oreb = int(stat_cells[10].get_text()) if stat_cells[10].get_text().isdigit() else 0
                dreb = int(stat_cells[11].get_text()) if stat_cells[11].get_text().isdigit() else 0
                pf = int(stat_cells[12].get_text()) if stat_cells[12].get_text().isdigit() else 0
                plus_minus = parse_plus_minus(stat_cells[13].get_text())
                
                player_espn_link = f"https://www.espn.com{player_href}" if player_href.startswith('/') else player_href
                
                player_stats.append({
                    'player_id': player_id,
                    'player_name': player_name,
                    'espn_link': player_espn_link,
                    'game_id': game_id,
                    'date': game.get('date'),
                    'season': game.get('season'),
                    'home': is_home,
                    'starter': is_starter,
                    'team': game.get('homeTeam', {}).get('name') if is_home else game.get('awayTeam', {}).get('name'),
                    'opponent': game.get('awayTeam', {}).get('name') if is_home else game.get('homeTeam', {}).get('name'),
                    'stats': {
                        'min': min_val, 'pts': pts, 'fg_made': fg_made, 'fg_att': fg_att,
                        'three_made': three_made, 'three_att': three_att,
                        'ft_made': ft_made, 'ft_att': ft_att,
                        'reb': reb, 'ast': ast, 'stl': stl, 'blk': blk,
                        'oreb': oreb, 'dreb': dreb, 'pf': pf, 'to': to,
                        'plus_minus': plus_minus
                    }
                })
            except Exception:
                continue
    
    return player_stats, game_id


def scrape_player_stats(game: dict, update: bool = True) -> int:
    """
    Scrape player stats for a single game.
    
    Args:
        game: MongoDB document with espn_link field
        update: If True, upsert to database
        
    Returns:
        Number of player stats scraped
    """
    espn_link = game.get('espn_link')
    if not espn_link:
        print(f"No ESPN link for game: {game.get('date')} {game.get('homeTeam', {}).get('name')}")
        return 0
    
    game_id = game.get('game_id') or parse_game_id(espn_link)
    if not game_id:
        print(f"Could not parse game_id from: {espn_link}")
        return 0
    
    # Convert to boxscore URL
    boxscore_url = espn_link.replace('matchup', 'boxscore')
    if 'boxscore' not in boxscore_url:
        boxscore_url = f"https://www.espn.com/nba/boxscore/_/gameId/{game_id}"
    
    try:
        response = requests.get(boxscore_url, headers=headers, timeout=30)
        soup = BSoup(response.content.decode('utf-8'), features="lxml")
    except Exception as e:
        print(f"Error fetching {boxscore_url}: {e}")
        return 0
    
    # Find the main content area with player tables
    main_content = soup.find('div', {'class': 'PageLayout__Main'})
    if not main_content:
        print(f"Could not find main content for game {game_id}")
        return 0
    
    # Find the boxscore wrapper - it contains both teams
    boxscore_wrapper = main_content.find('div', {'class': 'Boxscore__ResponsiveWrapper'})
    if not boxscore_wrapper:
        print(f"Could not find boxscore wrapper for game {game_id}")
        return 0
    
    # Find the Wrapper divs - each contains one team's boxscore
    # Structure: Boxscore__ResponsiveWrapper > Wrapper > Boxscore
    team_wrappers = boxscore_wrapper.find_all('div', {'class': 'Wrapper'}, recursive=False)
    
    if len(team_wrappers) < 2:
        # Fallback: try finding by team name headers
        team_wrappers = boxscore_wrapper.find_all('div', {'class': 'BoxscoreItem__TeamName'})
        if len(team_wrappers) >= 2:
            # Get parent Wrapper divs
            team_wrappers = [t.find_parent('div', {'class': 'Wrapper'}) for t in team_wrappers]
            team_wrappers = [w for w in team_wrappers if w is not None]
    
    if len(team_wrappers) < 2:
        print(f"Could not find both team boxscores for game {game_id} (found {len(team_wrappers)})")
        return 0
    
    players_scraped = 0
    
    # Process each team's boxscore
    # ESPN boxscore layout: first Wrapper is AWAY team, second Wrapper is HOME team
    for team_idx, wrapper in enumerate(team_wrappers[:2]):
        is_home = team_idx == 1  # First wrapper (0) is away, second wrapper (1) is home
        
        # Extract team name from this section for verification
        team_name_elem = wrapper.find('div', {'class': 'BoxscoreItem__TeamName'})
        section_team_name = team_name_elem.get_text().strip() if team_name_elem else "Unknown"
        
        # Determine is_home by matching team name to game data (more reliable)
        home_team_name = game.get('homeTeam', {}).get('name', '')
        away_team_name = game.get('awayTeam', {}).get('name', '')
        
        # Check if section team matches home or away
        if section_team_name and home_team_name and away_team_name:
            # Use team name matching instead of position
            if section_team_name.upper() in home_team_name.upper() or home_team_name.upper() in section_team_name.upper():
                is_home = True
            elif section_team_name.upper() in away_team_name.upper() or away_team_name.upper() in section_team_name.upper():
                is_home = False
        
        # Find the actual Boxscore section within the wrapper
        section = wrapper.find('div', {'class': 'Boxscore'})
        if not section:
            section = wrapper  # Use wrapper directly if no nested Boxscore
        
        # Find the fixed left table (player names) and stats table
        tables = section.find_all('table', {'class': 'Table'})
        
        if len(tables) < 2:
            continue
        
        player_table = tables[0]  # Fixed left table with player names
        stats_table = tables[1]   # Scrollable table with stats
        
        # Get player rows from the player name table
        player_tbody = player_table.find('tbody', {'class': 'Table__TBODY'})
        if not player_tbody:
            continue
        
        player_rows = player_tbody.find_all('tr', {'class': 'Table__TR'})
        
        # Get stats rows
        stats_tbody = stats_table.find('tbody', {'class': 'Table__TBODY'})
        if not stats_tbody:
            continue
        
        stats_rows = stats_tbody.find_all('tr', {'class': 'Table__TR'})
        
        # Process each player row, tracking starter/bench status
        is_starter = True  # Start assuming starters section
        
        for row_idx, (player_row, stats_row) in enumerate(zip(player_rows, stats_rows)):
            # Check for section header rows (starters, bench, team)
            header_cell = player_row.find('td', {'class': 'Table__customHeader'})
            if header_cell:
                header_text = header_cell.get_text().strip().lower()
                if 'starters' in header_text:
                    is_starter = True
                elif 'bench' in header_text:
                    is_starter = False
                # Skip header rows (don't process as players)
                continue
            
            # Check if DNP
            dnp_cell = stats_row.find('td', {'class': 'BoxscoreItem__DNP'})
            if dnp_cell:
                continue
            
            # Get player link and name
            player_link_elem = player_row.find('a', {'class': 'AnchorLink'})
            if not player_link_elem:
                continue
            
            player_href = player_link_elem.get('href', '')
            player_id = parse_player_id(player_href)
            
            if not player_id:
                continue
            
            # Get player name
            name_elem = player_link_elem.find('span', {'class': 'Boxscore__AthleteName--long'})
            player_name = name_elem.get_text() if name_elem else 'Unknown'
            
            # Get stats from stats row
            stat_cells = stats_row.find_all('td', {'class': 'Table__TD'})
            
            if len(stat_cells) < 14:
                continue
            
            try:
                # Extract stats based on column order:
                # MIN, PTS, FG, 3PT, FT, REB, AST, TO, STL, BLK, OREB, DREB, PF, +/-
                min_val = int(stat_cells[0].get_text()) if stat_cells[0].get_text().isdigit() else 0
                pts = int(stat_cells[1].get_text()) if stat_cells[1].get_text().isdigit() else 0
                
                fg_text = stat_cells[2].get_text()
                fg_made, fg_att = parse_stat_split(fg_text)
                
                three_text = stat_cells[3].get_text()
                three_made, three_att = parse_stat_split(three_text)
                
                ft_text = stat_cells[4].get_text()
                ft_made, ft_att = parse_stat_split(ft_text)
                
                reb = int(stat_cells[5].get_text()) if stat_cells[5].get_text().isdigit() else 0
                ast = int(stat_cells[6].get_text()) if stat_cells[6].get_text().isdigit() else 0
                # TO is at index 7, but we're pulling STL, BLK, etc.
                to = int(stat_cells[7].get_text()) if stat_cells[7].get_text().lstrip('-').isdigit() else 0
                stl = int(stat_cells[8].get_text()) if stat_cells[8].get_text().isdigit() else 0
                blk = int(stat_cells[9].get_text()) if stat_cells[9].get_text().isdigit() else 0
                oreb = int(stat_cells[10].get_text()) if stat_cells[10].get_text().isdigit() else 0
                dreb = int(stat_cells[11].get_text()) if stat_cells[11].get_text().isdigit() else 0
                pf = int(stat_cells[12].get_text()) if stat_cells[12].get_text().isdigit() else 0
                plus_minus = parse_plus_minus(stat_cells[13].get_text())
                
                # Build full ESPN link for player
                player_espn_link = f"https://www.espn.com{player_href}" if player_href.startswith('/') else player_href
                
                player_stat = {
                    'player_id': player_id,
                    'player_name': player_name,
                    'espn_link': player_espn_link,
                    'game_id': game_id,
                    'date': game.get('date'),
                    'season': game.get('season'),
                    'home': is_home,
                    'starter': is_starter,
                    'team': game.get('homeTeam', {}).get('name') if is_home else game.get('awayTeam', {}).get('name'),
                    'opponent': game.get('awayTeam', {}).get('name') if is_home else game.get('homeTeam', {}).get('name'),
                    'stats': {
                        'min': min_val,
                        'pts': pts,
                        'fg_made': fg_made,
                        'fg_att': fg_att,
                        'three_made': three_made,
                        'three_att': three_att,
                        'ft_made': ft_made,
                        'ft_att': ft_att,
                        'reb': reb,
                        'ast': ast,
                        'stl': stl,
                        'blk': blk,
                        'oreb': oreb,
                        'dreb': dreb,
                        'pf': pf,
                        'to': to,
                        'plus_minus': plus_minus
                    }
                }
                
                if update:
                    # Upsert by game_id + player_id
                    db.stats_nba_players.update_one(
                        {'game_id': game_id, 'player_id': player_id},
                        {'$set': player_stat},
                        upsert=True
                    )
                
                players_scraped += 1
                
            except Exception as e:
                print(f"Error parsing stats for player {player_id}: {e}")
                continue
    
    return players_scraped


def process_chunk(chunk_idx: int, games: List[dict], pool: MongoConnectionPool) -> Tuple[int, int, List[str]]:
    """
    Process a chunk of games sequentially, then batch upsert.
    
    Args:
        chunk_idx: Index of this chunk (for logging)
        games: List of game documents to process
        pool: Shared MongoDB connection pool
        
    Returns:
        Tuple of (players_scraped, games_processed, list of game_ids processed)
    """
    thread_name = threading.current_thread().name
    print(f"[Chunk {chunk_idx}] Starting on {thread_name} - {len(games)} games")
    
    all_player_stats = []
    processed_game_ids = []
    failed_games = 0
    
    for i, game in enumerate(games):
        game_id = game.get('game_id') or parse_game_id(game.get('espn_link', ''))
        
        try:
            player_stats, gid = scrape_player_stats_data(game)
            
            if player_stats:
                all_player_stats.extend(player_stats)
                processed_game_ids.append(game_id)
            else:
                failed_games += 1
            
            # Progress update every 50 games
            if (i + 1) % 50 == 0:
                print(f"[Chunk {chunk_idx}] Progress: {i + 1}/{len(games)} games scraped")
                
        except Exception as e:
            print(f"[Chunk {chunk_idx}] Error processing game {game_id}: {e}")
            failed_games += 1
    
    # Batch upsert all player stats
    if all_player_stats:
        print(f"[Chunk {chunk_idx}] Upserting {len(all_player_stats)} player stats...")
        
        def batch_upsert(db):
            operations = [
                UpdateOne(
                    {'game_id': ps['game_id'], 'player_id': ps['player_id']},
                    {'$set': ps},
                    upsert=True
                )
                for ps in all_player_stats
            ]
            
            # Execute in sub-batches to avoid memory issues
            batch_size = 1000
            for i in range(0, len(operations), batch_size):
                batch = operations[i:i + batch_size]
                db.stats_nba_players.bulk_write(batch, ordered=False)
            
            return len(operations)
        
        try:
            pool.execute_with_retry(batch_upsert)
        except Exception as e:
            print(f"[Chunk {chunk_idx}] Error in batch upsert: {e}")
    
    # Mark games as migrated in stats_nba collection
    if processed_game_ids:
        print(f"[Chunk {chunk_idx}] Marking {len(processed_game_ids)} games as migrated...")
        
        def mark_migrated(db):
            db.stats_nba.update_many(
                {'game_id': {'$in': processed_game_ids}},
                {'$set': {'player_stats_migrated': True}}
            )
        
        try:
            pool.execute_with_retry(mark_migrated)
        except Exception as e:
            print(f"[Chunk {chunk_idx}] Error marking games as migrated: {e}")
    
    print(f"[Chunk {chunk_idx}] Complete - {len(all_player_stats)} players from {len(processed_game_ids)} games ({failed_games} failed)")
    
    return len(all_player_stats), len(processed_game_ids), processed_game_ids


def run_async_mode(games: List[dict], max_workers: int = MAX_WORKERS, chunk_size: int = CHUNK_SIZE):
    """
    Run the scraper in async mode with chunked threading.
    
    Args:
        games: List of all games to process
        max_workers: Maximum number of parallel threads
        chunk_size: Number of games per chunk
    """
    print(f"\n{'='*60}")
    print(f"ASYNC MODE - Processing {len(games)} games")
    print(f"Chunk size: {chunk_size}, Workers: {max_workers}")
    print(f"{'='*60}\n")
    
    # Create chunks
    chunks = [games[i:i + chunk_size] for i in range(0, len(games), chunk_size)]
    print(f"Created {len(chunks)} chunks")
    
    # Initialize shared connection pool
    print("Initializing MongoDB connection pool...")
    pool = MongoConnectionPool()
    
    total_players = 0
    total_games = 0
    all_game_ids = []
    
    start_time = time.time()
    
    # Process chunks in parallel using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix='Chunk') as executor:
        # Submit all chunks
        futures = {
            executor.submit(process_chunk, idx, chunk, pool): idx 
            for idx, chunk in enumerate(chunks)
        }
        
        # Collect results as they complete
        for future in as_completed(futures):
            chunk_idx = futures[future]
            try:
                players, games_done, game_ids = future.result()
                total_players += players
                total_games += games_done
                all_game_ids.extend(game_ids)
            except Exception as e:
                print(f"[Chunk {chunk_idx}] Failed with exception: {e}")
    
    elapsed = time.time() - start_time
    
    print(f"\n{'='*60}")
    print(f"ASYNC MODE COMPLETE")
    print(f"{'='*60}")
    print(f"Total time: {elapsed:.1f} seconds ({elapsed/60:.1f} minutes)")
    print(f"Total players scraped: {total_players}")
    print(f"Total games processed: {total_games}")
    print(f"Average: {total_players/elapsed:.1f} players/sec, {total_games/elapsed:.1f} games/sec")
    print(f"{'='*60}\n")
    
    # Close connection pool
    pool.close()


def main():
    parser = argparse.ArgumentParser(
        description='ESPN NBA Player Stats Scraper',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python espn_nba_players.py                     # Scrape player stats for all games
  python espn_nba_players.py --date 2025-03-13   # Scrape for games on a specific date
  python espn_nba_players.py --game-id 401809801 # Scrape for a specific game
  python espn_nba_players.py --limit 100         # Scrape only 100 games
  python espn_nba_players.py --async             # Async mode with chunked threading
  python espn_nba_players.py --async --workers 8 # Async with 8 parallel workers
        """
    )
    
    parser.add_argument(
        '--date', '-d',
        type=str,
        help='Scrape player stats for games on this date (YYYY-MM-DD)'
    )
    
    parser.add_argument(
        '--game-id', '-g',
        type=str,
        help='Scrape player stats for a specific game ID'
    )
    
    parser.add_argument(
        '--limit', '-l',
        type=int,
        default=0,
        help='Limit number of games to process (0 = no limit)'
    )
    
    parser.add_argument(
        '--no-update',
        action='store_true',
        help='Do not update database (dry run)'
    )
    
    parser.add_argument(
        '--missing-only',
        action='store_true',
        help='Only scrape games that have no player stats yet'
    )
    
    parser.add_argument(
        '--async',
        dest='async_mode',
        action='store_true',
        help='Run in async mode with chunked threading (batches of 500)'
    )
    
    parser.add_argument(
        '--workers', '-w',
        type=int,
        default=MAX_WORKERS,
        help=f'Number of parallel workers for async mode (default: {MAX_WORKERS})'
    )
    
    parser.add_argument(
        '--chunk-size',
        type=int,
        default=CHUNK_SIZE,
        help=f'Number of games per chunk in async mode (default: {CHUNK_SIZE})'
    )
    
    args = parser.parse_args()
    
    update = not args.no_update
    
    # Build query - exclude already migrated games by default in async mode
    query = {'espn_link': {'$exists': True}}
    
    # In async mode, exclude games that have already been migrated
    if args.async_mode:
        query['$or'] = [
            {'player_stats_migrated': {'$exists': False}},
            {'player_stats_migrated': False}
        ]
    
    if args.date:
        try:
            target_date = datetime.strptime(args.date, '%Y-%m-%d')
            query['date'] = args.date
        except ValueError:
            print("Error: Invalid date format. Use YYYY-MM-DD")
            return
    
    if args.game_id:
        # Override the $or for specific game_id lookup
        if '$or' in query:
            del query['$or']
        query['$or'] = [
            {'game_id': args.game_id},
            {'espn_link': {'$regex': args.game_id}}
        ]
    
    # Get games to process
    games = list(db.stats_nba.find(query).sort('date', -1))
    
    if args.limit > 0:
        games = games[:args.limit]
    
    print(f"Found {len(games)} games to process")
    
    if args.missing_only and not args.async_mode:
        # Filter to games without player stats (async mode uses player_stats_migrated flag instead)
        games_with_stats = set(db.stats_nba_players.distinct('game_id'))
        games = [g for g in games if g.get('game_id') not in games_with_stats]
        print(f"After filtering for missing: {len(games)} games")
    
    if not games:
        print("No games to process.")
        return
    
    # Run in async mode or sequential mode
    if args.async_mode:
        if args.no_update:
            print("Warning: --no-update is ignored in async mode (batch upserts are required)")
        
        run_async_mode(games, max_workers=args.workers, chunk_size=args.chunk_size)
    else:
        # Sequential mode
        total_players = 0
        
        for i, game in enumerate(games):
            game_id = game.get('game_id') or parse_game_id(game.get('espn_link', ''))
            date_str = game.get('date', 'Unknown')
            home_team = game.get('homeTeam', {}).get('name', 'Unknown')
            away_team = game.get('awayTeam', {}).get('name', 'Unknown')
            
            print(f"[{i+1}/{len(games)}] {date_str}: {away_team} @ {home_team} (game_id: {game_id})")
            
            try:
                players = scrape_player_stats(game, update=update)
                total_players += players
                print(f"  Scraped {players} player stats")
                
                # Mark as migrated in sequential mode too
                if update and players > 0:
                    db.stats_nba.update_one(
                        {'game_id': game_id},
                        {'$set': {'player_stats_migrated': True}}
                    )
            except Exception as e:
                print(f"  Error: {e}")
        
        print(f"\nTotal player stats scraped: {total_players}")


if __name__ == '__main__':
    main()

