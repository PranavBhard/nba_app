"""
Master Training Data Module

Manages a master training CSV file containing ALL possible features.
This allows fast feature extraction for training without recalculating features.
"""

import os
import csv
import pandas as pd
from datetime import datetime, date
from typing import Optional, Dict, List, Tuple
from nba_app.cli.Mongo import Mongo
from nba_app.cli.NBAModel import NBAModel, get_default_classifier_features
from nba_app.cli.feature_sets import get_all_features
from nba_app.cli.feature_name_parser import parse_feature_name, FeatureNameComponents


# Get project root (assuming this file is in nba_app/cli/)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Consolidated: place master training in parent ../master_training/
_PARENT_ROOT = os.path.dirname(_PROJECT_ROOT)
MASTER_TRAINING_PATH = os.path.join(_PARENT_ROOT, 'master_training', 'MASTER_TRAINING.csv')
MASTER_COLLECTION = 'master_training_data_nba'

def _expand_feature_versions(feature_name: str) -> List[str]:
    """
    Expand a feature to include all three versions (diff, home, away) if applicable.
    
    For features that have diff/home/away versions, generate all three.
    For all other features, return as-is.
    
    Args:
        feature_name: Feature name in new format
        
    Returns:
        List of feature names (original + expanded versions)
    """
    # Parse the feature name
    components = parse_feature_name(feature_name)
    
    # If we can't parse it, return as-is
    if not components:
        return [feature_name]
    
    # Build base parts (stat_name, time_period, calc_weight)
    base_parts = [components.stat_name, components.time_period, components.calc_weight]
    side_suffix = '|side' if components.is_side else ''
    
    # Generate all three versions
    expanded = []
    for version in ['diff', 'home', 'away']:
        expanded_feature = '|'.join(base_parts + [version]) + side_suffix
        expanded.append(expanded_feature)
    
    return expanded


def get_all_possible_features(no_player: bool = False) -> List[str]:
    """
    Get all possible features that should be included in the master training CSV.
    This includes all three versions (diff, home, away) for features that support them.
    
    Args:
        no_player: If True, exclude player-level features (PER, injuries)
    
    Returns:
        List of all feature names (from feature sets + enhanced features)
        with diff, home, and away versions expanded
    """
    # Get all features from feature sets
    all_features = get_all_features(model_type=None)  # No filtering - get everything
    
    # Filter out player-level feature sets if no_player is True
    if no_player:
        from nba_app.cli.feature_sets import FEATURE_SETS
        # Remove player_talent and injuries feature sets
        player_feature_sets = ['player_talent', 'injuries']
        for feature_set_name in player_feature_sets:
            if feature_set_name in FEATURE_SETS:
                # Remove features from this set
                player_set_features = FEATURE_SETS[feature_set_name]
                all_features = [f for f in all_features if f not in player_set_features]
    
    # Add enhanced features that are generated in NBAModel but not in feature_sets
    enhanced_features = [
        # Blend features
        'points_net_blend|none|blend:season:0.80/games_20:0.10/games_12:0.10|diff',
        'points_net_blend|none|blend:season:0.80/games_20:0.10/games_12:0.10|home',
        'points_net_blend|none|blend:season:0.80/games_20:0.10/games_12:0.10|away',
        'points_net_blend|none|blend:season:0.70/games_20:0.20/games_12:0.10|diff',
        'points_net_blend|none|blend:season:0.70/games_20:0.20/games_12:0.10|home',
        'points_net_blend|none|blend:season:0.70/games_20:0.20/games_12:0.10|away',
        'points_net_blend|none|blend:season:0.60/games_20:0.20/games_12:0.20|diff',
        'points_net_blend|none|blend:season:0.60/games_20:0.20/games_12:0.20|home',
        'points_net_blend|none|blend:season:0.60/games_20:0.20/games_12:0.20|away',
        'points_net_blend|none|blend:season:0.80/games_12:0.20|diff',
        'points_net_blend|none|blend:season:0.80/games_12:0.20|home',
        'points_net_blend|none|blend:season:0.80/games_12:0.20|away',
        'off_rtg_net_blend|none|blend:season:0.80/games_20:0.10/games_12:0.10|diff',
        'off_rtg_net_blend|none|blend:season:0.80/games_20:0.10/games_12:0.10|home',
        'off_rtg_net_blend|none|blend:season:0.80/games_20:0.10/games_12:0.10|away',
        'off_rtg_net_blend|none|blend:season:0.70/games_20:0.20/games_12:0.10|diff',
        'off_rtg_net_blend|none|blend:season:0.70/games_20:0.20/games_12:0.10|home',
        'off_rtg_net_blend|none|blend:season:0.70/games_20:0.20/games_12:0.10|away',
        'off_rtg_net_blend|none|blend:season:0.60/games_20:0.20/games_12:0.20|diff',
        'off_rtg_net_blend|none|blend:season:0.60/games_20:0.20/games_12:0.20|home',
        'off_rtg_net_blend|none|blend:season:0.60/games_20:0.20/games_12:0.20|away',
        'off_rtg_net_blend|none|blend:season:0.80/games_12:0.20|diff',
        'off_rtg_net_blend|none|blend:season:0.80/games_12:0.20|home',
        'off_rtg_net_blend|none|blend:season:0.80/games_12:0.20|away',
        'efg_net_blend|none|blend:season:0.80/games_20:0.10/games_12:0.10|diff',
        'efg_net_blend|none|blend:season:0.80/games_20:0.10/games_12:0.10|home',
        'efg_net_blend|none|blend:season:0.80/games_20:0.10/games_12:0.10|away',
        'efg_net_blend|none|blend:season:0.70/games_20:0.20/games_12:0.10|diff',
        'efg_net_blend|none|blend:season:0.70/games_20:0.20/games_12:0.10|home',
        'efg_net_blend|none|blend:season:0.70/games_20:0.20/games_12:0.10|away',
        'efg_net_blend|none|blend:season:0.60/games_20:0.20/games_12:0.20|diff',
        'efg_net_blend|none|blend:season:0.60/games_20:0.20/games_12:0.20|home',
        'efg_net_blend|none|blend:season:0.60/games_20:0.20/games_12:0.20|away',
        'efg_net_blend|none|blend:season:0.80/games_12:0.20|diff',
        'efg_net_blend|none|blend:season:0.80/games_12:0.20|home',
        'efg_net_blend|none|blend:season:0.80/games_12:0.20|away',
        'wins_blend|none|blend:season:0.80/games_20:0.10/games_12:0.10|diff',
        'wins_blend|none|blend:season:0.80/games_20:0.10/games_12:0.10|home',
        'wins_blend|none|blend:season:0.80/games_20:0.10/games_12:0.10|away',
        'wins_blend|none|blend:season:0.70/games_20:0.20/games_12:0.10|diff',
        'wins_blend|none|blend:season:0.70/games_20:0.20/games_12:0.10|home',
        'wins_blend|none|blend:season:0.70/games_20:0.20/games_12:0.10|away',
        'wins_blend|none|blend:season:0.60/games_20:0.20/games_12:0.20|diff',
        'wins_blend|none|blend:season:0.60/games_20:0.20/games_12:0.20|home',
        'wins_blend|none|blend:season:0.60/games_20:0.20/games_12:0.20|away',
        'wins_blend|none|blend:season:0.80/games_12:0.20|diff',
        'wins_blend|none|blend:season:0.80/games_12:0.20|home',
        'wins_blend|none|blend:season:0.80/games_12:0.20|away',
        
        # Limited time period features
        'to_metric|season|avg|diff',
        'to_metric|days_12|raw|diff',
        'to_metric|days_12|avg|diff',
        'ast_to_ratio|season|raw|diff',
        'ast_to_ratio|season|avg|diff',
        'ast_to_ratio|days_12|raw|diff',
        'ast_to_ratio|days_12|avg|diff',
        
        # Travel features (enhanced features not in feature_sets)
        'travel|days_2|avg|diff',
        'travel|days_2|avg|home',
        'travel|days_2|avg|away',
        'travel|days_5|avg|diff',
        'travel|days_5|avg|home',
        'travel|days_5|avg|away',
        'travel|days_12|avg|diff',
        'travel|days_12|avg|home',
        'travel|days_12|avg|away',
    ]
    
    # Add player-level features if not excluded
    if not no_player:
        player_features = [
            'player_team_per|season|weighted_MPG|diff',
            'player_team_per|season|weighted_MPG|home',
            'player_team_per|season|weighted_MPG|away',
            'player_starters_per|season|avg|diff',
            'player_starters_per|season|avg|home',
            'player_starters_per|season|avg|away',
            'player_per_1|none|weighted_MIN_REC|diff',
            'player_per_1|none|weighted_MIN_REC|home',
            'player_per_1|none|weighted_MIN_REC|away',
            'player_per_1|season|raw|diff',
            'player_per_1|season|raw|home',
            'player_per_1|season|raw|away',
            'player_per_2|season|raw|diff',
            'player_per_2|season|raw|home',
            'player_per_2|season|raw|away',
            'player_per_3|season|raw|diff',
            'player_per_3|season|raw|home',
            'player_per_3|season|raw|away',
            # New format: player_per|season|topN_avg (average PER of top N players)
            'player_per|season|top1_avg|diff',
            'player_per|season|top1_avg|home',
            'player_per|season|top1_avg|away',
            'player_per|season|top2_avg|diff',
            'player_per|season|top2_avg|home',
            'player_per|season|top2_avg|away',
            'player_per|season|top3_avg|diff',
            'player_per|season|top3_avg|home',
            'player_per|season|top3_avg|away',
            # MPG-weighted versions
            'player_per|season|top1_weighted_MPG|diff',
            'player_per|season|top1_weighted_MPG|home',
            'player_per|season|top1_weighted_MPG|away',
            'player_per|season|top2_weighted_MPG|diff',
            'player_per|season|top2_weighted_MPG|home',
            'player_per|season|top2_weighted_MPG|away',
            'player_per|season|top3_weighted_MPG|diff',
            'player_per|season|top3_weighted_MPG|home',
            'player_per|season|top3_weighted_MPG|away',
            # Injury features
            'inj_severity|none|raw|diff',
            'inj_severity|none|raw|home',
            'inj_severity|none|raw|away',
            'inj_per|none|top1_avg|diff',
            'inj_per|none|top1_avg|home',
            'inj_per|none|top1_avg|away',
            'inj_rotation_per|none|raw|diff',
            'inj_rotation_per|none|raw|home',
            'inj_rotation_per|none|raw|away',
            'inj_per|none|weighted_MIN|diff',
            'inj_per|none|weighted_MIN|home',
            'inj_per|none|weighted_MIN|away',
            'inj_per|none|top3_sum|diff',
            'inj_per|none|top3_sum|home',
            'inj_per|none|top3_sum|away',
            'inj_min_lost|none|raw|diff',
            'inj_min_lost|none|raw|home',
            'inj_min_lost|none|raw|away',
            'inj_impact|none|blend:severity:0.45/top1_per:0.35/rotation:0.20|diff',
            'inj_impact|none|blend:severity:0.45/top1_per:0.35/rotation:0.20|home',
            'inj_impact|none|blend:severity:0.45/top1_per:0.35/rotation:0.20|away',
        ]
        enhanced_features.extend(player_features)
    
    # Combine all features
    all_features.extend(enhanced_features)
    
    # Expand features to include diff, home, and away versions
    expanded_features = set()
    for feature in all_features:
        # Skip any features that don't have the | separator (shouldn't happen, but safety check)
        if '|' not in feature:
            continue
        
        # Filter out features that would result in all zeros:
        # Features with time_period='none' and calc_weight in ['raw', 'rel', 'std']
        components = parse_feature_name(feature)
        if components:
            # Features that can use 'none' time period: elo, rest, b2b, player_per_1
            stats_allowing_none = ['elo', 'rest', 'b2b', 'player_per_1']
            if components.time_period == 'none' and components.calc_weight in ['raw', 'rel', 'std']:
                if components.stat_name not in stats_allowing_none:
                    # Skip this feature - it would result in all zeros
                    continue
        
        expanded = _expand_feature_versions(feature)
        expanded_features.update(expanded)
    
    return sorted(list(expanded_features))


def get_master_training_metadata(db) -> Optional[Dict]:
    """
    Get the current master training data metadata from MongoDB.
    
    Args:
        db: MongoDB database connection
        
    Returns:
        Metadata dict or None if no master exists
    """
    master_doc = db[MASTER_COLLECTION].find_one({'is_master': True})
    return master_doc


def create_or_update_master_metadata(
    db,
    file_path: str,
    feature_list: List[str],
    feature_count: int,
    last_date_updated: str,
    options: Dict = None
) -> str:
    """
    Create or update master training data metadata in MongoDB.
    
    Args:
        db: MongoDB database connection
        file_path: Path to master training CSV file
        feature_list: List of feature names included
        feature_count: Number of features
        last_date_updated: Last date the master was updated (YYYY-MM-DD)
        options: Optional dict with configuration options
        
    Returns:
        MongoDB document ID
    """
    """
    Create or update master training data metadata in MongoDB.
    
    Args:
        db: MongoDB database connection
        file_path: Path to master training CSV file
        feature_list: List of feature names included
        feature_count: Number of features
        last_date_updated: Last date the master was updated (YYYY-MM-DD)
        options: Optional dict with configuration options
        
    Returns:
        MongoDB document ID
    """
    metadata = {
        'is_master': True,
        'file_path': file_path,
        'feature_list': feature_list,
        'feature_count': feature_count,
        'last_date_updated': last_date_updated,
        'options': options or {},
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    
    # Update existing master or create new one
    result = db[MASTER_COLLECTION].update_one(
        {'is_master': True},
        {'$set': metadata},
        upsert=True
    )
    
    return result.upserted_id if result.upserted_id else db[MASTER_COLLECTION].find_one({'is_master': True})['_id']


def generate_master_training_data(
    query: Dict = None,
    output_path: str = None,
    progress_callback: callable = None,
    limit: int = None,
    games_list: List[int] = None,
    months_list: List[int] = None,
    days_list: List[int] = None,
    season: str = None,
    min_season: str = None,
    skip_months: int = 0,
    no_player: bool = False
) -> Tuple[str, List[str], int]:
    """
    Generate master training CSV with ALL possible features.
    
    Args:
        query: MongoDB query filter (uses DEFAULT_QUERY if None)
        output_path: Output path for master CSV (defaults to MASTER_TRAINING_PATH)
        progress_callback: Optional callback function(current, total, progress_pct)
        limit: Optional limit on number of games to process (for testing/debugging).
               When specified with default output_path, will add "_limit-N" suffix to filename.
        games_list: List of game window sizes (e.g., [5, 10, 15]). Defaults to [10] if None.
        months_list: List of month window sizes (e.g., [1, 2, 3]). Defaults to [1] if None.
        days_list: List of day window sizes (e.g., [7, 14, 30]). Defaults to [10] if None.
        season: Optional season filter (e.g., "2023-2024"). Must be in YYYY-YYYY format.
        min_season: Optional minimum season filter (e.g., "2008-2009"). Only includes games from this season or later.
                   Must be in YYYY-YYYY format. Cannot be used with season parameter.
        skip_months: Number of months to skip from the start of the season. Defaults to 0.
        no_player: If True, skip player-level features (PER, injuries) for faster generation.
        
    Returns:
        Tuple of (csv_path, feature_list, game_count)
    """
    # If limit is specified and using default path, modify output path to include "_limit-N" suffix
    if limit is not None and limit > 0:
        if output_path is None or output_path == MASTER_TRAINING_PATH:
            # Modify the default path
            base_name = os.path.splitext(MASTER_TRAINING_PATH)[0]  # Remove .csv extension
            output_path = f"{base_name}_limit-{limit}.csv"
        elif output_path and not output_path.endswith(f"_limit-{limit}.csv"):
            # Modify the provided path if it doesn't already have the limit suffix
            base_name = os.path.splitext(output_path)[0]  # Remove .csv extension
            output_path = f"{base_name}_limit-{limit}.csv"
    else:
        output_path = output_path or MASTER_TRAINING_PATH
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Build query with season filter if provided
    from nba_app.cli.NBAModel import NBAModel
    if query is None:
        query = NBAModel.DEFAULT_QUERY.copy()
    
    if season:
        # Override season filter in query (exact match)
        query['season'] = season
    elif min_season:
        # Add minimum season filter (greater than or equal)
        query['season'] = {'$gte': min_season}
    
    # Get all possible features (exclude player features if no_player is True)
    # This includes all three versions (diff, home, away) for features that support them
    all_features = get_all_possible_features(no_player=no_player)
    
    # Create NBAModel with features enabled based on no_player flag
    # Use get_default_classifier_features() with custom time periods as base stat tokens
    # The model will compute all features including enhanced, PER, Elo, etc.
    model = NBAModel(
        classifier_features=get_default_classifier_features(
            games_list=games_list,
            months_list=months_list,
            days_list=days_list
        ),
        points_features=None,  # Master is for classifier only
        include_elo=True,  # Include Elo
        use_exponential_weighting=False,
        # Enhanced features always included (team-level only)
        include_era_normalization=True,  # Include era normalization
        include_per_features=not no_player,  # Skip PER if no_player is True
        include_injuries=not no_player,  # Skip injuries if no_player is True
        recency_decay_k=15.0,  # Default recency decay constant
        output_dir=os.path.dirname(output_path),
        preload_data=True,  # Always preload game data (player data preloading is conditional)
        master_training_mode=not no_player  # Use master training mode to only include the 5 specified player features
    )
    
    # CRITICAL: Set feature_names to the expanded list (includes home/away/diff versions)
    # This ensures _build_feature_headers() uses all expanded features, not just diff versions
    model.feature_names = all_features
    
    # Helper function to filter games by skip_months
    def filter_skip_months(games_list: list, skip_months: int) -> list:
        """Filter games to skip the first N months of each season."""
        if skip_months <= 0:
            return games_list
        
        # Group games by season
        games_by_season = {}
        for game in games_list:
            season = game.get('season')
            if season:
                if season not in games_by_season:
                    games_by_season[season] = []
                games_by_season[season].append(game)
        
        # Filter each season's games
        filtered_games = []
        for season, season_games in games_by_season.items():
            # Sort by date
            season_games.sort(key=lambda g: (
                g.get('year', 0),
                g.get('month', 0),
                g.get('day', 0)
            ))
            
            # Find the first game after skip_months
            # We need to skip games in the first N months of the season
            # NBA season typically starts in October (month 10)
            # But we'll use the actual month from the games
            if season_games:
                # Get the earliest month in the season
                earliest_month = min(g.get('month', 1) for g in season_games if g.get('month'))
                # Calculate the cutoff month
                cutoff_month = earliest_month + skip_months - 1
                
                # Filter games after the cutoff month
                for game in season_games:
                    game_month = game.get('month', 0)
                    if game_month > cutoff_month:
                        filtered_games.append(game)
        
        return filtered_games
    
    # If limit is specified, fetch games first and create a query that matches only those games
    if limit is not None and limit > 0:
        from nba_app.cli.Mongo import Mongo
        mongo = Mongo()
        db = mongo.db
        
        # Fetch games with limit
        limited_games = list(db.stats_nba.find(query).limit(limit))
        
        # Apply skip_months filter if specified
        if skip_months > 0:
            limited_games = filter_skip_months(limited_games, skip_months)
            print(f"After skipping first {skip_months} months: {len(limited_games)} games remaining")
        
        if not limited_games:
            print(f"Warning: No games found matching query (limit: {limit})")
            return output_path, [], 0
        
        # Find the latest date in the limited games for Elo calculation
        # Elo needs to be computed for ALL games up to this date, not just the limited set
        dates = [g.get('date') for g in limited_games if g.get('date')]
        if dates:
            latest_date = max(dates)
            print(f"Limited to {limit} games, latest date: {latest_date}")
            print(f"Computing Elo for all games up to {latest_date} (for accurate Elo ratings)...")
            
            # Create query for Elo calculation: all games up to the latest date
            elo_query = query.copy()
            elo_query['date'] = {'$lte': latest_date}
            
            # Fetch all games up to latest date for Elo calculation
            elo_games = list(db.stats_nba.find(elo_query).sort('date', 1))
            print(f"  Fetched {len(elo_games)} games for Elo calculation")
            
            # Pre-compute Elo ratings using all games up to latest date
            if model.include_elo:
                model._compute_elo_ratings(elo_games)
                print(f"  Elo ratings computed for {len(model.elo_history)} game-team combinations")
        else:
            # No dates found, fall back to original behavior
            elo_games = limited_games
        
        # Create a query that matches only the limited game IDs (for training data generation)
        game_ids = [g.get('game_id') for g in limited_games if g.get('game_id')]
        if game_ids:
            limited_query = {'game_id': {'$in': game_ids}}
        else:
            # Fallback: use dates from fetched games
            dates = sorted(set(g.get('date') for g in limited_games if g.get('date')))
            if dates:
                limited_query = {'date': {'$in': dates}}
            else:
                limited_query = query
        
        # Create training data with limited query (Elo already computed above)
        # Note: min_games_filter=0 for master training to include ALL games
        game_count, clf_csv, _ = model.create_training_data(
            query=limited_query,
            classifier_csv=output_path,
            min_games_filter=0,  # Master training includes all games
            progress_callback=progress_callback
        )
    else:
        # Create training data with all features (no limit)
        # Note: min_games_filter=0 for master training to include ALL games
        
        # If skip_months is specified, we need to fetch games, filter them, and create a custom query
        if skip_months > 0:
            from nba_app.cli.Mongo import Mongo
            mongo = Mongo()
            db = mongo.db
            
            # Fetch all games matching the query
            all_games = list(db.stats_nba.find(query))
            print(f"Fetched {len(all_games)} games from database")
            
            # Apply skip_months filter
            filtered_games = filter_skip_months(all_games, skip_months)
            print(f"After skipping first {skip_months} months: {len(filtered_games)} games remaining")
            
            if not filtered_games:
                print("Warning: No games remaining after skip_months filter")
                return output_path, [], 0
            
            # Create a query that matches only the filtered game IDs
            game_ids = [g.get('game_id') for g in filtered_games if g.get('game_id')]
            if game_ids:
                filtered_query = {'game_id': {'$in': game_ids}}
            else:
                # Fallback: use dates from filtered games
                dates = sorted(set(g.get('date') for g in filtered_games if g.get('date')))
                if dates:
                    filtered_query = {'date': {'$in': dates}}
                else:
                    filtered_query = query
            
            game_count, clf_csv, _ = model.create_training_data(
                query=filtered_query,
                classifier_csv=output_path,
                min_games_filter=0,  # Master training includes all games
                progress_callback=progress_callback
            )
        else:
            # No skip_months, use query directly
            game_count, clf_csv, _ = model.create_training_data(
                query=query,
                classifier_csv=output_path,
                min_games_filter=0,  # Master training includes all games
                progress_callback=progress_callback
            )
    
    # Read the generated CSV to get actual feature list
    # Use error handling to skip bad lines (e.g., lines with extra commas)
    try:
        df = pd.read_csv(clf_csv, on_bad_lines='skip', engine='python')
    except TypeError:
        # Older pandas versions use error_bad_lines instead
        try:
            df = pd.read_csv(clf_csv, error_bad_lines=False, warn_bad_lines=True, engine='python')
        except TypeError:
            # Fallback: read with quoting to handle embedded commas
            df = pd.read_csv(clf_csv, quoting=1)  # QUOTE_ALL
    
    meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away', 'HomeWon']
    actual_features = [col for col in df.columns if col not in meta_cols]
    
    # Warn if we had to skip lines
    if len(df) < game_count:
        skipped = game_count - len(df)
        print(f"  Warning: Skipped {skipped} malformed rows when reading CSV (file has {len(df)} valid rows)")
    
    return clf_csv, actual_features, len(df)


def update_master_training_data_incremental(
    db,
    start_date: str,
    end_date: str,
    master_path: str = None,
    progress_callback: callable = None
) -> Tuple[int, str]:
    """
    Incrementally update master training data with new games between start_date and end_date.
    
    Args:
        db: MongoDB database connection
        start_date: Start date for new games (YYYY-MM-DD, exclusive - games after this date)
        end_date: End date for new games (YYYY-MM-DD, inclusive)
        master_path: Path to master CSV file (defaults to MASTER_TRAINING_PATH)
        progress_callback: Optional callback function(current, total, progress_pct)
        
    Returns:
        Tuple of (games_added_count, updated_master_path)
    """
    master_path = master_path or MASTER_TRAINING_PATH
    
    # Get master metadata
    master_meta = get_master_training_metadata(db)
    if not master_meta:
        raise ValueError("Master training data does not exist. Generate it first using generate_master_training_data()")
    
    # Query for games between start_date and end_date (both inclusive)
    # If start_date == end_date, query for that exact date
    # Otherwise, query for dates > start_date and <= end_date
    if start_date == end_date:
        date_query = {'$eq': start_date}
    else:
        date_query = {
            '$gt': start_date,
            '$lte': end_date
        }
    
    query = {
        'date': date_query,
        'homeTeam.points': {'$gt': 0},
        'awayTeam.points': {'$gt': 0},
        'game_type': {'$nin': ['preseason', 'allstar']}
    }
    
    # Get all possible features (same as master)
    all_features = get_all_possible_features()
    
    # Get master metadata to extract time period parameters if stored
    master_meta = get_master_training_metadata(db)
    options = master_meta.get('options', {}) if master_meta else {}
    games_list = options.get('games_list', [10])
    months_list = options.get('months_list', [1])
    days_list = options.get('days_list', [10])
    
    # Create NBAModel with same configuration as master
    # Check if no_player was set in options
    no_player = options.get('no_player', False)
    model = NBAModel(
        classifier_features=get_default_classifier_features(
            games_list=games_list,
            months_list=months_list,
            days_list=days_list
        ),
        points_features=None,
        include_elo=True,
        use_exponential_weighting=False,
        # Enhanced features always included (team-level only)
        include_era_normalization=True,
        include_per_features=not no_player,  # Skip PER if no_player is True
        include_injuries=not no_player,  # Skip injuries if no_player is True
        recency_decay_k=15.0,  # Default recency decay constant
        output_dir=os.path.dirname(master_path),
        master_training_mode=not no_player  # Use master training mode to only include the 5 specified player features
    )
    
    # Generate training data for new games only
    temp_csv = master_path.replace('.csv', '_temp_incremental.csv')
    game_count, clf_csv, _ = model.create_training_data(
        query=query,
        classifier_csv=temp_csv,
        progress_callback=progress_callback
    )
    
    if game_count == 0:
        # No new games, return existing master
        if os.path.exists(temp_csv):
            os.remove(temp_csv)
        return 0, master_path
    
    # Read existing master CSV
    master_df = pd.read_csv(master_path)
    
    # Read new games CSV
    new_df = pd.read_csv(clf_csv)
    
    # Ensure column alignment (new games might have different columns if features changed)
    # Use master's columns as authority
    master_cols = list(master_df.columns)
    new_cols = list(new_df.columns)
    
    # Add missing columns to new_df (fill with 0 or appropriate default)
    for col in master_cols:
        if col not in new_cols:
            new_df[col] = 0
    
    # Reorder new_df columns to match master
    new_df = new_df[master_cols]
    
    # Append new games to master
    combined_df = pd.concat([master_df, new_df], ignore_index=True)
    
    # Remove duplicates (in case of re-runs)
    # Use Year, Month, Day, Home, Away as unique key
    combined_df = combined_df.drop_duplicates(
        subset=['Year', 'Month', 'Day', 'Home', 'Away'],
        keep='last'  # Keep the most recent entry
    )
    
    # Sort by date
    combined_df = combined_df.sort_values(['Year', 'Month', 'Day', 'Home', 'Away'])
    
    # Write updated master CSV
    combined_df.to_csv(master_path, index=False)
    
    # Clean up temp file
    if os.path.exists(temp_csv):
        os.remove(temp_csv)
    
    # Update metadata
    actual_features = [col for col in master_cols if col not in ['Year', 'Month', 'Day', 'Home', 'Away', 'HomeWon']]
    options = master_meta.get('options', {})
    options.update({
        'games_list': games_list,
        'months_list': months_list,
        'days_list': days_list
    })
    create_or_update_master_metadata(
        db,
        master_path,
        actual_features,
        len(actual_features),
        end_date,
        options
    )
    
    return game_count, master_path


def extract_features_from_master(
    master_path: str,
    requested_features: List[str] = None,
    output_path: str = None
) -> str:
    """
    Extract selected features from master training CSV.
    
    Args:
        master_path: Path to master training CSV
        requested_features: List of feature names to extract (None = extract all features)
        output_path: Output path for extracted CSV (defaults to temp file)
        
    Returns:
        Path to extracted CSV file
    """
    if not os.path.exists(master_path):
        raise FileNotFoundError(f"Master training CSV not found: {master_path}")
    
    # Read master CSV
    df = pd.read_csv(master_path)
    
    # Meta columns that should always be included (not features)
    meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away', 'HomeWon', 'game_id']
    
    if requested_features is None or len(requested_features) == 0:
        # Extract all features (just return master as-is or copy it)
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = master_path.replace('MASTER_TRAINING.csv', f'extracted_training_{timestamp}.csv')
        
        df.to_csv(output_path, index=False)
        return output_path
    
    # Check which requested features exist in master
    available_features = [f for f in requested_features if f in df.columns]
    missing_features = [f for f in requested_features if f not in df.columns]
    
    if missing_features:
        raise ValueError(
            f"Requested features not found in master CSV: {missing_features}. "
            f"Master needs to be regenerated to include all possible features."
        )
    
    # Extract columns: meta + requested features
    # IMPORTANT: Preserve the original CSV column order, not the requested_features order!
    # This ensures feature alignment matches training
    csv_feature_cols = [c for c in df.columns if c not in meta_cols]
    # Filter to only include requested features, but keep CSV order
    ordered_available_features = [f for f in csv_feature_cols if f in available_features]
    columns_to_extract = meta_cols + ordered_available_features
    extracted_df = df[columns_to_extract]
    
    # Write extracted CSV
    if output_path is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = master_path.replace('MASTER_TRAINING.csv', f'extracted_training_{timestamp}.csv')
    
    extracted_df.to_csv(output_path, index=False)
    
    return output_path


def extract_features_from_master_for_points(
    master_path: str,
    requested_features: List[str] = None,
    output_path: str = None,
    begin_year: int = None,
    min_games_played: int = 15
) -> str:
    """
    Extract selected features from master training CSV for points regression.
    Includes home_points and away_points as metadata columns (targets).
    
    Args:
        master_path: Path to master training CSV
        requested_features: List of feature names to extract (None = extract all features)
        output_path: Output path for extracted CSV (defaults to temp file)
        begin_year: Minimum season start year to include (e.g., 2012 means >= 2012-2013 season).
                   If provided, filters data using SeasonStartYear logic (Oct-Dec belong to that year's season,
                   Jan-Jun belong to previous year's season).
        min_games_played: Minimum games played filter (default 15). Filters out games where either team
                         hasn't played at least this many games in the same season before the target game.
                         Set to 0 or None to disable filtering.
        
    Returns:
        Path to extracted CSV file
    """
    if not os.path.exists(master_path):
        raise FileNotFoundError(f"Master training CSV not found: {master_path}")
    
    # Read master CSV
    df = pd.read_csv(master_path)
    
    # Filter by begin_year if provided (same logic as dataset_builder)
    if begin_year is not None:
        import numpy as np
        # Calculate SeasonStartYear: Oct-Dec belong to that calendar year's season,
        # Jan-Jun belong to the previous calendar year's season
        df = df.copy()
        df['SeasonStartYear'] = np.where(
            df['Month'].astype(int) >= 10,
            df['Year'].astype(int),
            df['Year'].astype(int) - 1
        )
        df = df[df['SeasonStartYear'] >= int(begin_year)]
        # Drop SeasonStartYear column after filtering (it's a helper column)
        df = df.drop('SeasonStartYear', axis=1)
    
    # Apply min_games_played filter if specified (same logic as dataset_builder)
    if min_games_played is not None and min_games_played > 0:
        import numpy as np
        before_mgp = len(df)
        df = df.copy()
        
        # Calculate Season column (e.g., "2018-2019" for games from Oct 2018 to Jun 2019)
        df['Season'] = np.where(df['Month'].astype(int) >= 10,
                                df['Year'].astype(int).astype(str) + '-' + (df['Year'].astype(int) + 1).astype(str),
                                (df['Year'].astype(int) - 1).astype(str) + '-' + df['Year'].astype(int).astype(str))
        
        # Build a sortable date key
        df['_date_key'] = (df['Year'].astype(int) * 10000) + (df['Month'].astype(int) * 100) + df['Day'].astype(int)
        
        # Home prior counts per season (group by Season, not Year)
        home_keys = ['Year', 'Month', 'Day', 'Home']
        home_seq = df[home_keys + ['Season', '_date_key']].copy()
        home_seq = home_seq.sort_values(['Season', 'Home', '_date_key'])
        home_seq['_homePrior'] = home_seq.groupby(['Season', 'Home']).cumcount()
        df = df.merge(
            home_seq[home_keys + ['_homePrior']],
            on=home_keys,
            how='left'
        )
        
        # Away prior counts per season (group by Season, not Year)
        away_keys = ['Year', 'Month', 'Day', 'Away']
        away_seq = df[away_keys + ['Season', '_date_key']].copy()
        away_seq = away_seq.sort_values(['Season', 'Away', '_date_key'])
        away_seq['_awayPrior'] = away_seq.groupby(['Season', 'Away']).cumcount()
        df = df.merge(
            away_seq[away_keys + ['_awayPrior']],
            on=away_keys,
            how='left'
        )
        
        # Apply filter: both teams must have played at least min_games_played prior same-season games
        df = df[(df['_homePrior'] >= min_games_played) & (df['_awayPrior'] >= min_games_played)].copy()
        
        # Drop helper columns
        df.drop(columns=[c for c in ['_date_key', '_homePrior', '_awayPrior', 'Season'] if c in df.columns], inplace=True)
        
        after_mgp = len(df)
        print(f"[extract_features_from_master_for_points] Applied min_games_played filter (>= {min_games_played}): {before_mgp} -> {after_mgp} games")
        
        if len(df) == 0:
            raise ValueError(
                f'No training data available after applying min_games_played >= {min_games_played}. '
                f'This filter requires both teams to have played at least {min_games_played} games '
                f'in the same season before the target game. Try reducing min_games_played or check your data.'
            )
    
    # Meta columns that should always be included for points regression
    # Base metadata columns
    base_meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away']
    meta_cols = base_meta_cols.copy()
    
    # Add optional metadata columns if they exist
    if 'game_id' in df.columns:
        meta_cols.append('game_id')
    if 'home_points' in df.columns:
        meta_cols.append('home_points')
    if 'away_points' in df.columns:
        meta_cols.append('away_points')
    
    # If home_points or away_points are missing, raise an error
    if 'home_points' not in df.columns or 'away_points' not in df.columns:
        raise ValueError(
            f"Master training CSV missing required columns for points regression: "
            f"home_points={'missing' if 'home_points' not in df.columns else 'ok'}, "
            f"away_points={'missing' if 'away_points' not in df.columns else 'ok'}. "
            f"Please regenerate the master CSV using: python cli/generate_master_training.py"
        )
    
    if requested_features is None or len(requested_features) == 0:
        # Extract all features (just return master as-is or copy it)
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = master_path.replace('MASTER_TRAINING.csv', f'extracted_points_training_{timestamp}.csv')
        
        # Filter out HomeWon (not needed for points regression)
        columns_to_extract = [col for col in df.columns if col not in ['HomeWon']]
        df[columns_to_extract].to_csv(output_path, index=False)
        return output_path
    
    # Check which requested features exist in master
    available_features = [f for f in requested_features if f in df.columns]
    missing_features = [f for f in requested_features if f not in df.columns]
    
    if missing_features:
        raise ValueError(
            f"Requested features not found in master CSV: {missing_features}. "
            f"Master needs to be regenerated to include all possible features."
        )
    
    # Extract columns: meta + requested features
    # IMPORTANT: Preserve the original CSV column order, not the requested_features order!
    # This ensures feature alignment matches training
    csv_feature_cols = [c for c in df.columns if c not in meta_cols and c != 'HomeWon']
    # Filter to only include requested features, but keep CSV order
    ordered_available_features = [f for f in csv_feature_cols if f in available_features]
    columns_to_extract = meta_cols + ordered_available_features
    extracted_df = df[columns_to_extract]
    
    # Write extracted CSV
    if output_path is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = master_path.replace('MASTER_TRAINING.csv', f'extracted_points_training_{timestamp}.csv')
    
    extracted_df.to_csv(output_path, index=False)
    
    return output_path


def check_master_needs_regeneration(
    db,
    requested_features: List[str]
) -> Tuple[bool, List[str]]:
    """
    Check if master training data needs to be regenerated based on requested features.
    
    Args:
        db: MongoDB database connection
        requested_features: List of requested feature names
        
    Returns:
        Tuple of (needs_regeneration: bool, missing_features: List[str])
    """
    # Prefer checking the actual CSV header for truth. Mongo metadata can be stale
    # (e.g., if columns were added later like pred_* via populate_master_training_cols).
    try:
        if os.path.exists(MASTER_TRAINING_PATH):
            header_df = pd.read_csv(MASTER_TRAINING_PATH, nrows=0)
            master_cols = set(header_df.columns)
            requested_set = set(requested_features or [])

            missing_features = list(requested_set - master_cols)
            if missing_features:
                return True, missing_features
            return False, []
    except Exception:
        # Fall back to metadata check below
        pass

    master_meta = get_master_training_metadata(db)

    if not master_meta:
        # No master exists - needs generation
        return True, requested_features

    master_features = set(master_meta.get('feature_list', []))
    requested_set = set(requested_features)

    missing_features = list(requested_set - master_features)

    if missing_features:
        return True, missing_features

    return False, []


def register_existing_master_csv(
    db,
    master_path: str = None,
    options: Dict = None
) -> Dict:
    """
    Register an existing master training CSV file in MongoDB.
    Reads the CSV to extract feature list and latest date.
    
    Args:
        db: MongoDB database connection
        master_path: Path to existing master CSV (defaults to MASTER_TRAINING_PATH)
        options: Optional dict with configuration options
        
    Returns:
        Metadata dict that was saved
    """
    master_path = master_path or MASTER_TRAINING_PATH
    
    if not os.path.exists(master_path):
        raise FileNotFoundError(f"Master training CSV not found: {master_path}")
    
    print(f"Reading existing master CSV: {master_path}")
    
    # Read CSV to get feature list and latest date
    # Handle potential CSV parsing errors (from old CSV format or malformed lines)
    try:
        df = pd.read_csv(master_path, on_bad_lines='skip', engine='python')
    except TypeError:
        # Older pandas versions use error_bad_lines instead
        try:
            df = pd.read_csv(master_path, error_bad_lines=False, warn_bad_lines=True, engine='python')
        except:
            # Last resort: use csv module directly
            import csv
            rows = []
            with open(master_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)
                for row in reader:
                    if len(row) == len(header):  # Only include complete rows
                        rows.append(row)
            df = pd.DataFrame(rows, columns=header)
            # Convert numeric columns
            for col in df.columns:
                if col not in ['Home', 'Away']:
                    try:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    except:
                        pass
    except Exception as e:
        # Fallback: try with error_bad_lines=False for older pandas
        try:
            df = pd.read_csv(master_path, error_bad_lines=False, warn_bad_lines=True, engine='python')
        except:
            # Last resort: use csv module directly
            import csv
            rows = []
            with open(master_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)
                for row in reader:
                    if len(row) == len(header):  # Only include complete rows
                        rows.append(row)
            df = pd.DataFrame(rows, columns=header)
            # Convert numeric columns
            for col in df.columns:
                if col not in ['Home', 'Away']:
                    try:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    except:
                        pass
    
    # Meta columns that are not features
    meta_cols = ['Year', 'Month', 'Day', 'Home', 'Away', 'HomeWon']
    
    # Extract feature list
    feature_list = [col for col in df.columns if col not in meta_cols]
    feature_count = len(feature_list)
    
    # Find latest date in CSV
    if len(df) > 0:
        # Get the latest game date
        df_sorted = df.sort_values(['Year', 'Month', 'Day'], ascending=False)
        latest_row = df_sorted.iloc[0]
        last_date_updated = f"{int(latest_row['Year'])}-{int(latest_row['Month']):02d}-{int(latest_row['Day']):02d}"
    else:
        # Empty CSV - use today's date as placeholder
        last_date_updated = datetime.now().strftime('%Y-%m-%d')
    
    print(f"Found {len(df)} games, {feature_count} features, latest date: {last_date_updated}")
    
    # Create/update metadata
    metadata_id = create_or_update_master_metadata(
        db,
        master_path,
        feature_list,
        feature_count,
        last_date_updated,
        options
    )
    
    print(f"Registered master training data in MongoDB (ID: {metadata_id})")
    print(f"  Features: {feature_count}")
    print(f"  Games: {len(df)}")
    print(f"  Last updated: {last_date_updated}")
    
    return {
        'file_path': master_path,
        'feature_list': feature_list,
        'feature_count': feature_count,
        'last_date_updated': last_date_updated,
        'options': options or {},
        'game_count': len(df)
    }


def update_master_after_data_pull(
    db,
    new_game_date: str,
    master_path: str = None
) -> Tuple[int, str]:
    """
    Update master training data after a daily data pull.
    Checks if master needs updating and updates incrementally if needed.
    
    Args:
        db: MongoDB database connection
        new_game_date: Date of newly pulled games (YYYY-MM-DD)
        master_path: Path to master CSV file (defaults to MASTER_TRAINING_PATH)
        
    Returns:
        Tuple of (games_added_count, updated_master_path)
    """
    master_path = master_path or MASTER_TRAINING_PATH
    
    # Get master metadata
    master_meta = get_master_training_metadata(db)
    
    if not master_meta:
        # No master exists - create it
        print("Master training data does not exist. Generating initial master...")
        master_path, features, game_count = generate_master_training_data()
        print(f"Generated master training data: {game_count} games, {len(features)} features")
        return game_count, master_path
    
    # Get last updated date
    last_date_updated = master_meta.get('last_date_updated')
    
    if not last_date_updated:
        # No last_date_updated - regenerate entire master
        print("Master training data missing last_date_updated. Regenerating...")
        master_path, features, game_count = generate_master_training_data()
        return game_count, master_path
    
    # Check if new_game_date is after last_date_updated
    if new_game_date < last_date_updated:
        # No new games to add
        print(f"Master training data is up to date (last updated: {last_date_updated}, new games: {new_game_date})")
        return 0, master_path
    
    # Calculate start date
    from datetime import datetime, timedelta
    last_date = datetime.strptime(last_date_updated, '%Y-%m-%d').date()
    new_date = datetime.strptime(new_game_date, '%Y-%m-%d').date()
    
    # If same date, use that date (inclusive). Otherwise, use day after last_date (exclusive)
    if new_date == last_date:
        # Same date - query for games on that exact date
        start_date = last_date_updated
        end_date = new_game_date
        print(f"Updating master training data for date: {new_game_date}")
    else:
        # Different dates - use day after last_date (exclusive)
        start_date = (last_date + timedelta(days=1)).strftime('%Y-%m-%d')
        end_date = new_game_date
        print(f"Updating master training data: {start_date} to {end_date}")
    
    # Update incrementally
    games_added, updated_path = update_master_training_data_incremental(
        db,
        start_date,
        end_date,
        master_path
    )
    
    print(f"Added {games_added} new games to master training data")
    
    return games_added, updated_path

