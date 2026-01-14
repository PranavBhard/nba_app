"""
Points Regression Feature Sets - Feature grouping for points prediction model
"""

# All available features for points regression
ALL_POINTS_FEATURES = [
    # Base Team Efficiency (Season Averages)
    'home_offRtg_szn_avg', 'away_offRtg_szn_avg',
    'home_defRtg_szn_avg', 'away_defRtg_szn_avg',
    'home_pace_szn_avg', 'away_pace_szn_avg',
    'home_efg_szn_avg', 'away_efg_szn_avg',
    'home_TOV_pct_szn_avg', 'away_TOV_pct_szn_avg',
    'home_ORB_pct_szn_avg', 'away_ORB_pct_szn_avg',
    'home_3PA_rate', 'away_3PA_rate',
    'home_3P_pct_allowed', 'away_3P_pct_allowed',
    
    # Recent Form (Last 10 Games)
    'home_offRtg_last10', 'away_offRtg_last10',
    'home_pace_last10', 'away_pace_last10',
    
    # Recent Scoring (Last 5 Games)
    'home_points_last5_avg', 'away_points_last5_avg',
    
    # Player Availability
    'home_perWeighted_available', 'away_perWeighted_available',
    'home_startersPer_available', 'away_startersPer_available',
    'home_perAvg_available', 'away_perAvg_available',
    'home_top1PPG_available', 'away_top1PPG_available',
    'top1PPG_diff',
    
    # Interaction Features
    'home_threePointMatchup', 'away_threePointMatchup',
    'projectedPace',
    
    # Contextual Features
    'homeCourt',
    'home_restDays', 'away_restDays',
    'home_b2b', 'away_b2b',
    'travelDistance'
]

# Feature Sets organized by category
POINTS_FEATURE_SETS = {
    "team_efficiency": [
        'home_offRtg_szn_avg', 'away_offRtg_szn_avg',
        'home_defRtg_szn_avg', 'away_defRtg_szn_avg',
        'home_pace_szn_avg', 'away_pace_szn_avg',
        'home_efg_szn_avg', 'away_efg_szn_avg',
        'home_TOV_pct_szn_avg', 'away_TOV_pct_szn_avg',
        'home_ORB_pct_szn_avg', 'away_ORB_pct_szn_avg',
    ],
    
    "three_point_profile": [
        'home_3PA_rate', 'away_3PA_rate',
        'home_3P_pct_allowed', 'away_3P_pct_allowed',
    ],
    
    "recent_form": [
        'home_offRtg_last10', 'away_offRtg_last10',
        'home_pace_last10', 'away_pace_last10',
        'home_points_last5_avg', 'away_points_last5_avg',
    ],
    
    "player_availability": [
        'home_perWeighted_available', 'away_perWeighted_available',
        'home_startersPer_available', 'away_startersPer_available',
        'home_perAvg_available', 'away_perAvg_available',
        'home_top1PPG_available', 'away_top1PPG_available',
        'top1PPG_diff',
    ],
    
    "interaction_features": [
        'home_threePointMatchup', 'away_threePointMatchup',
        'projectedPace',
    ],
    
    "contextual": [
        'homeCourt',
        'home_restDays', 'away_restDays',
        'home_b2b', 'away_b2b',
        'travelDistance',
    ],
}

# Feature set descriptions
POINTS_FEATURE_SET_DESCRIPTIONS = {
    "team_efficiency": "Core team efficiency metrics: offensive/defensive ratings, pace, shooting efficiency, turnovers, rebounding",
    "three_point_profile": "Three-point attempt rates and opponent 3P% defense",
    "recent_form": "Recent performance indicators: last 10 games offensive rating and pace, last 5 games scoring average",
    "player_availability": "Player talent metrics: PER-weighted averages, starters PER, top scorer PPG",
    "interaction_features": "Derived interaction features: three-point matchup and projected pace",
    "contextual": "Game context: home court advantage, rest days, back-to-back status, travel distance",
}

def get_points_features_by_sets(feature_sets: list) -> list:
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

def generate_feature_set_hash(features: list) -> str:
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
