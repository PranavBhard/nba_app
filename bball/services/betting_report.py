"""
Betting Report Service - Generate betting recommendations based on model vs market edge.

Compares model predictions against Kalshi market odds and recommends stakes
using a Kelly Criterion-based approach with confidence adjustments.
"""

from datetime import datetime
from typing import List, Dict, Optional, TYPE_CHECKING

from sportscore.services.betting_report import (
    BetRecommendation,
    prob_to_american_odds,
    format_time_for_report,
    calculate_stake,
)

if TYPE_CHECKING:
    from bball.league_config import LeagueConfig


def generate_betting_report(
    db,
    game_date: str,
    bankroll: float,
    brier_score: float,
    league: Optional["LeagueConfig"] = None,
    edge_threshold: float = 0.07,
    force_include_game_ids: Optional[List[str]] = None
) -> List[BetRecommendation]:
    """
    Generate betting recommendations for games on a date.

    Compares model predictions against Kalshi market data and returns
    recommendations for value bets where model edge >= edge_threshold.
    Games in force_include_game_ids are always included (e.g. games with
    existing fills) even if edge is below threshold.

    Args:
        db: MongoDB database instance
        game_date: Date string in 'YYYY-MM-DD' format
        bankroll: Total bankroll amount
        brier_score: Model's Brier score for confidence adjustment
        league: Optional league config
        edge_threshold: Minimum edge required (default 0.07 = 7%)
        force_include_game_ids: Game IDs to always include regardless of edge

    Returns:
        List of BetRecommendation objects, sorted by game time
    """
    from bball.market.kalshi import get_game_market_data

    # Get collection names from league config
    if league is not None:
        games_coll = league.collections.get("games", "stats_nba")
        predictions_coll = league.collections.get("model_predictions", "nba_model_predictions")
        league_id = league.league_id
    else:
        games_coll = "stats_nba"
        predictions_coll = "nba_model_predictions"
        league_id = "nba"

    # Parse date
    try:
        game_date_obj = datetime.strptime(game_date, '%Y-%m-%d').date()
    except ValueError:
        return []

    # Fetch predictions for the date
    predictions_cursor = db[predictions_coll].find({'game_date': game_date})
    predictions_by_game = {}
    for pred in predictions_cursor:
        game_id = pred.get('game_id')
        if game_id:
            predictions_by_game[game_id] = pred

    if not predictions_by_game:
        return []

    # Fetch games for the date to get game times and team info
    games_cursor = db[games_coll].find({'date': game_date})
    games_by_id = {}
    for game in games_cursor:
        game_id = game.get('game_id')
        if game_id:
            games_by_id[game_id] = game

    recommendations = []
    force_set = set(force_include_game_ids) if force_include_game_ids else set()
    included_game_ids = set()

    for game_id, pred in predictions_by_game.items():
        game = games_by_id.get(game_id)
        if not game:
            continue

        home_team = pred.get('home_team') or game.get('homeTeam', {}).get('name')
        away_team = pred.get('away_team') or game.get('awayTeam', {}).get('name')

        if not home_team or not away_team:
            continue

        # Get model probabilities (stored as 0-100 in predictions collection)
        model_home_prob = pred.get('home_win_prob', 0)
        model_away_prob = pred.get('away_win_prob', 0)

        # Convert to 0.0-1.0 scale
        model_home_prob = model_home_prob / 100.0 if model_home_prob > 1 else model_home_prob
        model_away_prob = model_away_prob / 100.0 if model_away_prob > 1 else model_away_prob

        # Fetch market data from Kalshi
        market_data = get_game_market_data(
            game_date=game_date_obj,
            away_team=away_team,
            home_team=home_team,
            league_id=league_id,
            use_cache=True
        )

        if not market_data:
            continue

        market_home_prob = market_data.home_yes_price
        market_away_prob = market_data.away_yes_price
        mkt_status = market_data.status or "unknown"

        # Get game time
        gametime = game.get('gametime')
        if gametime:
            if isinstance(gametime, str):
                try:
                    gametime = datetime.fromisoformat(gametime.replace('Z', '+00:00'))
                except ValueError:
                    gametime = None
        gametime_formatted = format_time_for_report(gametime) if gametime else "TBD"

        home_edge = model_home_prob - market_home_prob
        away_edge = model_away_prob - market_away_prob
        force_this = game_id in force_set

        # Check home team edge
        if home_edge >= edge_threshold and market_home_prob > 0:
            stake_info = calculate_stake(model_home_prob, market_home_prob, brier_score, bankroll)

            recommendations.append(BetRecommendation(
                game_id=game_id,
                game_time=gametime,
                game_time_formatted=gametime_formatted,
                team=home_team,
                home_team=home_team,
                away_team=away_team,
                market_prob=market_home_prob,
                market_odds=prob_to_american_odds(market_home_prob),
                model_prob=model_home_prob,
                model_odds=prob_to_american_odds(model_home_prob),
                edge=home_edge,
                edge_kelly=stake_info['edge_kelly'],
                dog_variance_penalty=stake_info['dog_variance_penalty'],
                stake_fraction=stake_info['stake_fraction'],
                stake=stake_info['stake'],
                adjusted_stake=stake_info['adjusted_stake'],
                market_status=mkt_status
            ))
            included_game_ids.add(game_id)

        # Check away team edge
        if away_edge >= edge_threshold and market_away_prob > 0:
            stake_info = calculate_stake(model_away_prob, market_away_prob, brier_score, bankroll)

            recommendations.append(BetRecommendation(
                game_id=game_id,
                game_time=gametime,
                game_time_formatted=gametime_formatted,
                team=away_team,
                home_team=home_team,
                away_team=away_team,
                market_prob=market_away_prob,
                market_odds=prob_to_american_odds(market_away_prob),
                model_prob=model_away_prob,
                model_odds=prob_to_american_odds(model_away_prob),
                edge=away_edge,
                edge_kelly=stake_info['edge_kelly'],
                dog_variance_penalty=stake_info['dog_variance_penalty'],
                stake_fraction=stake_info['stake_fraction'],
                stake=stake_info['stake'],
                adjusted_stake=stake_info['adjusted_stake'],
                market_status=mkt_status
            ))
            included_game_ids.add(game_id)

        # Force-include: game has fills but neither side met threshold
        if force_this and game_id not in included_game_ids:
            # Pick the side with the better edge
            if home_edge >= away_edge and market_home_prob > 0:
                best_prob, best_mkt, best_team = model_home_prob, market_home_prob, home_team
                best_edge = home_edge
            elif market_away_prob > 0:
                best_prob, best_mkt, best_team = model_away_prob, market_away_prob, away_team
                best_edge = away_edge
            else:
                continue

            stake_info = calculate_stake(best_prob, best_mkt, brier_score, bankroll)
            recommendations.append(BetRecommendation(
                game_id=game_id,
                game_time=gametime,
                game_time_formatted=gametime_formatted,
                team=best_team,
                home_team=home_team,
                away_team=away_team,
                market_prob=best_mkt,
                market_odds=prob_to_american_odds(best_mkt),
                model_prob=best_prob,
                model_odds=prob_to_american_odds(best_prob),
                edge=best_edge,
                edge_kelly=stake_info['edge_kelly'],
                dog_variance_penalty=stake_info['dog_variance_penalty'],
                stake_fraction=stake_info['stake_fraction'],
                stake=stake_info['stake'],
                adjusted_stake=stake_info['adjusted_stake'],
                market_status=mkt_status
            ))
            included_game_ids.add(game_id)

    # Sort by game time (chronologically)
    def sort_key(rec):
        if rec.game_time is None:
            return datetime.max
        return rec.game_time

    recommendations.sort(key=sort_key)

    return recommendations
