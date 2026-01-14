#!/usr/bin/env python3
"""
Feature Name Parser - Parse new feature naming convention.

New format: <stat_name>|<time_period>|<calc_weight>|<home/away/diff>|side

This module provides functions to:
1. Parse new feature names into components
2. Convert parsed components back to feature names
3. Validate feature name format
"""

from typing import Dict, Optional, Tuple, List
import re


class FeatureNameComponents:
    """Container for parsed feature name components."""
    
    def __init__(
        self,
        stat_name: str,
        time_period: str,
        calc_weight: str,
        home_away_diff: str,
        is_side: bool = False
    ):
        self.stat_name = stat_name
        self.time_period = time_period
        self.calc_weight = calc_weight
        self.home_away_diff = home_away_diff  # 'home', 'away', or 'diff'
        self.is_side = is_side
    
    def to_feature_name(self) -> str:
        """Convert components back to feature name."""
        parts = [
            self.stat_name,
            self.time_period,
            self.calc_weight,
            self.home_away_diff
        ]
        
        if self.is_side:
            parts.append('side')
        
        return '|'.join(parts)
    
    def __repr__(self):
        return f"FeatureNameComponents({self.to_feature_name()})"


def parse_feature_name(feature_name: str) -> Optional[FeatureNameComponents]:
    """
    Parse a feature name in the new format.
    
    Format: <stat_name>|<time_period>|<calc_weight>|<home/away/diff>|side
    
    Args:
        feature_name: Feature name in new format
        
    Returns:
        FeatureNameComponents object, or None if parsing fails
    """
    if not feature_name or '|' not in feature_name:
        return None
    
    parts = feature_name.split('|')
    
    # Minimum 4 parts required (stat_name, time_period, calc_weight, home/away/diff)
    if len(parts) < 4:
        return None
    
    stat_name = parts[0]
    time_period = parts[1]
    calc_weight = parts[2]
    home_away_diff = parts[3]
    
    # Check for optional side flag (5th part)
    is_side = len(parts) > 4 and parts[4] == 'side'
    
    # Validate home_away_diff
    if home_away_diff not in ['home', 'away', 'diff', 'none']:
        # Special case: per_available uses 'none' as placeholder
        if stat_name == 'per_available' and home_away_diff == 'none':
            pass  # OK
        else:
            return None
    
    return FeatureNameComponents(
        stat_name=stat_name,
        time_period=time_period,
        calc_weight=calc_weight,
        home_away_diff=home_away_diff,
        is_side=is_side
    )


def validate_feature_name(feature_name: str) -> bool:
    """Validate that a feature name follows the new format."""
    components = parse_feature_name(feature_name)
    return components is not None


def get_feature_type(feature_name: str) -> Optional[str]:
    """
    Determine the type of feature (base_stat, enhanced, per, injury, special).
    
    Returns:
        Feature type string, or None if unknown
    """
    components = parse_feature_name(feature_name)
    if not components:
        return None
    
    stat_name = components.stat_name
    
    # Base stat features
    base_stats = [
        'points', 'wins', 'efg', 'ts', 'off_rtg', 'def_rtg',
        'assists_ratio', 'turnovers', 'three_made', 'three_pct',
        'reb_total', 'blocks'
    ]
    if stat_name in base_stats:
        return 'base_stat'
    
    # Enhanced features
    enhanced_stats = [
        'games_played', 'pace', 'travel', 'b2b'
    ]
    if stat_name in enhanced_stats:
        return 'enhanced'
    
    # Era normalization
    if 'rel' in components.calc_weight or stat_name in ['ppg']:
        return 'era_normalization'
    
    # PER features
    if stat_name.startswith('player_'):
        return 'per'
    
    # Injury features
    if stat_name.startswith('inj_'):
        return 'injury'
    
    # All stats are normal stats now - no special categorization needed
    
    return 'unknown'


def filter_features_by_type(features: List[str], feature_type: str) -> List[str]:
    """Filter features by type."""
    return [f for f in features if get_feature_type(f) == feature_type]


def is_diff_feature(feature_name: str) -> bool:
    """Check if feature is a differential feature."""
    components = parse_feature_name(feature_name)
    return components is not None and components.home_away_diff == 'diff'


def is_per_team_feature(feature_name: str) -> bool:
    """Check if feature is a per-team feature (home/away separate)."""
    components = parse_feature_name(feature_name)
    return components is not None and components.home_away_diff in ['home', 'away']


def is_side_feature(feature_name: str) -> bool:
    """Check if feature is a side-split feature."""
    components = parse_feature_name(feature_name)
    return components is not None and components.is_side

