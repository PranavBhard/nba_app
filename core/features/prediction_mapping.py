"""
Prediction Feature Mapping - Maps registry format to internal column names.

Registry format: pred_margin|none|ridge|none
Internal column: pred_margin

This module handles validation and mapping between the two formats,
as well as model type validation against the selected points model.
"""

from typing import Tuple, Optional, Dict, List

# Registry format to internal column mapping
# Registry stat name -> CSV column name
PRED_FEATURE_MAP = {
    "pred_home": "pred_home_points",
    "pred_away": "pred_away_points",
    "pred_margin": "pred_margin",
    "pred_total": "pred_point_total",
}

# Internal column to registry stat name (reverse mapping)
INTERNAL_TO_REGISTRY = {v: k for k, v in PRED_FEATURE_MAP.items()}

# Legacy simple names that are accepted (for backward compatibility)
LEGACY_PRED_COLUMNS = {
    "pred_home_points",
    "pred_away_points",
    "pred_margin",
    "pred_point_total",
    "pred_total",  # Alias for pred_point_total
}

# Valid model types (must match VALID_CALC_WEIGHTS in registry)
VALID_MODEL_TYPES = {"ridge", "elasticnet", "randomforest", "xgboost"}


def parse_pred_feature(feature_name: str) -> Optional[Dict]:
    """
    Parse a prediction feature name.

    Args:
        feature_name: Either registry format (pred_margin|none|ridge|none)
                     or legacy format (pred_margin)

    Returns:
        Dict with keys: stat_name, model_type, internal_column, is_legacy
        or None if not a prediction feature
    """
    # Check legacy format first
    if feature_name in LEGACY_PRED_COLUMNS:
        # Map to internal column name
        if feature_name == "pred_total":
            internal_col = "pred_point_total"
            stat_name = "pred_total"
        elif feature_name in INTERNAL_TO_REGISTRY:
            internal_col = feature_name
            stat_name = INTERNAL_TO_REGISTRY[feature_name]
        else:
            internal_col = feature_name
            stat_name = feature_name

        return {
            "stat_name": stat_name,
            "model_type": None,  # Legacy format doesn't specify model type
            "internal_column": internal_col,
            "is_legacy": True,
        }

    # Check registry format (e.g., pred_margin|none|ridge|none)
    parts = feature_name.split("|")
    if len(parts) != 4:
        return None

    stat_name, time_period, calc_weight, perspective = parts

    # Must be a prediction stat
    if stat_name not in PRED_FEATURE_MAP:
        return None

    # Validate format
    if time_period != "none" or perspective != "none":
        return None

    # calc_weight should be a model type
    if calc_weight.lower() not in VALID_MODEL_TYPES:
        return None

    return {
        "stat_name": stat_name,
        "model_type": calc_weight.lower(),
        "internal_column": PRED_FEATURE_MAP[stat_name],
        "is_legacy": False,
    }


def is_pred_feature(feature_name: str) -> bool:
    """Check if feature is a prediction feature."""
    return parse_pred_feature(feature_name) is not None


def validate_pred_feature_model_type(
    feature_name: str, selected_model_type: str
) -> Tuple[bool, Optional[str]]:
    """
    Validate that the requested prediction feature model type matches
    the selected points model.

    Args:
        feature_name: Registry format prediction feature name
        selected_model_type: Model type from model_config_points_nba (e.g., 'Ridge')

    Returns:
        (is_valid, error_message)
    """
    parsed = parse_pred_feature(feature_name)
    if not parsed:
        return False, f"'{feature_name}' is not a valid prediction feature"

    # Legacy format doesn't require model type validation
    if parsed["is_legacy"]:
        return True, None

    requested_type = parsed["model_type"]
    selected_type = selected_model_type.lower()

    if requested_type != selected_type:
        # Suggest the correct feature name
        stat_name = parsed["stat_name"]
        suggested = f"{stat_name}|none|{selected_type}|none"
        return False, (
            f"Requested model type '{requested_type}' does not match selected points model "
            f"'{selected_model_type}'. Use '{suggested}' instead, or change the selected points model."
        )

    return True, None


def get_pred_internal_columns(feature_names: List[str]) -> List[str]:
    """
    Convert list of prediction features (registry or legacy format)
    to internal column names for CSV storage.

    Args:
        feature_names: List of prediction feature names

    Returns:
        List of unique internal column names
    """
    internal_cols = set()
    for feature in feature_names:
        parsed = parse_pred_feature(feature)
        if parsed:
            internal_cols.add(parsed["internal_column"])
    return list(internal_cols)


def get_registry_format(internal_column: str, model_type: str) -> Optional[str]:
    """
    Convert internal column name to registry format.

    Args:
        internal_column: Internal column name (e.g., 'pred_margin')
        model_type: Model type (e.g., 'Ridge')

    Returns:
        Registry format feature name (e.g., 'pred_margin|none|ridge|none')
        or None if not a valid prediction column
    """
    stat_name = INTERNAL_TO_REGISTRY.get(internal_column)
    if not stat_name:
        # Try direct mapping for pred_total alias
        if internal_column == "pred_total":
            stat_name = "pred_total"
        else:
            return None

    return f"{stat_name}|none|{model_type.lower()}|none"


def get_all_pred_features() -> List[str]:
    """
    Get all valid prediction feature names in registry format.

    Returns:
        List of all pred_* feature names (all stat + model type combinations)
    """
    features = []
    for stat_name in PRED_FEATURE_MAP.keys():
        for model_type in VALID_MODEL_TYPES:
            features.append(f"{stat_name}|none|{model_type}|none")
    return sorted(features)
