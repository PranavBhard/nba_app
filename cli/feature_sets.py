"""
Feature Sets Module - Modular feature grouping for ablation studies

Defines 11 semantically coherent feature sets for the NBA win prediction classifier.
Each set can be toggled on/off for ablation studies and interpretability.
"""

# =============================================================================
# FEATURE SET DEFINITIONS
# =============================================================================

FEATURE_SETS = {
    # Set 1: Team Outcome Strength (Multi-Window Differentials)
    # NOTE: Contains both diff and per-team features - use filter_by_model_type() to get appropriate subset
    "outcome_strength": [
        # Scoring outcome (diff features - for LogisticRegression)
        "points|season|avg|diff",
        "points|months_1|avg|diff",
        "points|games_10|avg|diff",
        "points|season|avg|diff|side",
        "points|months_1|avg|diff|side",
        "points|games_10|avg|diff|side",
        # Net scoring outcome (opponent-adjusted - for LogisticRegression)
        "points_net|season|raw|diff",
        "points_net|season|avg|diff",
        "points_net|season|raw|diff|side",
        "points_net|season|avg|diff|side",
        # Win/loss outcome (diff features - for LogisticRegression)
        "wins|season|avg|diff",
        "wins|months_1|avg|diff",
        "wins|games_10|avg|diff",
        "wins|season|avg|diff|side",
        "wins|months_1|avg|diff|side",
        "wins|games_10|avg|diff|side",
        # Per-team absolute features (for Tree/NN models)
        # Standardized naming: home{Stat}, away{Stat}
        "points|season|avg|home",
        "points|season|avg|away",
        "points|season|avg|home|side",
        "points|season|avg|away|side",
        "wins|season|avg|home",
        "wins|season|avg|away",
        "wins|season|avg|home|side",
        "wins|season|avg|away|side",
    ],
    
    # Set 2: Shooting Efficiency & Shot Profile
    # NOTE: Contains both diff and per-team features - use filter_by_model_type() to get appropriate subset
    "shooting_efficiency": [
        # Efficiency (diff features - for LogisticRegression)
        # Rate stats: raw is more important (computed across all games), but include both raw and avg
        "efg|season|raw|diff",
        "efg|season|avg|diff",
        "efg|season|raw|diff|side",
        "efg|season|avg|diff|side",
        "efg|months_1|raw|diff",
        "efg|months_1|avg|diff",
        "efg|games_10|raw|diff",
        "efg|games_10|avg|diff",
        "ts|season|raw|diff",
        "ts|season|avg|diff",
        "ts|season|raw|diff|side",
        "ts|season|avg|diff|side",
        "ts|months_1|raw|diff",
        "ts|months_1|avg|diff",
        "ts|games_10|raw|diff",
        "ts|games_10|avg|diff",
        # 3-point profile (diff)
        "three_made|season|avg|diff",
        "three_made|season|avg|diff|side",
        "three_pct|season|raw|diff",
        "three_pct|season|avg|diff",
        "three_pct|season|raw|diff|side",
        "three_pct|season|avg|diff|side",
        "three_pct|months_1|raw|diff",
        "three_pct|months_1|avg|diff",
        "three_pct|games_10|raw|diff",
        "three_pct|games_10|avg|diff",
        # Net efficiency features (opponent-adjusted - for LogisticRegression)
        "efg_net|season|raw|diff",
        "efg_net|season|avg|diff",
        "efg_net|season|raw|diff|side",
        "efg_net|season|avg|diff|side",
        "ts_net|season|raw|diff",
        "ts_net|season|avg|diff",
        "ts_net|season|raw|diff|side",
        "ts_net|season|avg|diff|side",
        "three_pct_net|season|raw|diff",
        "three_pct_net|season|avg|diff",
        "three_pct_net|season|raw|diff|side",
        "three_pct_net|season|avg|diff|side",
    ],
    
    # Set 3: Offensive Engine & Ball Movement
    # NOTE: Contains both diff and per-team features - use filter_by_model_type() to get appropriate subset
    "offensive_engine": [
        # Base offensive ratings & playmaking (diff - for LogisticRegression)
        # Rate stats: raw is more important (computed across all games), but include both raw and avg
        "off_rtg|season|raw|diff",
        "off_rtg|season|avg|diff",
        "off_rtg|season|raw|diff|side",
        "off_rtg|season|avg|diff|side",
        "off_rtg|months_1|raw|diff",
        "off_rtg|months_1|avg|diff",
        "off_rtg|games_10|raw|diff",
        "off_rtg|games_10|avg|diff",
        "assists_ratio|season|raw|diff",
        "assists_ratio|season|avg|diff",
        "assists_ratio|season|raw|diff|side",
        "assists_ratio|season|avg|diff|side",
        "assists_ratio|months_1|raw|diff",
        "assists_ratio|months_1|avg|diff",
        "assists_ratio|games_10|raw|diff",
        "assists_ratio|games_10|avg|diff",
        # Net offensive ratings (opponent-adjusted - for LogisticRegression)
        "off_rtg_net|season|raw|diff",
        "off_rtg_net|season|avg|diff",
        "off_rtg_net|season|raw|diff|side",
        "off_rtg_net|season|avg|diff|side",
        "assists_ratio_net|season|raw|diff",
        "assists_ratio_net|season|avg|diff",
        "assists_ratio_net|season|raw|diff|side",
        "assists_ratio_net|season|avg|diff|side",
        # Note: off_rtg|none|raw|home/away/diff removed - time_period='none' doesn't make sense for rate stats
    ],
    
    # Set 4: Defensive Engine & Possession Control
    # NOTE: Contains both diff and per-team features - use filter_by_model_type() to get appropriate subset
    "defensive_engine": [
        # Defensive ratings (diff - for LogisticRegression)
        # Rate stat: raw is more important (computed across all games), but include both raw and avg
        "def_rtg|season|raw|diff",
        "def_rtg|season|avg|diff",
        "def_rtg|season|raw|diff|side",
        "def_rtg|season|avg|diff|side",
        "def_rtg|months_1|raw|diff",
        "def_rtg|months_1|avg|diff",
        "def_rtg|games_10|raw|diff",
        "def_rtg|games_10|avg|diff",
        # Note: def_rtg|none|raw|home/away/diff removed - time_period='none' doesn't make sense for rate stats
        # Possession & rim protection (diff)
        "reb_total|season|avg|diff",
        "reb_total|season|avg|diff|side",
        "blocks|season|avg|diff",
        "blocks|season|avg|diff|side",
        "steals|season|avg|diff",
        "steals|season|avg|diff|side",
        # Turnover control (diff)
        "turnovers|season|avg|diff",
        # Turnover metric (rate stat - to_metric)
        "to_metric|season|raw|diff",
    ],
    
    # Set 5: Pace & Volatility Features
    # NOTE: Contains both diff and per-team features - use filter_by_model_type() to get appropriate subset
    "pace_volatility": [
        "pace|season|avg|diff",
        "pace|season|avg|home",
        "pace|season|avg|away",
    ],
    
    # Set 6: Schedule & Fatigue Context
    # NOTE: Contains both diff and per-team features - use filter_by_model_type() to get appropriate subset
    "schedule_fatigue": [
        # Travel features
        "travel|days_2|avg|diff",
        "travel|days_2|avg|home",
        "travel|days_2|avg|away",
        "travel|days_5|avg|diff",
        "travel|days_5|avg|home",
        "travel|days_5|avg|away",
        "travel|days_12|avg|diff",
        "travel|days_12|avg|home",
        "travel|days_12|avg|away",
    ],
    
    # Set 7: Games-Played / Sample Size Features
    # NOTE: Contains both diff and per-team features - use filter_by_model_type() to get appropriate subset
    "sample_size": [
        "games_played|season|avg|diff",
        "games_played|season|avg|home",
        "games_played|season|avg|away",
    ],

    # Set 8: Elo & Macro Strength Trend
    "elo_strength": [
        "elo|none|raw|diff",
    ],

    # Set 9: Era-Normalized Relative Strength
    # NOTE: Contains both diff and per-team features - use filter_by_model_type() to get appropriate subset
    "era_normalization": [
        # Era normalization uses relative calculations within the stat handler
        # Add specific features here if needed
    ],

    # Set 10: Player Talent (PER) Feature Set
    # NOTE: Contains both diff and per-team features - use filter_by_model_type() to get appropriate subset
    "player_talent": [
        "player_team_per|season|weighted_MPG|diff",
        "player_team_per|season|avg|diff",
    ],

    # Set 11: Absolute Magnitude Context (Team Stats, Season Averages)
    # Standardized naming: all features use home{Stat}, away{Stat} format
    "absolute_magnitude": [
        "points|season|avg|home",
        "points|season|avg|away",
        "off_rtg|season|avg|home",
        "off_rtg|season|avg|away",
    ],

    # Set 12: Injury Impact Features
    # NOTE: Contains both diff and per-team features - use filter_by_model_type() to get appropriate subset
    "injuries": [
        "inj_impact|none|blend:severity:0.45/top1_per:0.35/rotation:0.20|diff",
    ],
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def is_diff_feature(feature_name: str) -> bool:
    """
    Determine if a feature is a differential (diff) feature.

    Features with |diff suffix (e.g., 'points|season|avg|diff')
    """
    # New format: check for |diff suffix
    if '|' in feature_name:
        return feature_name.endswith('|diff') or '|diff|' in feature_name
    
    # Old format (deprecated, should not be used): check for Diff suffix
    if feature_name.endswith('Diff') or 'Diff' in feature_name:
        return True
    
    return False


def is_per_team_feature(feature_name: str) -> bool:
    """
    Determine if a feature is a per-team feature (home/away separate).
    
    New format: Features with |home or |away suffix (e.g., 'points|season|avg|home')
    Old format (deprecated): Features starting with 'home'/'away'
    Diff features are NOT per-team.
    """
    # If it's a diff feature, it's NOT per-team
    if is_diff_feature(feature_name):
        return False
    
    # New format: check for |home or |away suffix
    if '|' in feature_name:
        return feature_name.endswith('|home') or feature_name.endswith('|away') or '|home|' in feature_name or '|away|' in feature_name
    
    # Old format (deprecated, should not be used): check for home/away prefix
    if feature_name.startswith('home') or feature_name.startswith('away'):
        return True
    
    return False


def filter_features_by_model_type(features: list, model_type: str = None) -> list:
    """
    Filter features based on model type requirements.
    
    Args:
        features: List of feature names to filter
        model_type: One of 'LogisticRegression', 'Tree', 'NeuralNetwork', or None
                   If None, returns all features (no filtering)
    
    Returns:
        Filtered list of features based on model type:
        - LogisticRegression: Only diff features
        - Tree/NeuralNetwork: Only per-team features
        - None: All features (no filtering)
    """
    if model_type is None:
        return features
    
    model_type_lower = model_type.lower()
    
    # LogisticRegression: only diffs
    if 'logistic' in model_type_lower or 'linear' in model_type_lower:
        return [f for f in features if is_diff_feature(f)]
    
    # Tree models and Neural Networks: only per-team
    if 'tree' in model_type_lower or 'neural' in model_type_lower or 'xgboost' in model_type_lower or \
       'lightgbm' in model_type_lower or 'catboost' in model_type_lower or 'gradient' in model_type_lower or \
       'randomforest' in model_type_lower or 'svm' in model_type_lower:
        return [f for f in features if is_per_team_feature(f)]
    
    # Default: return all (for unknown model types)
    return features


def get_all_features(model_type: str = None) -> list:
    """
    Get all features from all sets, optionally filtered by model type.
    
    Args:
        model_type: Optional model type to filter features ('LogisticRegression', 'Tree', 'NeuralNetwork')
    
    Returns:
        List of feature names, filtered if model_type is provided
    """
    all_features = []
    for features in FEATURE_SETS.values():
        all_features.extend(features)
    
    return filter_features_by_model_type(all_features, model_type)


def get_features_by_sets(set_names: list, model_type: str = None) -> list:
    """
    Get features for specified sets, optionally filtered by model type.
    
    Args:
        set_names: List of feature set names to include
        model_type: Optional model type to filter features ('LogisticRegression', 'Tree', 'NeuralNetwork')
        
    Returns:
        List of feature names, filtered if model_type is provided
    """
    features = []
    for set_name in set_names:
        if set_name in FEATURE_SETS:
            features.extend(FEATURE_SETS[set_name])
    
    return filter_features_by_model_type(features, model_type)


def get_features_excluding_sets(excluded_sets: list, model_type: str = None) -> list:
    """
    Get all features except those in excluded sets, optionally filtered by model type.
    
    Args:
        excluded_sets: List of feature set names to exclude
        model_type: Optional model type to filter features ('LogisticRegression', 'Tree', 'NeuralNetwork')
        
    Returns:
        List of feature names, filtered if model_type is provided
    """
    all_features = get_all_features(model_type=model_type)
    excluded_features = []
    for set_name in excluded_sets:
        if set_name in FEATURE_SETS:
            excluded_features.extend(FEATURE_SETS[set_name])
    
    # Filter excluded features by model type too
    excluded_features = filter_features_by_model_type(excluded_features, model_type)
    
    return [f for f in all_features if f not in excluded_features]


def get_set_name_for_feature(feature_name: str) -> str:
    """
    Get the feature set name for a given feature.
    
    Args:
        feature_name: Name of the feature
        
    Returns:
        Feature set name, or None if not found
    """
    for set_name, features in FEATURE_SETS.items():
        if feature_name in features:
            return set_name
    return None


def get_feature_set_info() -> dict:
    """
    Get information about all feature sets.
    
    Returns:
        Dict mapping set names to their feature counts
    """
    return {
        set_name: len(features)
        for set_name, features in FEATURE_SETS.items()
    }


# =============================================================================
# FEATURE SET DESCRIPTIONS (for documentation)
# =============================================================================

FEATURE_SET_DESCRIPTIONS = {
    "outcome_strength": "Highest-level 'scoreboard' signals: points and wins across multiple time windows",
    "shooting_efficiency": "How efficiently teams turn possessions into points (shot quality & spacing)",
    "offensive_engine": "Possession-level offensive quality and ball movement (process-oriented metrics)",
    "defensive_engine": "Prevent opponent scoring / control possessions (defense + possession control)",
    "pace_volatility": "Tempo (possessions) and consistency (volatility) metrics",
    "schedule_fatigue": "Short-term fatigue and schedule density (rest, back-to-backs, recent games)",
    "sample_size": "Data reliability signal (how much information available per team)",
    "elo_strength": "Single high-signal summary of team strength (meta-feature over other signals)",
    "era_normalization": "Normalized relative to league average (removes era effects)",
    "player_talent": "Player-level talent aggregations (PER-based team metrics)",
    "absolute_magnitude": "Non-differential magnitude features (absolute team performance levels)",
}


# =============================================================================
# LAYER DEFINITIONS (4-layer conceptual hierarchy)
# =============================================================================

FEATURE_LAYERS = {
    # Layer 1: Outcome & Ratings (Core Strength Comparison)
    "layer_1": [
        "outcome_strength",
        "shooting_efficiency",
        "offensive_engine",
        "defensive_engine",
    ],
    
    # Layer 2: Tempo, Schedule, Sample Size (Situational Context)
    "layer_2": [
        "pace_volatility",
        "schedule_fatigue",
        "sample_size",
    ],
    
    # Layer 3: Meta Priors & Normalization (Global Calibration)
    "layer_3": [
        "elo_strength",
        "era_normalization",
    ],
    
    # Layer 4: Player Talent & Absolute Magnitudes (Detailed Structure)
    "layer_4": [
        "player_talent",
        "absolute_magnitude",
    ],
}

LAYER_DESCRIPTIONS = {
    "layer_1": "Outcome & ratings - core strength comparison",
    "layer_2": "Tempo, schedule, sample size - situational context",
    "layer_3": "Meta priors & normalization - global calibration",
    "layer_4": "Player talent & absolute magnitudes - detailed structure",
}


def get_features_by_layers(layer_names: list, model_type: str = None) -> list:
    """
    Get features for specified layers, optionally filtered by model type.
    
    Args:
        layer_names: List of layer names (e.g., ['layer_1', 'layer_2'])
        model_type: Optional model type to filter features ('LogisticRegression', 'Tree', 'NeuralNetwork')
        
    Returns:
        List of feature names, filtered if model_type is provided
    """
    feature_sets = []
    for layer_name in layer_names:
        if layer_name in FEATURE_LAYERS:
            feature_sets.extend(FEATURE_LAYERS[layer_name])
    
    return get_features_by_sets(feature_sets, model_type=model_type)


def get_layer_info() -> dict:
    """
    Get information about all layers.
    
    Returns:
        Dict mapping layer names to their feature counts and set names
    """
    info = {}
    for layer_name, set_names in FEATURE_LAYERS.items():
        total_features = sum(len(FEATURE_SETS[set_name]) for set_name in set_names)
        info[layer_name] = {
            'sets': set_names,
            'feature_count': total_features,
            'description': LAYER_DESCRIPTIONS.get(layer_name, '')
        }
    return info


def get_common_layer_configs() -> dict:
    """
    Get common layer configuration presets for testing.
    
    Returns:
        Dict mapping config names to layer lists
    """
    return {
        'layer_1_only': ['layer_1'],
        'layer_1_2': ['layer_1', 'layer_2'],
        'layer_1_2_3': ['layer_1', 'layer_2', 'layer_3'],
        'layer_1_2_4': ['layer_1', 'layer_2', 'layer_4'],
        'all_layers': ['layer_1', 'layer_2', 'layer_3', 'layer_4'],
        'core_only': ['layer_1', 'layer_3'],  # Core strength + meta priors
        'context_heavy': ['layer_1', 'layer_2', 'layer_4'],  # Skip era normalization
    }

