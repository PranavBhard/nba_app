"""
Model-Specific Feature Builders

Implements separate feature pipelines for different model types as specified in
feature_set_architecture.md. Each model type gets features optimized for its architecture.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import date

from nba_app.cli.StatHandlerV2 import StatHandlerV2
from nba_app.cli.per_calculator import PERCalculator


class ModelSpecificFeatureBuilder:
    """Base class for model-specific feature builders."""
    
    def __init__(
        self,
        stat_handler: StatHandlerV2,
        per_calculator: Optional[PERCalculator] = None,
        include_elo: bool = True,
        include_era_normalization: bool = False,
        include_injuries: bool = False,
        recency_decay_k: float = 15.0
    ):
        self.stat_handler = stat_handler
        self.per_calculator = per_calculator
        self.include_elo = include_elo
        self.include_era_normalization = include_era_normalization
        self.include_injuries = include_injuries
        self.recency_decay_k = recency_decay_k
    
    def build_features(
        self,
        HOME: str,
        AWAY: str,
        season: str,
        year: int,
        month: int,
        day: int,
        elo_diff: float = 0.0,
        rest_diff: float = 0.0,
        player_filters: Optional[Dict] = None,
        injured_players: Optional[Dict] = None
    ) -> Dict:
        """
        Build features for a game matchup.
        
        Args:
            player_filters: Optional dict with team names as keys:
                {team: {'playing': [player_ids], 'starters': [player_ids]}}
            injured_players: Optional dict with team names as keys:
                {team: [player_ids]} - List of injured player IDs for each team
                Training: Should pass stats_nba.{home/away}Team.injured_players
                Prediction: Should pass injured players from nba_rosters.injured flag
        
        Returns:
            Dict with feature values (structure depends on model type)
        """
        raise NotImplementedError


class LogisticRegressionFeatureBuilder(ModelSpecificFeatureBuilder):
    """
    Feature builder for Logistic Regression.
    
    Strategy: Pure differential modeling + optional absolutes.
    Uses flattened vector of differentials.
    """
    
    def build_features(
        self,
        HOME: str,
        AWAY: str,
        season: str,
        year: int,
        month: int,
        day: int,
        elo_diff: float = 0.0,
        rest_diff: float = 0.0,
        player_filters: Optional[Dict] = None
    ) -> Dict:
        """Build differential-based features for Logistic Regression."""
        features = {}
        
        # Get base differentials from stat handler
        base_diffs = self.stat_handler.getStatAvgDiffs(
            HOME, AWAY, season, year, month, day,
            point_regression=False,
            # Enhanced features always included (team-level only)
        )
        
        if base_diffs == 'SOME BS':
            return None
        
        # Build feature dict from base diffs
        # The stat handler returns a list matching the order of statistics
        # Map list indices to feature names based on statistics order
        stat_idx = 0
        for stat in self.stat_handler.statistics:
            if stat_idx < len(base_diffs):
                features[f"{stat}Diff"] = base_diffs[stat_idx]
                stat_idx += 1
                
                # Add absolutes for key stats (if enabled)
                if self.stat_handler.include_absolute and self.stat_handler._is_key_stat(stat):
                    if stat_idx < len(base_diffs):
                        features[f"{stat}_home_abs"] = base_diffs[stat_idx]
                        stat_idx += 1
                    if stat_idx < len(base_diffs):
                        features[f"{stat}_away_abs"] = base_diffs[stat_idx]
                        stat_idx += 1
        
        # Enhanced features - calculate directly using new format feature names
        # Note: This file uses old format feature names for backward compatibility with model-specific builders
        # Enhanced features are calculated via calculate_feature() but mapped to old format names
        enhanced_features = [
            'pace|season|avg|diff',
            'points|season|std|diff',
            'games_played|days_3|avg|diff',
            'games_played|days_5|avg|diff',
            'b2b|none|raw|diff',
            'travel|days_12|avg|diff',
        ]
        for feature_name in enhanced_features:
            try:
                value = self.stat_handler.calculate_feature(
                    feature_name, HOME, AWAY, season, year, month, day, None
                )
                # Use new format feature names (old format removed)
                features[feature_name] = value
            except Exception:
                # If calculation fails, set to 0 (use new format feature names)
                if feature_name == 'pace|season|avg|diff':
                    features['pace|season|avg|diff'] = 0.0
                elif feature_name == 'points|season|std|diff':
                    features['points|season|std|diff'] = 0.0
                elif feature_name == 'games_played|days_3|avg|diff':
                    features['games_played|days_3|avg|diff'] = 0.0
                elif feature_name == 'games_played|days_5|avg|diff':
                    features['games_played|days_5|avg|diff'] = 0.0
                elif feature_name == 'b2b|none|raw|diff':
                    features['b2b|none|raw|diff'] = 0.0
                elif feature_name == 'travel|days_12|avg|diff':
                    features['travel|days_12|avg|diff'] = 0.0
        
        # Elo (new format)
        if self.include_elo:
            features['elo|none|raw|diff'] = elo_diff
        
        # Rest (new format)
        features['rest|none|raw|diff'] = rest_diff
        
        # Era normalization (differentials)
        if self.include_era_normalization:
            era_features = self.stat_handler.get_era_normalized_features(
                HOME, AWAY, season, year, month, day
            )
            features.update(era_features)
        
        # PER aggregates (differentials)
        if self.per_calculator:
            game_date = f"{year}-{month:02d}-{day:02d}"
            per_features = self.per_calculator.get_game_per_features(
                HOME, AWAY, season, game_date, 
                player_filters=player_filters,
                injured_players=injured_players
            )
            if per_features:
                # PER features are now in new format - extract diff features directly
                per_diffs = {
                    'perAvgDiff': per_features.get('player_team_per|season|avg|diff', 0),
                    'perWeightedDiff': per_features.get('player_team_per|season|weighted_MPG|diff', 0),
                    'startersPerDiff': per_features.get('player_starters_per|season|avg|diff', 0),
                    'per1Diff': per_features.get('player_per_1|season|top1_avg|diff', 0),
                    'per2Diff': per_features.get('player_per_2|season|top1_avg|diff', 0),
                    'per3Diff': per_features.get('player_per_3|season|top1_avg|diff', 0),
                }
                features.update(per_diffs)
        
        # Injury features (differentials)
        if self.include_injuries:
            game_date = f"{year}-{month:02d}-{day:02d}"
            injury_features = self.stat_handler.get_injury_features(
                HOME, AWAY, season, year, month, day,
                game_doc=None,
                per_calculator=self.per_calculator,
                recency_decay_k=self.recency_decay_k
            )
            if injury_features:
                # For LogisticRegression, only include diff features (new format)
                injury_diffs = {
                    'inj_per|none|weighted_MIN|diff': injury_features.get('inj_per|none|weighted_MIN|diff', 0.0),
                    'inj_per|none|top1_avg|diff': injury_features.get('inj_per|none|top1_avg|diff', 0.0),
                    'inj_per|none|top3_sum|diff': injury_features.get('inj_per|none|top3_sum|diff', 0.0),
                    'inj_min_lost|none|raw|diff': injury_features.get('inj_min_lost|none|raw|diff', 0.0),
                    'inj_severity|none|raw|diff': injury_features.get('inj_severity|none|raw|diff', 0.0),
                    'inj_rotation_per|none|raw|diff': injury_features.get('inj_rotation_per|none|raw|diff', 0.0),
                }
                features.update(injury_diffs)
        
        return features


class TreeModelFeatureBuilder(ModelSpecificFeatureBuilder):
    """
    Feature builder for Tree Models (XGBoost, LightGBM, GradientBoosting).
    
    Strategy: Per-team blocks ONLY + explicit interactions.
    NO differential features - trees can learn interactions from per-team features.
    """
    
    def build_features(
        self,
        HOME: str,
        AWAY: str,
        season: str,
        year: int,
        month: int,
        day: int,
        elo_diff: float = 0.0,
        rest_diff: float = 0.0,
        player_filters: Optional[Dict] = None
    ) -> Dict:
        """Build per-team + interaction features for tree models."""
        features = {}
        
        # Calculate enhanced features directly using new format feature names
        # Map to old format names for backward compatibility with model-specific builders
        enhanced_feature_map = {
            # Home team features
            'homeOffRtg': 'off_rtg|season|avg|home',
            'homeDefRtg': 'def_rtg|season|avg|home',
            'homePace': 'pace|season|avg|home',
            'homeEfgOff': 'efg|season|avg|home',
            'homeEfgDef': 'efg|season|avg|home',  # Note: efgDef is opponent efg, need to handle separately
            'homePointsStd': 'points|season|std|home',
            'homeGamesPlayed': 'games_played|season|avg|home',
            'homeGamesLast3Days': 'games_played|days_3|avg|home',
            'homeGamesLast5Days': 'games_played|days_5|avg|home',
            'homeB2B': 'b2b|none|raw|home',
            'homeTravel12': 'travel|days_12|avg|home',
            'homeTravel5': 'travel|days_5|avg|home',
            # Away team features
            'awayOffRtg': 'off_rtg|season|avg|away',
            'awayDefRtg': 'def_rtg|season|avg|away',
            'awayPace': 'pace|season|avg|away',
            'awayEfgOff': 'efg|season|avg|away',
            'awayEfgDef': 'efg|season|avg|away',  # Note: efgDef is opponent efg, need to handle separately
            'awayPointsStd': 'points|season|std|away',
            'awayGamesPlayed': 'games_played|season|avg|away',
            'awayGamesLast3Days': 'games_played|days_3|avg|away',
            'awayGamesLast5Days': 'games_played|days_5|avg|away',
            'awayB2B': 'b2b|none|raw|away',
            'awayTravel12': 'travel|days_12|avg|away',
            'awayTravel5': 'travel|days_5|avg|away',
        }
        
        for old_name, new_name in enhanced_feature_map.items():
            try:
                value = self.stat_handler.calculate_feature(
                    new_name, HOME, AWAY, season, year, month, day, None
                )
                features[old_name] = value
            except Exception:
                features[old_name] = 0.0
        
        # Handle efgDef separately (opponent efg) - this requires special handling
        # For now, set to 0 as it's not directly available via calculate_feature
        features['homeEfgDef'] = 0.0
        features['awayEfgDef'] = 0.0
        
        # Get base stats for per-team blocks
        # We need to compute home/away stats separately
        # For now, use what we have from enhanced features and add more from base stats
        
        # Get season averages for both teams
        from nba_app.cli.db_query_funcs import getTeamSeasonGamesFromDate
        home_games = getTeamSeasonGamesFromDate(HOME, year, month, day, season, self.stat_handler.all_games)
        away_games = getTeamSeasonGamesFromDate(AWAY, year, month, day, season, self.stat_handler.all_games)
        
        if len(home_games) == 0 or len(away_games) == 0:
            return None
        
        # Aggregate and compute advanced stats for per-team features
        home_agg, home_against, _, _, _, _ = self.stat_handler._aggregate_games(home_games, HOME)
        away_agg, away_against, _, _, _, _ = self.stat_handler._aggregate_games(away_games, AWAY)
        
        home_adv = self.stat_handler._compute_advanced_stats(home_agg, home_against, len(home_games))
        away_adv = self.stat_handler._compute_advanced_stats(away_agg, away_against, len(away_games))
        
        # Add more per-team stats - using standardized names
        features['homePointsSznAvg'] = home_adv.get('ppg', 0)
        features['awayPointsSznAvg'] = away_adv.get('ppg', 0)
        home_wins_pct = sum(1 for g in home_games if 
            (g['homeTeam']['name'] == HOME and g['homeWon']) or
            (g['awayTeam']['name'] == HOME and not g['homeWon'])) / len(home_games) if len(home_games) > 0 else 0
        away_wins_pct = sum(1 for g in away_games if
            (g['homeTeam']['name'] == AWAY and g['homeWon']) or
            (g['awayTeam']['name'] == AWAY and not g['homeWon'])) / len(away_games) if len(away_games) > 0 else 0
        features['homeWinsSznAvg'] = home_wins_pct
        features['awayWinsSznAvg'] = away_wins_pct
        
        # Add base stats from stat handler (per-team)
        # These come from the statistics list in the stat handler
        # We'll compute them per-team for tree models
        home_to_metric = home_adv.get('to_metric', 0)
        away_to_metric = away_adv.get('to_metric', 0)
        features['homeToMetric'] = home_to_metric
        features['awayToMetric'] = away_to_metric
        
        # Rebounding stats (if available)
        home_reb = home_agg.get('total_reb', 0) / len(home_games) if len(home_games) > 0 else 0
        away_reb = away_agg.get('total_reb', 0) / len(away_games) if len(away_games) > 0 else 0
        features['homeTotalRebSznAvg'] = home_reb
        features['awayTotalRebSznAvg'] = away_reb
        
        # Assists ratio
        home_ast_ratio = home_adv.get('ast_ratio', 0)
        away_ast_ratio = away_adv.get('ast_ratio', 0)
        features['homeAstRatioSznAvg'] = home_ast_ratio
        features['awayAstRatioSznAvg'] = away_ast_ratio
        
        # Note: NO diff features for tree models - they can learn interactions from per-team features
        # Trees learn the differentials implicitly from home/away features
        
        # Crossed interaction features (VERY IMPORTANT)
        # Matchup effects that trees can learn - using standardized names
        features['homeOffRtgXawayDefRtg'] = features['homeOffRtg'] * features['awayDefRtg']
        features['homeEfgOffXawayEfgDef'] = features['homeEfgOff'] * features['awayEfgDef']
        features['homePaceXawayPace'] = features['homePace'] * features['awayPace']
        features['homePointsStdXawayPointsStd'] = features['homePointsStd'] * features['awayPointsStd']
        # Turnover interactions (offense vs defense)
        features['homeToMetricXawayDefRtg'] = home_to_metric * features['awayDefRtg']
        # Rebounding interactions (offense vs defense)
        features['homeTotalRebSznAvgXawayDefRtg'] = home_reb * features['awayDefRtg']
        # Assists interactions
        features['homeAstRatioSznAvgXawayDefRtg'] = home_ast_ratio * features['awayDefRtg']
        
        # Elo (per-team only - need actual elo values)
        # Note: If we only have elo_diff, we skip it for tree models
        # Tree models should have homeElo and awayElo separately
        # For now, we'll skip elo if we only have the diff
        # TODO: Add per-team elo values when available
        
        # PER aggregates (per-team, not diff) - using standardized names
        if self.per_calculator:
            game_date = f"{year}-{month:02d}-{day:02d}"
            per_features = self.per_calculator.get_game_per_features(
                HOME, AWAY, season, game_date, 
                player_filters=player_filters,
                injured_players=injured_players
            )
            if per_features:
                # PER features are now in new format - map to old format keys for backward compatibility
                features['homeTeamPerAvg'] = per_features.get('player_team_per|season|avg|home', 0)
                features['homeTeamPerWeighted'] = per_features.get('player_team_per|season|weighted_MPG|home', 0)
                features['homeStartersPerAvg'] = per_features.get('player_starters_per|season|avg|home', 0)
                features['homePer1'] = per_features.get('player_per_1|season|top1_avg|home', 0)
                features['homePer2'] = per_features.get('player_per_2|season|top1_avg|home', 0)
                features['homePer3'] = per_features.get('player_per_3|season|top1_avg|home', 0)
                
                features['awayTeamPerAvg'] = per_features.get('player_team_per|season|avg|away', 0)
                features['awayTeamPerWeighted'] = per_features.get('player_team_per|season|weighted_MPG|away', 0)
                features['awayStartersPerAvg'] = per_features.get('player_starters_per|season|avg|away', 0)
                features['awayPer1'] = per_features.get('player_per_1|season|top1_avg|away', 0)
                features['awayPer2'] = per_features.get('player_per_2|season|top1_avg|away', 0)
                features['awayPer3'] = per_features.get('player_per_3|season|top1_avg|away', 0)
        
        # Injury features (per-team)
        if self.include_injuries:
            game_date = f"{year}-{month:02d}-{day:02d}"
            injury_features = self.stat_handler.get_injury_features(
                HOME, AWAY, season, year, month, day,
                game_doc=None,
                per_calculator=self.per_calculator,
                recency_decay_k=self.recency_decay_k
            )
            if injury_features:
                # For Tree models, include both per-team and diff features (new format)
                features['inj_per|none|weighted_MIN|home'] = injury_features.get('inj_per|none|weighted_MIN|home', 0.0)
                features['inj_per|none|weighted_MIN|away'] = injury_features.get('inj_per|none|weighted_MIN|away', 0.0)
                features['inj_per|none|top1_avg|home'] = injury_features.get('inj_per|none|top1_avg|home', 0.0)
                features['inj_per|none|top1_avg|away'] = injury_features.get('inj_per|none|top1_avg|away', 0.0)
                features['inj_per|none|top3_sum|home'] = injury_features.get('inj_per|none|top3_sum|home', 0.0)
                features['inj_per|none|top3_sum|away'] = injury_features.get('inj_per|none|top3_sum|away', 0.0)
                features['inj_min_lost|none|raw|home'] = injury_features.get('inj_min_lost|none|raw|home', 0.0)
                features['inj_min_lost|none|raw|away'] = injury_features.get('inj_min_lost|none|raw|away', 0.0)
                features['inj_severity|none|raw|home'] = injury_features.get('inj_severity|none|raw|home', 0.0)
                features['inj_severity|none|raw|away'] = injury_features.get('inj_severity|none|raw|away', 0.0)
                features['inj_rotation_per|none|raw|home'] = injury_features.get('inj_rotation_per|none|raw|home', 0.0)
                features['inj_rotation_per|none|raw|away'] = injury_features.get('inj_rotation_per|none|raw|away', 0.0)
                # Also include diff features for trees
                features['inj_per|none|weighted_MIN|diff'] = injury_features.get('inj_per|none|weighted_MIN|diff', 0.0)
                features['inj_per|none|top1_avg|diff'] = injury_features.get('inj_per|none|top1_avg|diff', 0.0)
                features['inj_per|none|top3_sum|diff'] = injury_features.get('inj_per|none|top3_sum|diff', 0.0)
                features['inj_min_lost|none|raw|diff'] = injury_features.get('inj_min_lost|none|raw|diff', 0.0)
                features['inj_severity|none|raw|diff'] = injury_features.get('inj_severity|none|raw|diff', 0.0)
                features['inj_rotation_per|none|raw|diff'] = injury_features.get('inj_rotation_per|none|raw|diff', 0.0)
        
        # Era normalization (per-team relative) - using standardized names
        if self.include_era_normalization:
            era_features = self.stat_handler.get_era_normalized_features(
                HOME, AWAY, season, year, month, day
            )
            if era_features:
                features['homePpgRel'] = era_features.get('homePpgRel', 0)
                features['awayPpgRel'] = era_features.get('awayPpgRel', 0)
                features['homeOffRtgRel'] = era_features.get('homeOffRtgRel', 0)
                features['awayOffRtgRel'] = era_features.get('awayOffRtgRel', 0)
        
        return features


class NeuralNetworkFeatureBuilder(ModelSpecificFeatureBuilder):
    """
    Feature builder for Neural Networks.
    
    Strategy: Structured per-team blocks (no diffs, no interactions - NN handles this).
    """
    
    def build_features(
        self,
        HOME: str,
        AWAY: str,
        season: str,
        year: int,
        month: int,
        day: int,
        elo_diff: float = 0.0,
        rest_diff: float = 0.0,
        player_filters: Optional[Dict] = None
    ) -> Dict:
        """
        Build structured per-team features for neural networks.
        
        Returns:
            Dict with 'home' and 'away' keys, each containing full team feature dict
        """
        # Get season stats for both teams
        from nba_app.cli.db_query_funcs import getTeamSeasonGamesFromDate
        home_games = getTeamSeasonGamesFromDate(HOME, year, month, day, season, self.stat_handler.all_games)
        away_games = getTeamSeasonGamesFromDate(AWAY, year, month, day, season, self.stat_handler.all_games)
        
        if len(home_games) == 0 or len(away_games) == 0:
            return None
        
        # Aggregate stats
        home_agg, home_against, _, _, _, _ = self.stat_handler._aggregate_games(home_games, HOME)
        away_agg, away_against, _, _, _, _ = self.stat_handler._aggregate_games(away_games, AWAY)
        
        home_adv = self.stat_handler._compute_advanced_stats(home_agg, home_against, len(home_games))
        away_adv = self.stat_handler._compute_advanced_stats(away_agg, away_against, len(away_games))
        
        # Calculate enhanced features directly using new format feature names
        home_pace = self.stat_handler.calculate_feature('pace|season|avg|home', HOME, AWAY, season, year, month, day, None) or 0.0
        away_pace = self.stat_handler.calculate_feature('pace|season|avg|away', HOME, AWAY, season, year, month, day, None) or 0.0
        home_points_std = self.stat_handler.calculate_feature('points|season|std|home', HOME, AWAY, season, year, month, day, None) or 0.0
        away_points_std = self.stat_handler.calculate_feature('points|season|std|away', HOME, AWAY, season, year, month, day, None) or 0.0
        home_games_played = self.stat_handler.calculate_feature('games_played|season|avg|home', HOME, AWAY, season, year, month, day, None) or 0.0
        away_games_played = self.stat_handler.calculate_feature('games_played|season|avg|away', HOME, AWAY, season, year, month, day, None) or 0.0
        home_games_3d = self.stat_handler.calculate_feature('games_played|days_3|avg|home', HOME, AWAY, season, year, month, day, None) or 0.0
        away_games_3d = self.stat_handler.calculate_feature('games_played|days_3|avg|away', HOME, AWAY, season, year, month, day, None) or 0.0
        home_games_5d = self.stat_handler.calculate_feature('games_played|days_5|avg|home', HOME, AWAY, season, year, month, day, None) or 0.0
        away_games_5d = self.stat_handler.calculate_feature('games_played|days_5|avg|away', HOME, AWAY, season, year, month, day, None) or 0.0
        home_b2b = self.stat_handler.calculate_feature('b2b|none|raw|home', HOME, AWAY, season, year, month, day, None) or 0.0
        away_b2b = self.stat_handler.calculate_feature('b2b|none|raw|away', HOME, AWAY, season, year, month, day, None) or 0.0
        
        # Build per-team feature blocks
        home_features = {
            'off_rtg': home_adv.get('off_rtg', 0),
            'def_rtg': home_adv.get('def_rtg', 0),
            'pace': home_pace,
            'efg': home_adv.get('efg', 0),
            'ts': home_adv.get('ts', 0),
            'wins': sum(1 for g in home_games if 
                (g['homeTeam']['name'] == HOME and g['homeWon']) or
                (g['awayTeam']['name'] == HOME and not g['homeWon'])) / len(home_games) if len(home_games) > 0 else 0,
            'points': home_adv.get('ppg', 0),
            'volatility': home_points_std,
            'games_played': home_games_played,
            'games_last_3_days': home_games_3d,
            'games_last_5_days': home_games_5d,
            'is_b2b': home_b2b,
            'is_home': 1,  # Context indicator
        }
        
        away_features = {
            'off_rtg': away_adv.get('off_rtg', 0),
            'def_rtg': away_adv.get('def_rtg', 0),
            'pace': away_pace,
            'efg': away_adv.get('efg', 0),
            'ts': away_adv.get('ts', 0),
            'wins': sum(1 for g in away_games if
                (g['homeTeam']['name'] == AWAY and g['homeWon']) or
                (g['awayTeam']['name'] == AWAY and not g['homeWon'])) / len(away_games) if len(away_games) > 0 else 0,
            'points': away_adv.get('ppg', 0),
            'volatility': away_points_std,
            'games_played': away_games_played,
            'games_last_3_days': away_games_3d,
            'games_last_5_days': away_games_5d,
            'is_b2b': away_b2b,
            'is_home': 0,  # Context indicator
        }
        
        # Elo (per-team)
        if self.include_elo:
            # Would need actual elo values, for now use placeholder
            home_features['elo'] = 1500  # Placeholder
            away_features['elo'] = 1500  # Placeholder
        
        # PER aggregates
        if self.per_calculator:
            game_date = f"{year}-{month:02d}-{day:02d}"
            per_features = self.per_calculator.get_game_per_features(
                HOME, AWAY, season, game_date, 
                player_filters=player_filters,
                injured_players=injured_players
            )
            if per_features:
                # PER features are now in new format
                home_features['team_per_avg'] = per_features.get('player_team_per|season|avg|home', 0)
                home_features['team_per_weighted'] = per_features.get('player_team_per|season|weighted_MPG|home', 0)
                home_features['starters_per_avg'] = per_features.get('player_starters_per|season|avg|home', 0)
                home_features['top_per1'] = per_features.get('player_per_1|season|top1_avg|home', 0)
                home_features['top_per2'] = per_features.get('player_per_2|season|top1_avg|home', 0)
                home_features['top_per3'] = per_features.get('player_per_3|season|top1_avg|home', 0)
                
                away_features['team_per_avg'] = per_features.get('player_team_per|season|avg|away', 0)
                away_features['team_per_weighted'] = per_features.get('player_team_per|season|weighted_MPG|away', 0)
                away_features['starters_per_avg'] = per_features.get('player_starters_per|season|avg|away', 0)
                away_features['top_per1'] = per_features.get('player_per_1|season|top1_avg|away', 0)
                away_features['top_per2'] = per_features.get('player_per_2|season|top1_avg|away', 0)
                away_features['top_per3'] = per_features.get('player_per_3|season|top1_avg|away', 0)
        
        # Era normalization
        if self.include_era_normalization:
            era_features = self.stat_handler.get_era_normalized_features(
                HOME, AWAY, season, year, month, day
            )
            if era_features:
                home_features['ppg_rel'] = era_features.get('homePpgRel', 0)
                home_features['off_rtg_rel'] = era_features.get('homeOffRtgRel', 0)
                away_features['ppg_rel'] = era_features.get('awayPpgRel', 0)
                away_features['off_rtg_rel'] = era_features.get('awayOffRtgRel', 0)
        
        # Injury features (per-team)
        if self.include_injuries:
            game_date = f"{year}-{month:02d}-{day:02d}"
            injury_features = self.stat_handler.get_injury_features(
                HOME, AWAY, season, year, month, day,
                game_doc=None,
                per_calculator=self.per_calculator,
                recency_decay_k=self.recency_decay_k
            )
            if injury_features:
                home_features['inj_per_value'] = injury_features.get('inj_per|none|weighted_MIN|home', 0.0)
                home_features['inj_top1_per'] = injury_features.get('inj_per|none|top1_avg|home', 0.0)
                home_features['inj_top3_per_sum'] = injury_features.get('inj_per|none|top3_sum|home', 0.0)
                home_features['inj_min_lost'] = injury_features.get('inj_min_lost|none|raw|home', 0.0)
                home_features['injury_severity'] = injury_features.get('inj_severity|none|raw|home', 0.0)
                home_features['inj_rotation'] = injury_features.get('inj_rotation_per|none|raw|home', 0.0)
                away_features['inj_per_value'] = injury_features.get('inj_per|none|weighted_MIN|away', 0.0)
                away_features['inj_top1_per'] = injury_features.get('inj_per|none|top1_avg|away', 0.0)
                away_features['inj_top3_per_sum'] = injury_features.get('inj_per|none|top3_sum|away', 0.0)
                away_features['inj_min_lost'] = injury_features.get('inj_min_lost|none|raw|away', 0.0)
                away_features['injury_severity'] = injury_features.get('inj_severity|none|raw|away', 0.0)
                away_features['inj_rotation'] = injury_features.get('inj_rotation_per|none|raw|away', 0.0)
        
        return {
            'home': home_features,
            'away': away_features
        }


def get_feature_builder(model_type: str, stat_handler: StatHandlerV2, 
                       per_calculator: Optional[PERCalculator] = None,
                       include_elo: bool = True,
                       include_era_normalization: bool = False,
                       include_injuries: bool = False,
                       recency_decay_k: float = 15.0) -> ModelSpecificFeatureBuilder:
    """
    Factory function to get the appropriate feature builder for a model type.
    
    Args:
        model_type: One of:
                   - 'LogisticRegression', 'SVM' (linear models → differential features)
                   - 'GradientBoosting', 'XGBoost', 'LightGBM', 'CatBoost', 'RandomForest' (tree models → per-team + interactions)
                   - 'NeuralNetwork', 'MLPClassifier' (neural networks → structured blocks)
                   - 'NaiveBayes' (defaults to differential features)
        stat_handler: StatHandlerV2 instance
        per_calculator: Optional PERCalculator instance
        include_elo: Whether to include Elo features
        include_era_normalization: Whether to include era normalization
        
    Returns:
        Appropriate ModelSpecificFeatureBuilder instance
    """
    tree_models = ['GradientBoosting', 'XGBoost', 'LightGBM', 'CatBoost', 'RandomForest']
    neural_models = ['NeuralNetwork', 'MLPClassifier']
    linear_models = ['LogisticRegression', 'SVM']  # SVM is linear, uses same features as LR
    
    if model_type in linear_models:
        # LogisticRegression and SVM both benefit from differential features
        return LogisticRegressionFeatureBuilder(
            stat_handler, per_calculator, include_elo, include_era_normalization,
            include_injuries, recency_decay_k
        )
    elif model_type in tree_models:
        return TreeModelFeatureBuilder(
            stat_handler, per_calculator, include_elo, include_era_normalization,
            include_injuries, recency_decay_k
        )
    elif model_type in neural_models:
        return NeuralNetworkFeatureBuilder(
            stat_handler, per_calculator, include_elo, include_era_normalization,
            include_injuries, recency_decay_k
        )
    else:
        # Default to LogisticRegression for unknown types (e.g., NaiveBayes)
        # NaiveBayes can work with differential features, but may benefit from different structure
        return LogisticRegressionFeatureBuilder(
            stat_handler, per_calculator, include_elo, include_era_normalization,
            include_injuries, recency_decay_k
        )

