"""
Centralized Feature Management with standardized naming conventions and feature blocks.
Ensures consistent feature generation across all components.
"""

from typing import Dict, List, Set
import re


class FeatureManager:
    """Centralized feature management with standardized blocks and naming."""
    
    # Standardized feature blocks
    FEATURE_BLOCKS = {
        'basic': {
            'description': 'Basic team performance metrics',
            'features': [
                'off_rtg', 'def_rtg', 'pace', 'off_eff', 'def_eff',
                'off_rtg|season|avg', 'def_rtg|season|avg'
            ]
        },
        'advanced': {
            'description': 'Advanced analytics metrics',
            'features': [
                'off_rtg|season|avg', 'def_rtg|season|avg',
                'off_rtg|season|home', 'def_rtg|season|home',
                'off_rtg|season|away', 'def_rtg|season|away',
                'off_rtg|last5', 'def_rtg|last5',
                'off_rtg|last10', 'def_rtg|last10'
            ]
        },
        'per': {
            'description': 'Player Efficiency Rating features',
            'features': [
                'per_available', 'player_per', 'team_per', 'opp_per',
                'per_diff', 'per_ratio'
            ]
        },
        'travel': {
            'description': 'Travel and schedule-related features',
            'features': [
                'travel_days', 'back_to_back', 'time_zones', 'rest_days',
                'home_standings', 'away_standings', 'momentum'
            ]
        },
        'injury': {
            'description': 'Injury and roster status features',
            'features': [
                'injured_players', 'healthy_players', 'roster_stability',
                'key_player_injured', 'depth_impact'
            ]
        },
        'elo': {
            'description': 'ELO rating and power ranking features',
            'features': [
                'home_elo', 'away_elo', 'elo_diff', 'elo_change',
                'power_ranking', 'strength_of_schedule'
            ]
        },
        'temporal': {
            'description': 'Time-based and seasonal features',
            'features': [
                'month', 'day_of_week', 'season_progress',
                'days_since_last_game', 'back_to_back_days'
            ]
        }
    }
    
    @staticmethod
    def get_features(block_names: List[str], include_meta: bool = False) -> List[str]:
        """
        Generate feature list from block names.
        
        Args:
            block_names: List of feature block names (e.g., ['basic', 'per'])
            include_meta: Whether to include metadata columns
            
        Returns:
            List of feature names
        """
        features = []
        
        for block_name in block_names:
            if block_name in FeatureManager.FEATURE_BLOCKS:
                block_features = FeatureManager.FEATURE_BLOCKS[block_name]['features']
                features.extend(block_features)
            else:
                print(f"⚠️  Unknown feature block: {block_name}")
        
        # Remove duplicates while preserving order
        seen = set()
        unique_features = []
        for feature in features:
            if feature not in seen:
                seen.add(feature)
                unique_features.append(feature)
        
        if include_meta:
            unique_features.extend(['Year', 'Month', 'Day', 'Home', 'Away', 'game_id'])
        
        return unique_features
    
    @staticmethod
    def normalize_feature_names(features: List[str]) -> List[str]:
        """
        Convert feature names to standard format.
        
        Args:
            features: List of raw feature names
            
        Returns:
            List of normalized feature names
        """
        normalized = []
        
        for feature in features:
            # Handle common variations
            if feature in ['Year', 'Month', 'Day', 'Home', 'Away', 'game_id', 'home_points', 'away_points', 'HomeWon']:
                normalized.append(feature)
            elif '|' in feature:
                # Handle calculated features like 'off_rtg|season|avg'
                normalized.append(feature)
            elif feature.endswith('_pred'):
                # Handle prediction features
                normalized.append(feature)
            else:
                # Standardize basic features
                feature_lower = feature.lower()
                if feature_lower in ['offrtg', 'off_rating']:
                    normalized.append('off_rtg')
                elif feature_lower in ['defrtg', 'def_rating']:
                    normalized.append('def_rtg')
                elif feature_lower in ['pace']:
                    normalized.append('pace')
                elif feature_lower in ['offeff', 'offensive_efficiency']:
                    normalized.append('off_eff')
                elif feature_lower in ['defeff', 'defensive_efficiency']:
                    normalized.append('def_eff')
                else:
                    normalized.append(feature)
        
        return normalized
    
    @staticmethod
    def get_feature_blocks(features: List[str]) -> Dict[str, List[str]]:
        """
        Categorize features into blocks.
        
        Args:
            features: List of feature names
            
        Returns:
            Dictionary mapping block names to feature lists
        """
        categorized = {block: [] for block in FeatureManager.FEATURE_BLOCKS}
        
        for feature in features:
            placed = False
            
            for block_name, block_info in FeatureManager.FEATURE_BLOCKS.items():
                if feature in block_info['features']:
                    categorized[block_name].append(feature)
                    placed = True
                    break
            
            if not placed:
                categorized['other'] = categorized.get('other', [])
                categorized['other'].append(feature)
        
        # Remove empty blocks
        return {k: v for k, v in categorized.items() if v}
    
    @staticmethod
    def validate_features(features: List[str]) -> Dict[str, any]:
        """
        Validate feature names and return validation results.
        
        Args:
            features: List of feature names to validate
            
        Returns:
            Dictionary with validation results
        """
        validation = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'unknown_features': [],
            'blocks_found': set()
        }
        
        # Check each feature
        for feature in features:
            known_feature = False
            
            # Check against all feature blocks
            for block_name, block_info in FeatureManager.FEATURE_BLOCKS.items():
                if feature in block_info['features']:
                    known_feature = True
                    validation['blocks_found'].add(block_name)
                    break
            
            # Check for calculated features
            if '|' in feature or feature.endswith('_pred'):
                known_feature = True
            
            # Check for meta features
            if feature in ['Year', 'Month', 'Day', 'Home', 'Away', 'game_id', 'home_points', 'away_points', 'HomeWon']:
                known_feature = True
            
            if not known_feature:
                validation['unknown_features'].append(feature)
                validation['valid'] = False
                validation['errors'].append(f"Unknown feature: {feature}")
        
        # Add warnings
        if validation['unknown_features']:
            validation['warnings'].append(f"Found {len(validation['unknown_features'])} unknown features")
        
        return validation
    
    @staticmethod
    def get_feature_description(feature: str) -> str:
        """
        Get description of a feature.
        
        Args:
            feature: Feature name
            
        Returns:
            Description string
        """
        for block_name, block_info in FeatureManager.FEATURE_BLOCKS.items():
            if feature in block_info['features']:
                return f"{block_info['description']}: {feature}"
        
        # Handle special cases
        if '|' in feature:
            return f"Calculated feature: {feature}"
        elif feature.endswith('_pred'):
            return f"Prediction feature: {feature}"
        elif feature in ['Year', 'Month', 'Day', 'Home', 'Away', 'game_id']:
            return f"Metadata feature: {feature}"
        
        return f"Unknown feature: {feature}"
    
    @staticmethod
    def generate_feature_set_hash(features: List[str]) -> str:
        """
        Generate hash for feature set identification.
        
        Args:
            features: List of feature names
            
        Returns:
            MD5 hash string
        """
        import hashlib
        
        # Sort features for consistent hashing
        sorted_features = sorted(features)
        feature_str = '|'.join(sorted_features)
        
        return hashlib.md5(feature_str.encode()).hexdigest()
    
    @staticmethod
    def get_default_features() -> List[str]:
        """
        Get default feature set for basic models.
        
        Returns:
            List of default feature names
        """
        return FeatureManager.get_features(['basic'], include_meta=False)
    
    @staticmethod
    def get_advanced_features() -> List[str]:
        """
        Get advanced feature set.
        
        Returns:
            List of advanced feature names
        """
        return FeatureManager.get_features(['basic', 'advanced'], include_meta=False)
    
    @staticmethod
    def get_all_features() -> List[str]:
        """
        Get all available features.
        
        Returns:
            List of all feature names
        """
        all_features = []
        for block_info in FeatureManager.FEATURE_BLOCKS.values():
            all_features.extend(block_info['features'])
        
        return FeatureManager.normalize_feature_names(all_features)
    
    @staticmethod
    def get_block_info(block_name: str) -> Dict:
        """
        Get information about a feature block.
        
        Args:
            block_name: Name of feature block
            
        Returns:
            Dictionary with block information
        """
        return FeatureManager.FEATURE_BLOCKS.get(block_name, {
            'description': 'Unknown block',
            'features': []
        })
