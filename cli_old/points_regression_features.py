"""
Points Regression Feature Sets - Feature grouping for points prediction model

Uses FeatureRegistry (SSoT) for feature validation and follows the standard
pipe-delimited naming convention: stat|time_period|calc_weight|perspective
"""

from typing import List, Dict
from nba_app.core.features.registry import FeatureRegistry


# All available features for points regression (in new SSoT-compliant format)
ALL_POINTS_FEATURES: List[str] = [
    # Base Team Efficiency (Season Averages)
    "off_rtg|season|avg|home",
    "off_rtg|season|avg|away",
    "def_rtg|season|avg|home",
    "def_rtg|season|avg|away",
    "pace|season|avg|home",
    "pace|season|avg|away",
    "efg|season|avg|home",
    "efg|season|avg|away",
    "to_metric|season|avg|home",
    "to_metric|season|avg|away",
    "reb_off_pct|season|avg|home",
    "reb_off_pct|season|avg|away",
    "three_rate|season|avg|home",
    "three_rate|season|avg|away",
    "three_pct_allowed|season|avg|home",
    "three_pct_allowed|season|avg|away",

    # Recent Form (Last 10 Games)
    "off_rtg|games_10|avg|home",
    "off_rtg|games_10|avg|away",
    "pace|games_10|avg|home",
    "pace|games_10|avg|away",

    # Recent Scoring (Last 5 Games)
    "points|games_5|avg|home",
    "points|games_5|avg|away",

    # Player Availability (PER-based)
    "player_team_per|season|weighted_MPG|home",
    "player_team_per|season|weighted_MPG|away",
    "player_starters_per|season|avg|home",
    "player_starters_per|season|avg|away",
    "player_team_per|season|avg|home",
    "player_team_per|season|avg|away",
    "player_per_1|season|raw|home",
    "player_per_1|season|raw|away",
    "player_per_1|season|raw|diff",

    # Interaction Features (Matchup-level)
    "three_pct_matchup|season|derived|home",
    "three_pct_matchup|season|derived|away",
    "pace_interaction|season|harmonic_mean|none",

    # Contextual Features
    "home_court|none|raw|home",  # Binary indicator for home team
    "days_rest|none|raw|home",
    "days_rest|none|raw|away",
    "b2b|none|raw|home",
    "b2b|none|raw|away",
    "travel|days_2|avg|home",
    "travel|days_2|avg|away",
]

# Feature Sets organized by category
POINTS_FEATURE_SETS: Dict[str, List[str]] = {
    "team_efficiency": [
        "off_rtg|season|avg|home",
        "off_rtg|season|avg|away",
        "def_rtg|season|avg|home",
        "def_rtg|season|avg|away",
        "pace|season|avg|home",
        "pace|season|avg|away",
        "efg|season|avg|home",
        "efg|season|avg|away",
        "to_metric|season|avg|home",
        "to_metric|season|avg|away",
        "reb_off_pct|season|avg|home",
        "reb_off_pct|season|avg|away",
    ],

    "three_point_profile": [
        "three_rate|season|avg|home",
        "three_rate|season|avg|away",
        "three_pct_allowed|season|avg|home",
        "three_pct_allowed|season|avg|away",
    ],

    "recent_form": [
        "off_rtg|games_10|avg|home",
        "off_rtg|games_10|avg|away",
        "pace|games_10|avg|home",
        "pace|games_10|avg|away",
        "points|games_5|avg|home",
        "points|games_5|avg|away",
    ],

    "player_availability": [
        "player_team_per|season|weighted_MPG|home",
        "player_team_per|season|weighted_MPG|away",
        "player_starters_per|season|avg|home",
        "player_starters_per|season|avg|away",
        "player_team_per|season|avg|home",
        "player_team_per|season|avg|away",
        "player_per_1|season|raw|home",
        "player_per_1|season|raw|away",
        "player_per_1|season|raw|diff",
    ],

    "interaction_features": [
        "three_pct_matchup|season|derived|home",
        "three_pct_matchup|season|derived|away",
        "pace_interaction|season|harmonic_mean|none",
    ],

    "contextual": [
        "home_court|none|raw|home",
        "days_rest|none|raw|home",
        "days_rest|none|raw|away",
        "b2b|none|raw|home",
        "b2b|none|raw|away",
        "travel|days_2|avg|home",
        "travel|days_2|avg|away",
    ],
}

# Feature set descriptions
POINTS_FEATURE_SET_DESCRIPTIONS: Dict[str, str] = {
    "team_efficiency": "Core team efficiency metrics: offensive/defensive ratings, pace, shooting efficiency, turnovers, rebounding",
    "three_point_profile": "Three-point attempt rates and opponent 3P% defense",
    "recent_form": "Recent performance indicators: last 10 games offensive rating and pace, last 5 games scoring average",
    "player_availability": "Player talent metrics: PER-weighted averages, starters PER, top scorer PPG",
    "interaction_features": "Derived interaction features: three-point matchup and projected pace",
    "contextual": "Game context: home court advantage, rest days, back-to-back status, travel distance",
}


def get_points_features_by_sets(feature_sets: List[str]) -> List[str]:
    """
    Get all features from specified feature sets.

    Args:
        feature_sets: List of feature set names

    Returns:
        List of feature names
    """
    features = []
    for set_name in feature_sets:
        if set_name in POINTS_FEATURE_SETS:
            features.extend(POINTS_FEATURE_SETS[set_name])
    return list(set(features))  # Remove duplicates


def generate_feature_set_hash(features: List[str]) -> str:
    """
    Generate MD5 hash of sorted feature list.

    Args:
        features: List of feature names

    Returns:
        MD5 hash string
    """
    import hashlib
    features_sorted = sorted(features)
    features_str = ','.join(features_sorted)
    return hashlib.md5(features_str.encode()).hexdigest()


def validate_points_features() -> Dict[str, any]:
    """
    Validate all points regression features against FeatureRegistry.

    Returns:
        Validation result dict with 'valid', 'errors', 'invalid_features'
    """
    return FeatureRegistry.validate_feature_list(ALL_POINTS_FEATURES)


# Note: Some features may not yet be defined in the registry.
# The following features need registry definitions:
# - reb_off_pct: Offensive rebound percentage
# - three_pct_allowed: Opponent 3PT% allowed
# - three_pct_matchup: Derived three-point matchup metric
# - home_court: Binary home court indicator
#
# Until these are added to the registry, validation will fail for those features.
# This is intentional - it highlights which features need to be added to the SSoT.
