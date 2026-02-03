from __future__ import annotations

import json
import os
import pickle
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from nba_app.core.services.prediction import PredictionService


def _json_safe(obj: Any) -> Any:
    """
    Convert Mongo/Python objects into JSON-serializable structures.
    Keep this conservative and lightweight (strings for unknown types).
    """
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {str(k): _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_json_safe(v) for v in obj]

    # ObjectId and other types: stringify
    try:
        # Some objects (like ObjectId) stringify cleanly
        return str(obj)
    except Exception:
        return json.dumps(obj, default=str)


def _deep_get(obj: Any, path: str) -> Any:
    """
    Safe nested getter supporting dotted paths, e.g. "output.features_dict._ensemble_breakdown.base_models".
    Returns None if any segment is missing.
    """
    cur = obj
    for key in path.split("."):
        if cur is None:
            return None
        if isinstance(cur, dict):
            cur = cur.get(key)
        else:
            return None
    return cur


def get_selected_configs(*, db, league=None) -> Dict[str, Any]:
    """
    Return currently selected classifier + points configs (if any).
    """
    service = PredictionService(db=db, league=league)
    cfgs = service.get_selected_configs() or {}
    return _json_safe(cfgs)


def get_prediction_doc(game_id: str, *, db, league=None) -> Dict[str, Any]:
    """
    Return the ensemble base model breakdown (for ensembles) or model info (for single models).

    For ensembles: Returns `whole_doc.output.features_dict._ensemble_breakdown.base_models`
    For single models: Returns model metadata and summary info.
    """
    service = PredictionService(db=db, league=league)
    doc = service.get_prediction_for_game(game_id) or {}
    base_models = _deep_get(doc, "output.features_dict._ensemble_breakdown.base_models")
    if base_models is None:
        # Backward-compat: some docs may store features_dict at top-level
        base_models = _deep_get(doc, "features_dict._ensemble_breakdown.base_models")

    if base_models is not None:
        return _json_safe(base_models)

    # Not an ensemble - return single model info
    p_home = doc.get("home_win_prob")
    if p_home is not None:
        p_home = p_home / 100.0  # Convert from percentage
    else:
        p_home = _deep_get(doc, "output.p_home") or doc.get("p_home")

    return _json_safe({
        "is_ensemble": False,
        "game_id": game_id,
        "p_home": round(p_home, 4) if p_home is not None else None,
        "home_team": doc.get("home_team"),
        "away_team": doc.get("away_team"),
        "predicted_winner": doc.get("predicted_winner"),
        "predicted_at": doc.get("predicted_at"),
        "_note": "This prediction used a single model, not an ensemble. Use get_base_model_direction_table for detailed model info.",
    })


def get_prediction_feature_values(
    game_id: str,
    *,
    keys: Optional[List[str]] = None,
    db,
    league=None,
) -> Dict[str, Any]:
    """
    Return prediction feature values (features_dict) for this game.
    If keys is provided, return only those keys (missing keys included as None).
    """
    service = PredictionService(db=db, league=league)
    doc = service.get_prediction_for_game(game_id) or {}
    # Prediction docs may store features under output.features_dict (SSoT),
    # with backward-compat variants at the top-level.
    feats = doc.get("features_dict")
    if not isinstance(feats, dict):
        feats = _deep_get(doc, "output.features_dict")
    if not isinstance(feats, dict):
        feats = {}

    if not keys:
        return _json_safe(feats)

    # If the requested keys aren't present at the top-level features_dict,
    # they may exist inside the per-base-model breakdown.
    base_models = _deep_get(doc, "output.features_dict._ensemble_breakdown.base_models")
    if base_models is None:
        base_models = _deep_get(doc, "features_dict._ensemble_breakdown.base_models")

    out: Dict[str, Any] = {}
    for k in keys:
        if k in feats:
            out[k] = _json_safe(feats.get(k))
            continue

        # Search within base models (if available)
        matches: List[Dict[str, Any]] = []
        if isinstance(base_models, list):
            for bm in base_models:
                if not isinstance(bm, dict):
                    continue
                bm_name = bm.get("name") or bm.get("config_id_short") or bm.get("config_id") or "base_model"
                bm_feats = bm.get("features_dict") or {}
                if isinstance(bm_feats, dict) and k in bm_feats:
                    matches.append({"base_model": str(bm_name), "value": _json_safe(bm_feats.get(k))})

        if not matches:
            out[k] = None
        elif len(matches) == 1:
            out[k] = matches[0]["value"]
        else:
            # Rare: same key appears in multiple base models; return disambiguated list.
            out[k] = matches

    return out


def get_prediction_base_outputs(game_id: str, *, db, league=None) -> Dict[str, Any]:
    """
    Return the meta feature values for the ensemble meta-model (for ensembles)
    or key feature values (for single models).

    For ensembles: Returns `same_doc.output.features_dict._ensemble_breakdown.meta_feature_values`
    For single models: Returns a selection of key features from the prediction.
    """
    service = PredictionService(db=db, league=league)
    doc = service.get_prediction_for_game(game_id) or {}
    meta_vals = _deep_get(doc, "output.features_dict._ensemble_breakdown.meta_feature_values")
    if meta_vals is None:
        meta_vals = _deep_get(doc, "features_dict._ensemble_breakdown.meta_feature_values")

    if meta_vals is not None:
        return _json_safe(meta_vals)

    # Not an ensemble - return key features from the prediction
    features_dict = doc.get("features_dict")
    if not isinstance(features_dict, dict):
        features_dict = _deep_get(doc, "output.features_dict") or {}

    # Filter to key predictive features (exclude internal keys)
    key_features: Dict[str, Any] = {}
    for k, v in features_dict.items():
        if k.startswith("_"):
            continue
        if isinstance(v, (int, float)):
            key_features[k] = round(float(v), 4)
        else:
            key_features[k] = v

    return _json_safe({
        "is_ensemble": False,
        "game_id": game_id,
        "features": key_features,
        "feature_count": len(key_features),
        "_note": "This prediction used a single model. These are the raw feature values used for prediction.",
    })


# Base model display names
_BASE_MODEL_DISPLAY_NAMES = {
    "B1": "Season Strength",
    "B2": "Recent Form",
    "B3": "Rest & Travel",
    "B4": "Player Talent",
    "B5": "Injuries",
    "B6": "Head-to-Head",
}


def _extract_base_model_id(key: str) -> Optional[str]:
    """
    Extract base model ID (B1, B2, ..., B6) from a meta_feature_values key.

    Key formats observed:
    - p_B1__TEAM_SEAS_HOME_AWAY__GB_MIN20_SIGT10C2123E24
    - p_B4__PLYR_TALENT_HOME_AWAY__GB_MIN20_SIGT10C2123E24
    - p_B6V2__H2H_HOME_AWAY__GB_MIN20_SIGT10C2123E24
    - pred_margin (not a base model)
    """
    import re

    # Look for p_B{N} or p_B{N}V{M} pattern at the start
    match = re.match(r'^p_B(\d+)(V\d+)?__', key)
    if match:
        base_num = match.group(1)  # e.g., "1", "2", "6"
        return f"B{base_num}"

    # Also try to find _B{N}_ pattern anywhere in the key (fallback)
    match = re.search(r'_B(\d+)(V\d+)?_', key)
    if match:
        base_num = match.group(1)
        return f"B{base_num}"

    return None


def _get_single_model_info(game_id: str, doc: Dict[str, Any], *, db, league=None) -> Dict[str, Any]:
    """
    Get model info for a single (non-ensemble) model prediction.

    Returns model metadata and ALL feature details (importances/coefficients + values).
    """
    service = PredictionService(db=db, league=league)

    # Get p_home from prediction
    p_home = None
    output = doc.get("output") or {}
    if isinstance(output, dict):
        p_home = output.get("p_home")
    if p_home is None:
        p_home = doc.get("p_home")
    if p_home is None:
        p_home = doc.get("home_win_prob")
        if p_home is not None:
            p_home = p_home / 100.0  # Convert from percentage

    # Compute model direction
    model_favors = "NEUTRAL"
    if p_home is not None:
        if p_home > 0.50:
            model_favors = "HOME"
        elif p_home < 0.50:
            model_favors = "AWAY"

    # Get features_dict
    features_dict = doc.get("features_dict")
    if not isinstance(features_dict, dict):
        features_dict = _deep_get(doc, "output.features_dict") or {}

    # Try to get model config info
    model_info: Dict[str, Any] = {
        "is_ensemble": False,
        "model_type": None,
        "config_name": None,
        "feature_count": None,
        "created_at": None,
    }

    # Feature table - ALL features with their details
    feature_table: List[Dict[str, Any]] = []

    # Get selected config to find model details
    try:
        cfgs = service.get_selected_configs() or {}
        classifier_cfg = cfgs.get("classifier") if isinstance(cfgs, dict) else None
        if isinstance(classifier_cfg, dict):
            model_info["model_type"] = classifier_cfg.get("model_type")
            model_info["config_name"] = classifier_cfg.get("name") or classifier_cfg.get("config_name")
            model_info["created_at"] = classifier_cfg.get("created_at") or classifier_cfg.get("artifacts_saved_at")
            model_info["feature_set"] = classifier_cfg.get("feature_set")
            model_info["training_csv"] = classifier_cfg.get("training_csv")

            # Get feature names from config
            feature_names = classifier_cfg.get("feature_names") or []
            if not feature_names:
                features_path = classifier_cfg.get("features_path")
                if features_path and os.path.exists(features_path):
                    try:
                        with open(features_path, "r") as f:
                            feature_names = json.load(f)
                    except Exception:
                        pass
            model_info["feature_count"] = len(feature_names) if feature_names else None

            # Try to load feature importances from the model
            model_path = classifier_cfg.get("model_artifact_path")
            if model_path and os.path.exists(model_path):
                try:
                    with open(model_path, "rb") as f:
                        model = pickle.load(f)

                    # Get feature importances (tree-based models)
                    if hasattr(model, "feature_importances_"):
                        importances = model.feature_importances_
                        if feature_names and len(feature_names) == len(importances):
                            # Sort by importance descending - include ALL features
                            sorted_pairs = sorted(
                                zip(feature_names, importances),
                                key=lambda x: abs(x[1]),
                                reverse=True
                            )
                            for fname, imp in sorted_pairs:
                                feat_val = features_dict.get(fname)
                                feature_table.append({
                                    "feature": fname,
                                    "importance": round(float(imp), 4),
                                    "importance_pct": f"{float(imp) * 100:.1f}%",
                                    "value": round(float(feat_val), 4) if isinstance(feat_val, (int, float)) else feat_val,
                                })
                            model_info["has_feature_importance"] = True

                    # Get coefficients (linear models)
                    elif hasattr(model, "coef_"):
                        coefs = model.coef_
                        try:
                            flat_coefs = list(coefs.reshape(-1))
                        except Exception:
                            flat_coefs = list(coefs[0]) if isinstance(coefs, (list, tuple)) else []

                        if feature_names and len(feature_names) == len(flat_coefs):
                            # Sort by absolute coefficient value descending - include ALL features
                            sorted_pairs = sorted(
                                zip(feature_names, flat_coefs),
                                key=lambda x: abs(x[1]),
                                reverse=True
                            )
                            for fname, coef in sorted_pairs:
                                feat_val = features_dict.get(fname)
                                # For logistic regression, positive coef = increases home win prob
                                direction = "HOME" if coef > 0 else "AWAY"
                                feature_table.append({
                                    "feature": fname,
                                    "coefficient": round(float(coef), 4),
                                    "direction": direction,
                                    "value": round(float(feat_val), 4) if isinstance(feat_val, (int, float)) else feat_val,
                                })
                            model_info["has_coefficients"] = True

                    model_info["model_class"] = type(model).__name__
                except Exception as e:
                    model_info["_model_load_error"] = str(e)
    except Exception as e:
        model_info["_config_error"] = str(e)

    # If we couldn't load importances/coefficients, still include all feature values
    if not feature_table:
        for k, v in features_dict.items():
            if k.startswith("_"):  # Skip internal keys
                continue
            feature_table.append({
                "feature": k,
                "value": round(float(v), 4) if isinstance(v, (int, float)) else v,
            })
        # Sort alphabetically if no importance info
        feature_table.sort(key=lambda x: x["feature"])

    return _json_safe({
        "game_id": game_id,
        "p_home": round(p_home, 4) if p_home is not None else None,
        "model_favors": model_favors,
        "model_info": model_info,
        "feature_table": feature_table,
        "_interpretation_rule": "p_home > 0.50 = HOME favored, p_home < 0.50 = AWAY favored. For coefficients: positive = favors HOME, negative = favors AWAY.",
        "_note": "This is a single model (not an ensemble). Features are sorted by importance/coefficient magnitude.",
    })


def get_base_model_direction_table(game_id: str, *, db, league=None) -> Dict[str, Any]:
    """
    Return a pre-computed direction table for all base models (ensembles)
    or model info with top features (single models).

    This tool removes the interpretation burden from the agent by computing
    the direction (HOME vs AWAY) for each base model output.

    RULE: output > 0.50 = HOME, output < 0.50 = AWAY, output = 0.50 = NEUTRAL

    For ensembles, returns:
        {
            "game_id": "...",
            "p_home": 0.471,
            "is_ensemble": true,
            "ensemble_favors": "AWAY",
            "direction_table": [
                {
                    "base_model": "B1",
                    "name": "Season Strength",
                    "output": 0.514,
                    "favors": "HOME",
                    "magnitude": 0.014,
                    "magnitude_pct": "1.4%"
                },
                ...
            ],
            "summary": {
                "home_count": 3,
                "away_count": 3,
                "neutral_count": 0
            }
        }

    For single models, returns:
        {
            "game_id": "...",
            "p_home": 0.53,
            "model_favors": "HOME",
            "model_info": {
                "is_ensemble": false,
                "model_type": "GradientBoosting",
                "config_name": "My Model",
                "feature_count": 42,
                "has_feature_importance": true
            },
            "feature_table": [
                {"feature": "elo_diff", "importance": 0.15, "importance_pct": "15.0%", "value": 45.2},
                {"feature": "win_pct_home", "importance": 0.12, "importance_pct": "12.0%", "value": 0.65},
                ... (ALL features, sorted by importance)
            ]
        }
    """
    service = PredictionService(db=db, league=league)
    doc = service.get_prediction_for_game(game_id) or {}

    # Check if this is an ensemble prediction by looking for ensemble breakdown
    meta_vals = _deep_get(doc, "output.features_dict._ensemble_breakdown.meta_feature_values")
    if meta_vals is None:
        meta_vals = _deep_get(doc, "features_dict._ensemble_breakdown.meta_feature_values")

    # If no ensemble breakdown, this is a single model - return single model info
    if not isinstance(meta_vals, dict) or not meta_vals:
        return _get_single_model_info(game_id, doc, db=db, league=league)

    # ----- Ensemble model path -----

    # Get p_home from prediction
    p_home = None
    output = doc.get("output") or {}
    if isinstance(output, dict):
        p_home = output.get("p_home")
    if p_home is None:
        p_home = doc.get("p_home")

    direction_table = []
    home_count = 0
    away_count = 0
    neutral_count = 0

    # Parse base model outputs
    for key, value in meta_vals.items():
        if not isinstance(value, (int, float)):
            continue

        # Extract base model ID using regex
        base_id = _extract_base_model_id(key)

        if base_id is None:
            # Skip non-base-model values (like pred_margin)
            if "pred_margin" in key.lower():
                continue
            # Unknown key format - skip it
            continue

        # Compute direction
        if value > 0.50:
            favors = "HOME"
            home_count += 1
        elif value < 0.50:
            favors = "AWAY"
            away_count += 1
        else:
            favors = "NEUTRAL"
            neutral_count += 1

        magnitude = abs(value - 0.50)
        magnitude_pct = f"{magnitude * 100:.1f}%"

        name = _BASE_MODEL_DISPLAY_NAMES.get(base_id, f"Base Model {base_id}")

        direction_table.append({
            "base_model": base_id,
            "name": name,
            "output": round(value, 4),
            "favors": favors,
            "magnitude": round(magnitude, 4),
            "magnitude_pct": magnitude_pct,
            "key": key,  # Include original key for debugging
        })

    # Sort by base model number (B1, B2, ..., B6)
    def sort_key(x):
        bm = x["base_model"]
        if bm.startswith("B") and bm[1:].isdigit():
            return int(bm[1:])
        return 99  # Unknown at end

    direction_table.sort(key=sort_key)

    # Compute ensemble direction
    ensemble_favors = "NEUTRAL"
    if p_home is not None:
        if p_home > 0.50:
            ensemble_favors = "HOME"
        elif p_home < 0.50:
            ensemble_favors = "AWAY"

    return _json_safe({
        "game_id": game_id,
        "p_home": round(p_home, 4) if p_home is not None else None,
        "is_ensemble": True,
        "ensemble_favors": ensemble_favors,
        "direction_table": direction_table,
        "summary": {
            "home_count": home_count,
            "away_count": away_count,
            "neutral_count": neutral_count,
        },
        "_interpretation_rule": "output > 0.50 = HOME, output < 0.50 = AWAY",
    })


def get_prediction_snapshot(snapshot_id: str, *, db, league=None) -> Dict[str, Any]:
    """
    Load an immutable prediction scenario snapshot by snapshot_id.

    Snapshots are created by the experimenter to enable before/after
    analysis without relying on the upserted-by-game_id predictions doc.
    """
    scenarios_coll = "nba_prediction_scenarios"
    if league is not None and getattr(league, "collections", None):
        scenarios_coll = league.collections.get("prediction_scenarios", scenarios_coll)
    doc = db[scenarios_coll].find_one({"snapshot_id": str(snapshot_id)}) or {}
    doc.pop("_id", None)
    return _json_safe(doc) if doc else {}


def get_prediction_snapshot_doc(snapshot_id: str, *, db, league=None) -> Dict[str, Any]:
    """
    Return the ensemble base model breakdown for a snapshot:
    `prediction_doc.output.features_dict._ensemble_breakdown.base_models`
    """
    snap = get_prediction_snapshot(snapshot_id, db=db, league=league) or {}
    pred = snap.get("prediction_doc") if isinstance(snap, dict) else None
    base_models = _deep_get(pred, "output.features_dict._ensemble_breakdown.base_models")
    if base_models is None:
        base_models = _deep_get(pred, "features_dict._ensemble_breakdown.base_models")
    return _json_safe(base_models) if base_models is not None else {}


def get_prediction_snapshot_base_outputs(snapshot_id: str, *, db, league=None) -> Dict[str, Any]:
    """
    Return meta_feature_values for a snapshot:
    `prediction_doc.output.features_dict._ensemble_breakdown.meta_feature_values`
    """
    snap = get_prediction_snapshot(snapshot_id, db=db, league=league) or {}
    pred = snap.get("prediction_doc") if isinstance(snap, dict) else None
    meta = _deep_get(pred, "output.features_dict._ensemble_breakdown.meta_feature_values")
    if meta is None:
        meta = _deep_get(pred, "features_dict._ensemble_breakdown.meta_feature_values")
    return _json_safe(meta) if meta is not None else {}


def get_ensemble_meta_model_params(game_id: str, *, db, league=None) -> Dict[str, Any]:
    """
    Return the ensemble meta-model parameters needed for contribution analysis.

    For ensembles, loads:
    - `cli/models/ensembles/{run_id}_ensemble_config.json` (meta_feature_cols ordering + model type)
    - `cli/models/ensembles/{run_id}_meta_model.pkl` (sklearn meta-model; coefficients/intercept when available)

    Returns a JSON-safe dict:
      {
        ensemble_run_id,
        meta_model_type,
        meta_feature_cols: [...],
        intercept,
        coefficients: {feature_name: coef, ...},
      }

    For single models, returns model info with coefficients/importances if available.
    """
    service = PredictionService(db=db, league=league)
    doc = service.get_prediction_for_game(game_id) or {}

    # Check if this is an ensemble by looking for ensemble breakdown
    has_ensemble_breakdown = (
        _deep_get(doc, "output.features_dict._ensemble_breakdown") is not None
        or _deep_get(doc, "features_dict._ensemble_breakdown") is not None
    )

    features = doc.get("features_dict")
    if not isinstance(features, dict):
        features = _deep_get(doc, "output.features_dict")
    if not isinstance(features, dict):
        features = {}

    run_id = features.get("_ensemble_run_id")
    if not run_id and isinstance(features.get("_ensemble_breakdown"), dict):
        eb = features.get("_ensemble_breakdown") or {}
        run_id = eb.get("ensemble_run_id") or eb.get("run_id") or eb.get("_ensemble_run_id")

    # Fallback: selected ensemble config's run id (may differ from stored prediction)
    if not run_id:
        try:
            cfgs = service.get_selected_configs() or {}
            clf = cfgs.get("classifier") if isinstance(cfgs, dict) else None
            if isinstance(clf, dict):
                run_id = clf.get("ensemble_run_id")
        except Exception:
            run_id = None

    # If no run_id and no ensemble breakdown, this is a single model
    if not run_id and not has_ensemble_breakdown:
        # Return single model info instead
        try:
            cfgs = service.get_selected_configs() or {}
            clf = cfgs.get("classifier") if isinstance(cfgs, dict) else None
            if isinstance(clf, dict):
                model_type = clf.get("model_type", "Unknown")
                config_name = clf.get("name") or clf.get("config_name")
                model_path = clf.get("model_artifact_path")
                features_path = clf.get("features_path")

                result: Dict[str, Any] = {
                    "is_ensemble": False,
                    "game_id": game_id,
                    "model_type": model_type,
                    "config_name": config_name,
                }

                # Try to load model params
                if model_path and os.path.exists(model_path):
                    try:
                        with open(model_path, "rb") as f:
                            model = pickle.load(f)

                        result["model_class"] = type(model).__name__

                        # Load feature names
                        feature_names: List[str] = []
                        if features_path and os.path.exists(features_path):
                            with open(features_path, "r") as f:
                                feature_names = json.load(f)
                        result["feature_count"] = len(feature_names)

                        # Get coefficients (linear models)
                        if hasattr(model, "coef_"):
                            coefs = model.coef_
                            try:
                                flat = list(coefs.reshape(-1))
                            except Exception:
                                flat = list(coefs[0]) if isinstance(coefs, (list, tuple)) else []

                            if hasattr(model, "intercept_"):
                                try:
                                    itc = model.intercept_
                                    result["intercept"] = float(itc.reshape(-1)[0])
                                except Exception:
                                    pass

                            if feature_names and len(feature_names) == len(flat):
                                result["coefficients"] = {
                                    feature_names[i]: round(float(flat[i]), 6)
                                    for i in range(len(feature_names))
                                }

                        # Get feature importances (tree-based models)
                        elif hasattr(model, "feature_importances_"):
                            importances = model.feature_importances_
                            if feature_names and len(feature_names) == len(importances):
                                result["feature_importances"] = {
                                    feature_names[i]: round(float(importances[i]), 6)
                                    for i in range(len(feature_names))
                                }

                    except Exception as e:
                        result["_model_load_error"] = str(e)

                result["_note"] = "This prediction used a single model, not an ensemble."
                return _json_safe(result)
        except Exception as e:
            return {
                "is_ensemble": False,
                "game_id": game_id,
                "error": "failed_to_load_single_model_info",
                "exception": str(e),
            }

    if not run_id:
        return {"error": "missing_ensemble_run_id", "game_id": game_id}

    nba_app_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ensembles_dir = os.path.join(nba_app_path, "cli", "models", "ensembles")
    config_path = os.path.join(ensembles_dir, f"{run_id}_ensemble_config.json")
    model_path = os.path.join(ensembles_dir, f"{run_id}_meta_model.pkl")

    meta_feature_cols: List[str] = []
    meta_model_type: str = ""
    try:
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = json.load(f) or {}
            if isinstance(cfg, dict):
                meta_feature_cols = cfg.get("meta_feature_cols") or []
                meta_model_type = cfg.get("meta_model_type") or cfg.get("model_type") or ""
    except Exception:
        pass

    intercept = None
    coef_map: Dict[str, float] = {}

    if not os.path.exists(model_path):
        return {
            "ensemble_run_id": str(run_id),
            "meta_model_type": meta_model_type or "",
            "meta_feature_cols": meta_feature_cols,
            "error": "meta_model_file_not_found",
            "meta_model_path": model_path,
        }

    try:
        with open(model_path, "rb") as f:
            meta_model = pickle.load(f)

        # Try to recover coefficient-based attribution (LR / linear models)
        if hasattr(meta_model, "coef_"):
            coefs = getattr(meta_model, "coef_", None)
            try:
                # sklearn LR stores shape (1, n_features)
                flat = list(coefs.reshape(-1))  # type: ignore[attr-defined]
            except Exception:
                flat = list(coefs[0]) if isinstance(coefs, (list, tuple)) and coefs else []

            if hasattr(meta_model, "intercept_"):
                try:
                    itc = getattr(meta_model, "intercept_", None)
                    intercept = float(itc.reshape(-1)[0])  # type: ignore[attr-defined]
                except Exception:
                    try:
                        intercept = float(getattr(meta_model, "intercept_")[0])
                    except Exception:
                        intercept = None

            # Prefer meta_feature_cols ordering from config json; else fallback to model feature_names_in_
            names: List[str] = []
            if meta_feature_cols:
                names = [str(x) for x in meta_feature_cols]
            elif hasattr(meta_model, "feature_names_in_"):
                try:
                    names = [str(x) for x in list(getattr(meta_model, "feature_names_in_"))]
                except Exception:
                    names = []

            if names and flat and len(names) == len(flat):
                coef_map = {names[i]: float(flat[i]) for i in range(len(names))}
            else:
                # As a last resort, return the raw coef vector
                coef_map = {"_raw_coef": _json_safe(flat)}

        meta_model_type = meta_model_type or meta_model.__class__.__name__
    except Exception as e:
        return {
            "ensemble_run_id": str(run_id),
            "meta_model_type": meta_model_type or "",
            "meta_feature_cols": meta_feature_cols,
            "error": "failed_to_load_meta_model",
            "exception": str(e),
        }

    return _json_safe(
        {
            "ensemble_run_id": str(run_id),
            "meta_model_type": meta_model_type,
            "meta_feature_cols": meta_feature_cols,
            "intercept": intercept,
            "coefficients": coef_map,
        }
    )
