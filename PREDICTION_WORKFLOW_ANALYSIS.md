# Prediction Workflow Analysis

## Overview

This document analyzes the prediction workflows across 4 interfaces to identify code divergence and duplication.

---

## Workflow Comparison Matrix

| Aspect | game_list UI | game_detail UI | Agent Tooling | CLI |
|--------|-------------|----------------|---------------|-----|
| **Entry Point** | `POST /api/predict-all` | `POST /api/predict` | `matchup_predict.predict()` | `train.py predict` |
| **Config Source** | MongoDB selected | MongoDB selected | MongoDB selected | MongoDB OR CSV |
| **Model Loading** | `ModelFactory` | `ModelFactory` | `load_model_from_config()` | Train from CSV |
| **Feature Building** | `_build_features_dict()` | `_build_features_dict()` | `_build_features_dict()` | `_build_features_dict()` |
| **Core Predict Fn** | `predict_with_player_config()` | `predict_with_player_config()` | `predict_with_player_config()` | `predict()` (different!) |
| **Player Filtering** | Default rosters | `player_config` param | `player_filters` param | `--exclude-players` arg |
| **Points Model** | Optional | Yes (if selected) | Yes (if selected) | Optional |
| **Matchup Source** | ESPN API | Request params | Request params | ESPN API |
| **Output** | JSON → UI refresh | JSON → UI refresh | Dict return | Console + file |

---

## Code Path Diagrams

### 1. game_list UI (`/api/predict-all`)

```
web/app.py:predict_all()
    │
    ├─ get_scoreboard(date) → matchups from ESPN
    │
    ├─ db.model_config_nba.find_one({'selected': True})
    │
    ├─ ModelFactory.create_model(config) → (model, scaler, features)
    │
    └─ FOR EACH game:
        │
        └─ model.predict_with_player_config(
               home, away, season, date,
               player_filters=None,  ← DEFAULT ROSTERS
               additional_features=None
           )
           │
           ├─ _build_features_dict()
           │   └─ stat_handler.calculate_feature() × N
           │
           ├─ scaler.transform(X)
           │
           └─ model.predict_proba(X)
```

**Location:** `web/app.py` lines 4049+

---

### 2. game_detail UI (`/api/predict`)

```
web/app.py:predict()
    │
    ├─ Parse request: game_id, date, home, away, player_config
    │
    ├─ db.model_config_nba.find_one({'selected': True})
    ├─ db.model_config_points_nba.find_one({'selected': True})
    │
    ├─ build_player_lists_for_prediction() → player_filters
    │   └─ Uses player_config from request (injuries/starters)
    │
    ├─ IF points_config:
    │   └─ PointsRegressionTrainer.predict() → pred_margin
    │
    └─ model.predict_with_player_config(
           home, away, season, date,
           player_filters=player_filters,  ← CUSTOM ROSTERS
           additional_features={'pred_margin': ...}
       )
       │
       ├─ _build_features_dict()
       │   ├─ stat_handler.calculate_feature() × N
       │   ├─ per_calculator.get_per_features(player_filters)
       │   └─ stat_handler.get_injury_features()
       │
       ├─ scaler.transform(X)
       │
       └─ model.predict_proba(X)
```

**Location:** `web/app.py` lines 2814+

---

### 3. Agent Tooling (`matchup_predict.predict()`)

```
agents/tools/matchup_predict.py:predict()
    │
    ├─ Parse params: home, away, game_id, date, injuries, starters
    │
    ├─ db.model_config_nba.find_one({'selected': True})
    ├─ db.model_config_points_nba.find_one({'selected': True})
    │
    ├─ load_model_from_config(config)  ← CUSTOM LOADER
    │   └─ ModelFactory.create_model() OR ensemble setup
    │
    ├─ build_player_lists_for_prediction() → player_filters
    │   └─ Uses injuries/starters params
    │
    ├─ IF points_config:
    │   ├─ load_points_model(config)  ← CUSTOM LOADER
    │   └─ points_trainer.predict() → pred_margin
    │
    └─ model.predict_with_player_config(
           home, away, season, date,
           player_filters=player_filters,
           additional_features={'pred_margin': ...}
       )
       │
       └─ (same as game_detail)
```

**Location:** `agents/tools/matchup_predict.py` lines 200-419

---

### 4. CLI (`train.py predict`)

```
cli/train.py:predict_mode(args)
    │
    ├─ Parse args: --date, --model-type, --c-value, --exclude-players
    │
    ├─ db.model_config_nba.find_one({'selected': True})
    │   └─ OR: get_latest_training_csv()  ← FALLBACK
    │
    ├─ load_model_cache() → cached model info
    │
    ├─ read_csv_safe(csv_path) → training data
    │
    ├─ scaler = StandardScaler().fit_transform(X)  ← RETRAIN!
    │
    ├─ classifier = create_model_with_c().fit(X, y)  ← RETRAIN!
    │
    ├─ nba_model.classifier_model = classifier
    │   nba_model.scaler = scaler
    │   nba_model.feature_names = features
    │
    └─ nba_model.predict(date)  ← DIFFERENT METHOD!
       │
       ├─ get_matchups_with_venue(date)  ← ESPN API
       │
       └─ FOR EACH matchup:
           │
           ├─ _build_features_dict()
           │   ├─ stat_handler.calculate_feature() × N
           │   ├─ _get_per_features(exclude=args.exclude_players)
           │   └─ stat_handler.get_injury_features()
           │
           ├─ scaler.transform(X)
           │
           └─ model.predict_proba(X)
```

**Location:** `cli/train.py` lines 795-1075

---

## Key Divergence Points

### 1. Model Loading Strategy

| Interface | Strategy | Problem |
|-----------|----------|---------|
| game_list | `ModelFactory.create_model()` | ✓ Uses artifacts |
| game_detail | `ModelFactory.create_model()` | ✓ Uses artifacts |
| Agent | `load_model_from_config()` → `ModelFactory` | ✓ Uses artifacts |
| **CLI** | **Retrains from CSV every time** | ❌ Inconsistent, slow |

**Issue:** CLI retrains the model from scratch on every predict call instead of loading saved artifacts.

---

### 2. Core Prediction Method

| Interface | Method | Signature |
|-----------|--------|-----------|
| game_list | `predict_with_player_config()` | `(home, away, season, date, player_filters, additional_features)` |
| game_detail | `predict_with_player_config()` | Same |
| Agent | `predict_with_player_config()` | Same |
| **CLI** | **`predict()`** | `(date)` - loops internally |

**Issue:** CLI uses a completely different method that:
- Fetches matchups internally (others receive them as params)
- Uses `--exclude-players` arg instead of `player_filters` dict
- Doesn't support `additional_features` (no pred_margin integration)

---

### 3. Player Filtering Mechanism

| Interface | Mechanism | Data Structure |
|-----------|-----------|----------------|
| game_list | None (default rosters) | N/A |
| game_detail | `player_config` from UI | `{home: {playing: [], starters: []}, away: {...}}` |
| Agent | `home_injuries`, `away_injuries` params | Converted to same dict |
| **CLI** | **`--exclude-players` arg** | **Comma-separated IDs** |

**Issue:** CLI uses a completely different mechanism for player filtering that doesn't integrate with the roster system.

---

### 4. Points Model Integration

| Interface | Integration |
|-----------|-------------|
| game_list | None |
| game_detail | Full (loads points model, passes pred_margin) |
| Agent | Full (loads points model, passes pred_margin) |
| **CLI** | **Partial (separate points prediction, not integrated)** |

**Issue:** CLI's points prediction is disconnected from classifier - doesn't pass `pred_margin` as additional feature.

---

### 5. Config Resolution

| Interface | Primary Source | Fallback |
|-----------|---------------|----------|
| game_list | MongoDB selected config | Error |
| game_detail | MongoDB selected config | Error |
| Agent | MongoDB selected config | Error |
| **CLI** | MongoDB selected config | **Latest CSV + cache** |

**Issue:** CLI has a complex fallback system that can result in using a different model than the web/agent interfaces.

---

## Duplication Analysis

### Duplicated Code

1. **Model loading logic**
   - `web/app.py` has inline loading
   - `agents/tools/matchup_predict.py` has `load_model_from_config()`
   - `cli/train.py` has its own loading + training

2. **Player filter building**
   - `web/app.py` builds from request params
   - `agents/tools/matchup_predict.py` builds from function params
   - `cli/train.py` uses `--exclude-players` (incompatible)

3. **Matchup fetching**
   - `web/app.py:predict_all()` calls ESPN API
   - `cli/train.py:predict_mode()` calls ESPN API
   - Others receive matchups as parameters

### Missing Unification

The `core/` layer has:
- ✓ `predict_with_player_config()` - used by web + agent
- ✓ `build_player_lists_for_prediction()` - used by web + agent
- ✓ `ModelFactory.create_model()` - used by web + agent
- ❌ No unified prediction entry point that CLI uses
- ❌ No unified matchup fetching in core

---

## Recommended Unified Architecture

### Create `core/prediction_service.py`

```python
class PredictionService:
    """Single Source of Truth for all prediction workflows."""

    def __init__(self, db=None):
        self.db = db or Mongo().db
        self.model_factory = ModelFactory()
        self.config_manager = ModelConfigManager(self.db)

    def predict_game(
        self,
        home_team: str,
        away_team: str,
        game_date: str,
        game_id: Optional[str] = None,
        player_config: Optional[Dict] = None,
        include_points: bool = True,
        classifier_config: Optional[Dict] = None,
        points_config: Optional[Dict] = None,
    ) -> PredictionResult:
        """
        Unified prediction for a single game.

        Used by: game_detail UI, agent tooling, CLI
        """
        # 1. Load configs (from param or MongoDB)
        classifier_config = classifier_config or self._get_selected_classifier()
        points_config = points_config or self._get_selected_points()

        # 2. Load models (from artifacts via ModelFactory)
        model, scaler, features = self.model_factory.create_model(classifier_config)

        # 3. Build player filters (unified mechanism)
        player_filters = self._build_player_filters(
            home_team, away_team, game_date, game_id, player_config
        )

        # 4. Get points prediction if enabled
        additional_features = {}
        if include_points and points_config:
            points_pred = self._predict_points(points_config, ...)
            additional_features['pred_margin'] = points_pred['point_diff_pred']

        # 5. Make classifier prediction
        return model.predict_with_player_config(
            home_team, away_team, season, game_date,
            player_filters=player_filters,
            additional_features=additional_features
        )

    def predict_date(
        self,
        date: str,
        player_configs: Optional[Dict[str, Dict]] = None,
        include_points: bool = True,
    ) -> List[PredictionResult]:
        """
        Predict all games on a date.

        Used by: game_list UI, CLI
        """
        # 1. Fetch matchups (unified)
        matchups = self._get_matchups_for_date(date)

        # 2. Predict each game
        results = []
        for matchup in matchups:
            player_config = player_configs.get(matchup['game_id']) if player_configs else None
            result = self.predict_game(
                home_team=matchup['home_team'],
                away_team=matchup['away_team'],
                game_date=date,
                game_id=matchup['game_id'],
                player_config=player_config,
                include_points=include_points,
            )
            results.append(result)

        return results

    def _get_matchups_for_date(self, date: str) -> List[Dict]:
        """Unified matchup fetching."""
        # Move ESPN API logic here or call existing function
        ...

    def _build_player_filters(self, ...) -> Dict:
        """Unified player filter building."""
        return build_player_lists_for_prediction(...)
```

### Updated Interface Code

**game_list UI:**
```python
@app.route('/api/predict-all', methods=['POST'])
def predict_all():
    date = request.json.get('date')
    service = PredictionService()
    results = service.predict_date(date)
    return jsonify([r.to_dict() for r in results])
```

**game_detail UI:**
```python
@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    service = PredictionService()
    result = service.predict_game(
        home_team=data['home_team'],
        away_team=data['away_team'],
        game_date=data['game_date'],
        game_id=data['game_id'],
        player_config=data.get('player_config'),
    )
    return jsonify(result.to_dict())
```

**Agent tooling:**
```python
def predict(home, away, game_date, game_id=None, home_injuries=None, ...):
    service = PredictionService()
    player_config = _build_player_config(home_injuries, away_injuries, ...)
    return service.predict_game(
        home_team=home,
        away_team=away,
        game_date=game_date,
        game_id=game_id,
        player_config=player_config,
    )
```

**CLI:**
```python
def predict_mode(args):
    service = PredictionService()
    results = service.predict_date(
        date=args.date,
        include_points=not args.no_points,
    )
    for result in results:
        print(format_prediction_line(result))
```

---

## Migration Path

### Phase 1: Create unified service
1. Create `core/prediction_service.py` with `PredictionService` class
2. Implement `predict_game()` and `predict_date()`
3. Move matchup fetching to core

### Phase 2: Migrate interfaces
1. Update `web/app.py` routes to use `PredictionService`
2. Update `agents/tools/matchup_predict.py` to use `PredictionService`
3. Update `cli/train.py` to use `PredictionService`

### Phase 3: Cleanup
1. Remove duplicated model loading logic
2. Remove duplicated player filter building
3. Deprecate `NBAModel.predict()` (keep only `predict_with_player_config()`)

---

## Benefits

1. **Single code path** - Fix a bug once, fixed everywhere
2. **Consistent behavior** - Same model, same features, same results
3. **Easier testing** - Test one service, not four implementations
4. **Cleaner interfaces** - Web/agent/CLI become thin wrappers
5. **Feature parity** - All interfaces get points integration, player filtering, etc.
