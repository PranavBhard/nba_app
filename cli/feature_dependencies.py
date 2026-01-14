"""
Feature dependency mapping and resolution.

This module provides infrastructure for tracking which features depend on other features,
and for resolving transitive dependencies when regenerating features.
"""

from typing import Dict, List, Set, Tuple
import re


# Direct dependency mappings
# Format: {dependent_feature: [list of features it depends on]}
FEATURE_DEPENDENCIES: Dict[str, List[str]] = {
    # Injury impact blend feature - home
    'inj_impact|none|blend:severity:0.45/top1_per:0.35/rotation:0.20|home': [
        'inj_severity|none|raw|home',
        'inj_per|none|top1_avg|home',
        'inj_rotation_per|none|raw|home'
    ],
    # Injury impact blend feature - away
    'inj_impact|none|blend:severity:0.45/top1_per:0.35/rotation:0.20|away': [
        'inj_severity|none|raw|away',
        'inj_per|none|top1_avg|away',
        'inj_rotation_per|none|raw|away'
    ],
    # Injury impact blend feature - diff
    'inj_impact|none|blend:severity:0.45/top1_per:0.35/rotation:0.20|diff': [
        'inj_severity|none|raw|diff',
        'inj_per|none|top1_avg|diff',
        'inj_rotation_per|none|raw|diff'
    ],
    # Legacy alias
    'inj_impact|blend|raw|diff': [
        'inj_impact|none|blend:severity:0.45/top1_per:0.35/rotation:0.20|diff'
    ],
}


def parse_blend_feature_dependencies(feature_name: str) -> List[str]:
    """
    Parse a blend feature name and extract its component dependencies.
    
    Blend features have format: {base_stat}_blend|none|blend:{tp1}:{w1}/{tp2}:{w2}/...|{perspective}
    
    Args:
        feature_name: Feature name (e.g., 'wins_blend|none|blend:season:0.80/games_12:0.20|diff')
        
    Returns:
        List of component feature names this blend depends on
    """
    if '|blend:' not in feature_name:
        return []
    
    try:
        parts = feature_name.split('|')
        if len(parts) < 3:
            return []
        
        base_stat = parts[0]  # e.g., 'wins_blend'
        time_period = parts[1]  # e.g., 'blend:season:0.80/games_12:0.20'
        calc_weight = parts[2] if len(parts) > 2 else 'none'
        perspective = parts[3] if len(parts) > 3 else 'diff'
        
        # Remove _blend suffix to get base stat
        if base_stat.endswith('_blend'):
            base_stat_name = base_stat[:-6]  # Remove '_blend'
        else:
            return []  # Not a blend feature
        
        # Parse blend components
        # Format: blend:season:0.80/games_12:0.20
        if not time_period.startswith('blend:'):
            return []
        
        blend_str = time_period[6:]  # Remove 'blend:' prefix
        components = blend_str.split('/')
        
        # Determine calc_weight for components
        # wins_blend uses 'avg', off_rtg_net_blend uses 'raw', etc.
        if base_stat_name in ['wins', 'points_net']:
            component_calc_weight = 'avg'
        elif base_stat_name in ['off_rtg_net', 'efg_net']:
            component_calc_weight = 'raw'
        else:
            component_calc_weight = 'avg'  # Default
        
        # Build component feature names
        dependencies = []
        for component in components:
            # Format: season:0.80 or games_12:0.20
            if ':' not in component:
                continue
            component_time_period = component.split(':')[0]
            
            # Build component feature name
            component_feature = f"{base_stat_name}|{component_time_period}|{component_calc_weight}|{perspective}"
            dependencies.append(component_feature)
        
        return dependencies
    except Exception as e:
        # If parsing fails, return empty list (feature might not be a blend)
        return []


def get_direct_dependencies(feature_name: str) -> List[str]:
    """
    Get direct dependencies for a feature.
    
    Checks both explicit mappings and parses blend features.
    
    Args:
        feature_name: Feature name
        
    Returns:
        List of feature names this feature directly depends on
    """
    # Check explicit mappings first
    if feature_name in FEATURE_DEPENDENCIES:
        return FEATURE_DEPENDENCIES[feature_name].copy()
    
    # Try parsing as blend feature
    blend_deps = parse_blend_feature_dependencies(feature_name)
    if blend_deps:
        return blend_deps
    
    # No dependencies found
    return []


def resolve_dependencies(feature_names: List[str], include_transitive: bool = True) -> Tuple[Set[str], Dict[str, Set[str]]]:
    """
    Resolve all dependencies for a list of features (transitive closure).
    
    Args:
        feature_names: List of feature names to resolve
        include_transitive: If True, include transitive dependencies (A -> B -> C, includes C)
        
    Returns:
        Tuple of:
        - Set of all features to regenerate (original + all dependencies)
        - Dict mapping each original feature to its direct dependencies
    """
    all_features = set(feature_names)
    dependency_map = {f: set() for f in feature_names}
    
    if not include_transitive:
        # Just get direct dependencies
        for feature in feature_names:
            deps = get_direct_dependencies(feature)
            dependency_map[feature] = set(deps)
            all_features.update(deps)
        return all_features, dependency_map
    
    # Transitive closure: keep resolving until no new dependencies found
    to_process = set(feature_names)
    processed = set()
    
    while to_process:
        current = to_process.pop()
        if current in processed:
            continue
        
        processed.add(current)
        deps = get_direct_dependencies(current)
        
        # Track direct dependencies for original features
        if current in feature_names:
            dependency_map[current].update(deps)
        
        # Add new dependencies to process
        for dep in deps:
            if dep not in processed and dep not in to_process:
                to_process.add(dep)
                all_features.add(dep)
    
    return all_features, dependency_map


def get_dependent_features(feature_name: str, all_features: List[str]) -> List[str]:
    """
    Get all features that depend on the given feature (reverse lookup).
    
    Args:
        feature_name: Feature name to check
        all_features: List of all available features
        
    Returns:
        List of features that depend on the given feature
    """
    dependents = []
    for feature in all_features:
        deps = get_direct_dependencies(feature)
        if feature_name in deps:
            dependents.append(feature)
    return dependents


def categorize_features(
    requested_features: List[str],
    all_features: Set[str]
) -> Dict[str, List[str]]:
    """
    Categorize features into requested vs. dependencies.
    
    Args:
        requested_features: Features explicitly requested for regeneration
        all_features: All features that will be regenerated (including dependencies)
        
    Returns:
        Dict with keys:
        - 'requested': List of requested features
        - 'dependencies': List of dependency features (not in requested)
        - 'all': List of all features (requested + dependencies)
    """
    requested_set = set(requested_features)
    all_set = set(all_features)
    
    dependencies = sorted(list(all_set - requested_set))
    
    return {
        'requested': sorted(list(requested_set)),
        'dependencies': dependencies,
        'all': sorted(list(all_set))
    }
