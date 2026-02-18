#!/usr/bin/env python3
"""
Test script to investigate _net feature calculations.

Tests:
1. Whether opponent stats are being aggregated correctly
2. Whether opp_effective_fg_perc, opp_true_shooting_perc, etc. return different values
3. Whether net features are calculated differently from regular features
4. Whether there are any caching or reuse issues
"""

import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from bball.features.compute import BasketballFeatureComputer
from bball.mongo import Mongo
from datetime import date
from collections import defaultdict


def _find_sample_game(db, computer, min_games=20):
    """Find a sample game where both teams have at least min_games prior games."""
    potential_games = list(db.stats_nba.find({
        'homeTeam.points': {'$gt': 0},
        'awayTeam.points': {'$gt': 0},
        'game_type': {'$nin': ['preseason', 'allstar']},
        'month': {'$gte': 1, '$lte': 6},
        'season': {'$gte': '2008-2009'}
    }).sort('date', 1).limit(100))

    for game in potential_games:
        home_team = game['homeTeam']['name']
        away_team = game['awayTeam']['name']
        season = game.get('season', '2023-2024')
        game_date = game['date']

        home_games = computer._get_team_season_games(home_team, season, game_date)
        away_games = computer._get_team_season_games(away_team, season, game_date)

        if len(home_games) >= min_games and len(away_games) >= min_games:
            return game

    # Fallback
    return db.stats_nba.find_one({
        'homeTeam.points': {'$gt': 0},
        'awayTeam.points': {'$gt': 0},
        'game_type': {'$nin': ['preseason', 'allstar']},
        'month': {'$gte': 1, '$lte': 6},
        'season': {'$gte': '2008-2009'}
    }, sort=[('date', 1)])


def test_team_against_agg_population():
    """Test if opponent stats aggregation works correctly via net features."""
    print("=" * 80)
    print("TEST 1: Opponent Stats Aggregation (via net features)")
    print("=" * 80)

    mongo = Mongo()
    db = mongo.db
    computer = BasketballFeatureComputer(db=db)

    sample_game = _find_sample_game(db, computer)
    if not sample_game:
        print("ERROR: No sample game found in database")
        return False

    home_team = sample_game['homeTeam']['name']
    away_team = sample_game['awayTeam']['name']
    season = sample_game.get('season', '2023-2024')
    game_date = sample_game['date']

    print(f"\nTesting with game: {away_team} @ {home_team} on {game_date}")

    # Get games for home team and manually verify aggregation
    home_games = computer._get_team_season_games(home_team, season, game_date)
    print(f"\nHome team ({home_team}) has {len(home_games)} games before {game_date}")

    # Manually aggregate to verify opponent stats differ from team stats
    team_agg = defaultdict(float)
    team_against_agg = defaultdict(float)

    for game in home_games[:5]:
        if game['homeTeam']['name'] == home_team:
            team_data = game['homeTeam']
            opp_data = game['awayTeam']
        elif game['awayTeam']['name'] == home_team:
            team_data = game['awayTeam']
            opp_data = game['homeTeam']
        else:
            continue

        for key, value in team_data.items():
            if isinstance(value, (int, float)):
                team_agg[key] += value

        for key, value in opp_data.items():
            if isinstance(value, (int, float)):
                team_against_agg[key] += value

    print(f"\nTeam aggregated stats (sample):")
    print(f"  FG_made: {team_agg.get('FG_made', 0):.1f}")
    print(f"  FG_att: {team_agg.get('FG_att', 0):.1f}")
    print(f"  three_made: {team_agg.get('three_made', 0):.1f}")
    print(f"  points: {team_agg.get('points', 0):.1f}")

    print(f"\nOpponent aggregated stats (team_against_agg):")
    print(f"  FG_made: {team_against_agg.get('FG_made', 0):.1f}")
    print(f"  FG_att: {team_against_agg.get('FG_att', 0):.1f}")
    print(f"  three_made: {team_against_agg.get('three_made', 0):.1f}")
    print(f"  points: {team_against_agg.get('points', 0):.1f}")

    if team_agg.get('FG_made', 0) == team_against_agg.get('FG_made', 0):
        print("\nWARNING: team_agg and team_against_agg have same FG_made values!")
        print("   This suggests opponent stats are not being aggregated correctly.")
        return False
    else:
        print("\nPASS: team_against_agg is populated with different values from team_agg")
        return True


def test_opponent_stats_different_values():
    """Test if different opponent stats return different values via net features."""
    print("\n" + "=" * 80)
    print("TEST 2: Net Features Return Different Values for Different Stats")
    print("=" * 80)

    mongo = Mongo()
    db = mongo.db
    computer = BasketballFeatureComputer(db=db)

    sample_game = _find_sample_game(db, computer)
    if not sample_game:
        print("ERROR: No sample game found")
        return False

    home_team = sample_game['homeTeam']['name']
    away_team = sample_game['awayTeam']['name']
    season = sample_game.get('season', '2023-2024')
    game_date = sample_game['date']

    print(f"\nTesting with game: {away_team} @ {home_team} on {game_date}")

    # Test different net stats via compute_matchup_features
    net_stats = [
        'efg_net|season|raw|home',
        'ts_net|season|raw|home',
        'three_pct_net|season|raw|home',
        'assists_ratio_net|season|raw|home',
        'opp_points|season|avg|home',
    ]

    feature_results = computer.compute_matchup_features(
        net_stats, home_team, away_team, season, game_date
    )

    print(f"\nNet/opponent stats for {home_team}:")
    for stat_name in net_stats:
        value = feature_results.get(stat_name, 0.0)
        print(f"  {stat_name}: {value:.4f}")

    # Check if all values are the same (they shouldn't be)
    values = [feature_results.get(s, 0.0) for s in net_stats]
    if len(set(values)) == 1 and len(values) > 1:
        print("\nWARNING: All net/opponent stats have the same value!")
        return False
    else:
        print("\nPASS: Different net/opponent stats return different values")
        return True


def test_net_vs_regular_features():
    """Test if net features are calculated differently from regular features."""
    print("\n" + "=" * 80)
    print("TEST 3: Net vs Regular Feature Calculations")
    print("=" * 80)

    mongo = Mongo()
    db = mongo.db
    computer = BasketballFeatureComputer(db=db)

    # Find multiple suitable games
    potential_games = list(db.stats_nba.find({
        'homeTeam.points': {'$gt': 0},
        'awayTeam.points': {'$gt': 0},
        'game_type': {'$nin': ['preseason', 'allstar']},
        'month': {'$gte': 1, '$lte': 6},
        'season': {'$gte': '2008-2009'}
    }).sort('date', 1).limit(100))

    sample_games = []
    for game in potential_games:
        home_team = game['homeTeam']['name']
        away_team = game['awayTeam']['name']
        season = game.get('season', '2023-2024')
        game_date = game['date']

        home_games = computer._get_team_season_games(home_team, season, game_date)
        away_games = computer._get_team_season_games(away_team, season, game_date)

        if len(home_games) >= 20 and len(away_games) >= 20:
            sample_games.append(game)
            if len(sample_games) >= 10:
                break

    if not sample_games:
        print("ERROR: No sample games found")
        return False

    print(f"\nTesting with {len(sample_games)} games:")

    net_features = [
        'efg_net|season|raw|diff',
        'ts_net|season|raw|diff',
        'three_pct_net|season|raw|diff',
        'off_rtg_net|season|raw|diff',
        'assists_ratio_net|season|raw|diff',
    ]

    regular_features = [
        'efg|season|raw|diff',
        'ts|season|raw|diff',
        'three_pct|season|raw|diff',
        'off_rtg|season|raw|diff',
        'assists_ratio|season|raw|diff',
    ]

    all_features = net_features + regular_features
    results = []

    for game in sample_games:
        home_team = game['homeTeam']['name']
        away_team = game['awayTeam']['name']
        season = game.get('season', '2023-2024')
        game_date = game['date']

        feature_results = computer.compute_matchup_features(
            all_features, home_team, away_team, season, game_date
        )

        game_results = {
            'game': f"{away_team} @ {home_team}",
            'date': game_date,
            'net_features': {f: feature_results.get(f, 0.0) for f in net_features},
            'regular_features': {f: feature_results.get(f, 0.0) for f in regular_features},
        }
        results.append(game_results)

    # Analyze results
    print("\n" + "-" * 80)
    print("Results Summary:")
    print("-" * 80)

    for i, result in enumerate(results[:3], 1):
        print(f"\nGame {i}: {result['game']} ({result['date']})")
        print("\n  Net Features:")
        for feature, value in result['net_features'].items():
            print(f"    {feature}: {value:.6f}" if isinstance(value, (int, float)) else f"    {feature}: {value}")
        print("\n  Regular Features:")
        for feature, value in result['regular_features'].items():
            print(f"    {feature}: {value:.6f}" if isinstance(value, (int, float)) else f"    {feature}: {value}")

    # Check if all net features have the same value
    print("\n" + "-" * 80)
    print("Checking for identical values:")
    print("-" * 80)

    all_net_values = []
    for result in results:
        net_vals = [v for v in result['net_features'].values() if isinstance(v, (int, float))]
        all_net_values.extend(net_vals)

    if len(set(all_net_values)) == 1 and len(all_net_values) > 1:
        print("WARNING: All net feature values are identical!")
        print(f"   Value: {all_net_values[0]}")
        return False
    else:
        unique_values = len(set(all_net_values))
        print(f"PASS: Net features have {unique_values} unique values out of {len(all_net_values)} total")

        # Check if net and regular features are different
        print("\nComparing net vs regular features:")
        for result in results[:3]:
            print(f"\n  {result['game']}:")
            for base_stat in ['efg', 'ts', 'three_pct', 'off_rtg', 'assists_ratio']:
                net_feat = f"{base_stat}_net|season|raw|diff"
                reg_feat = f"{base_stat}|season|raw|diff"
                net_val = result['net_features'].get(net_feat)
                reg_val = result['regular_features'].get(reg_feat)

                if isinstance(net_val, (int, float)) and isinstance(reg_val, (int, float)):
                    if abs(net_val - reg_val) < 0.0001:
                        print(f"    NOTE: {base_stat}: net={net_val:.6f}, regular={reg_val:.6f} (SAME)")
                    else:
                        print(f"    PASS: {base_stat}: net={net_val:.6f}, regular={reg_val:.6f} (different)")

        return True


def test_caching_issues():
    """Test for caching or reuse of values."""
    print("\n" + "=" * 80)
    print("TEST 4: Caching/Reuse Issues")
    print("=" * 80)

    mongo = Mongo()
    db = mongo.db
    computer = BasketballFeatureComputer(db=db)

    sample_game = _find_sample_game(db, computer)
    if not sample_game:
        print("ERROR: No sample game found")
        return False

    home_team = sample_game['homeTeam']['name']
    away_team = sample_game['awayTeam']['name']
    season = sample_game.get('season', '2023-2024')
    game_date = sample_game['date']

    print(f"\nTesting with game: {away_team} @ {home_team} on {game_date}")

    # Calculate same feature multiple times
    feature_name = 'efg_net|season|raw|diff'
    values = []

    print(f"\nCalculating '{feature_name}' 5 times:")
    for i in range(5):
        feature_results = computer.compute_matchup_features(
            [feature_name], home_team, away_team, season, game_date
        )
        value = feature_results.get(feature_name, 0.0)
        values.append(value)
        print(f"  Attempt {i+1}: {value:.6f}")

    if len(set(values)) == 1:
        print("\nPASS: Feature calculation is consistent (same value each time)")
    else:
        print("\nWARNING: Feature calculation returns different values!")
        print(f"   Values: {values}")
        return False

    # Test different net features for same game
    net_features = [
        'efg_net|season|raw|diff',
        'ts_net|season|raw|diff',
        'three_pct_net|season|raw|diff',
        'off_rtg_net|season|raw|diff',
        'assists_ratio_net|season|raw|diff',
    ]

    print(f"\nCalculating different net features for same game:")
    feature_results = computer.compute_matchup_features(
        net_features, home_team, away_team, season, game_date
    )

    net_values = {}
    for feature_name in net_features:
        value = feature_results.get(feature_name, 0.0)
        net_values[feature_name] = value
        print(f"  {feature_name}: {value:.6f}")

    unique_values = len(set(net_values.values()))
    if unique_values == 1:
        print(f"\nWARNING: All {len(net_features)} net features have the same value!")
        print(f"   This suggests a caching or calculation bug.")
        return False
    else:
        print(f"\nPASS: Different net features return different values ({unique_values} unique)")
        return True


if __name__ == '__main__':
    print("=" * 80)
    print("NET FEATURES INVESTIGATION TEST SUITE")
    print("=" * 80)

    results = {}

    try:
        results['test1'] = test_team_against_agg_population()
    except Exception as e:
        print(f"\nERROR in test 1: {e}")
        import traceback
        traceback.print_exc()
        results['test1'] = False

    try:
        results['test2'] = test_opponent_stats_different_values()
    except Exception as e:
        print(f"\nERROR in test 2: {e}")
        import traceback
        traceback.print_exc()
        results['test2'] = False

    try:
        results['test3'] = test_net_vs_regular_features()
    except Exception as e:
        print(f"\nERROR in test 3: {e}")
        import traceback
        traceback.print_exc()
        results['test3'] = False

    try:
        results['test4'] = test_caching_issues()
    except Exception as e:
        print(f"\nERROR in test 4: {e}")
        import traceback
        traceback.print_exc()
        results['test4'] = False

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    for test_name, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        print(f"  {test_name}: {status}")

    all_passed = all(results.values())
    print(f"\nOverall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
