# Project Instructions for Claude Code

## Architecture Overview

```
basketball/                     # repo root
├── bball/                      # main Python package (SSoT)
│   ├── data/                   # repositories, ESPN client
│   ├── features/               # feature registry, generation
│   ├── training/               # schemas, experiment runner, dataset builder
│   ├── models/                 # model implementations, ensemble
│   ├── services/               # prediction, training, business logic
│   ├── pipeline/               # data pipelines
│   ├── market/                 # Kalshi integration
│   ├── stats/                  # stat calculations, PER, ELO
│   ├── utils/                  # shared utilities
│   ├── config.py               # environment config
│   ├── league_config.py        # league YAML loader
│   └── mongo.py                # MongoDB connection
├── web/                        # consumer: Flask app
├── cli/                        # consumer: CLI scripts
├── agents/                     # consumer: AI agents
├── leagues/                    # league YAML configs
├── tests/                      # test suite
├── pyproject.toml              # package config
└── requirements.txt            # pinned deps
```

## Multi-Sport Architecture

This app depends on `sportscore` (shared infrastructure, installed as `pip install -e ~/Documents/sportscore`). Each `bball/` subdir mirrors a sportscore subpackage:

| bball dir | extends sportscore | contains |
|-----------|-------------------|----------|
| `data/` | `sportscore.db` | Sport-specific repositories, data sources |
| `features/` | `sportscore.features` | Stat definitions, feature sets |
| `training/` | `sportscore.training` | Sport-specific schemas, constants |
| `services/` | `sportscore.services` | Sport-specific orchestration |
| `pipeline/` | `sportscore.pipeline` | Sport-specific data pipelines |
| `market/` | `sportscore.market` | Sport-specific market mapping |

## CRITICAL: Layered Architecture

### The `bball/` Package is the Single Source of Truth (SSoT)

All core functionality lives in `bball/`:
- **Feature registry, calculations, and generation** (`bball/features/`)
- **Training infrastructure** (`bball/training/`) - ExperimentRunner, StackingTrainer, DatasetBuilder, RunTracker, schemas
- **Model training and prediction workflows** (`bball/models/`, `bball/services/prediction.py`)
- **Database access** (`bball/mongo.py`, `bball/data/`)
- **Shared utilities** (`bball/stats/`, `bball/utils/`)

### Consumer Layers (DO NOT put core logic here)

These layers **consume** `bball/` - they do NOT implement core functionality themselves:
- `web/` - Web UI layer
- `agents/` - AI agent tooling layer
- `cli/` - Command-line interface layer

### Rules

1. **NEVER duplicate core logic** - If functionality exists in `bball/`, import and use it.
2. **All new core functionality goes in `bball/`** - New features, calculations, or workflows belong in the core package.
3. **Consumer layers are thin wrappers** - `web/`, `agents/`, and `cli/` should only handle I/O, formatting, and orchestration.
4. **ALL cli scripts and web app views are thin wrappers of core layer code** - They NEVER rewrite shared core code.
5. **League-driven architecture** - First argument for `cli/scripts` is `<league>`. Uses league config YAMLs (`leagues/`).

### HARD STOPS - Do NOT Proceed If:

- **Writing sklearn/model training logic in `web/` or `cli/`**: Stop. This belongs in `bball/services/` or `bball/training/`.
- **Writing feature calculation logic outside `bball/features/`**: Stop. Use the feature registry.
- **Writing database queries outside `bball/` or repository classes**: Stop. Use repository patterns.

### What Belongs Where

| Logic Type | Belongs In | NOT In |
|------------|-----------|--------|
| Model training/evaluation | `bball/services/training_service.py` | `web/app.py`, `cli/` |
| Model creation/instantiation | `bball/training/` | Views, CLI scripts |
| Feature calculations | `bball/features/`, `bball/stats/` | Anywhere else |
| Database access | `bball/data/` repositories | Views, CLI inline |
| Prediction workflow | `bball/services/prediction.py` | Views |
| Config management | `bball/services/config_manager.py` | Views |

### Before Writing Code, Ask:
- Does this functionality already exist in `bball/`? -> **Use it**
- Am I about to modify a file outside `bball/` that has a `bball/` equivalent? -> **Stop. Use the `bball/` version**
- Is this new core logic? -> **Add it to `bball/`, then call it from consumer layers**
- Am I writing training/fitting logic in a view? -> **Stop. Put it in `bball/services/`**

---

## Python Environment
- Always run `source venv/bin/activate` before executing Python commands
- Use `python` (not `python3`) after activating the venv
- With `pip install -e .`, imports like `from bball.X import Y` work everywhere
- Set `PYTHONPATH=/Users/pranav/Documents/basketball` as fallback when running scripts

## MongoDB Access
- Run `. ./setup.sh` but DO NOT read that file EVER (note: this also activates the venv)
- Use `from bball.mongo import Mongo` to connect to the database
- The Mongo wrapper handles connection details automatically

## Data Filtering Rules

**CRITICAL: All stat calculations and training data MUST exclude certain game types (preseason, allstar, etc.).**

### Single Source of Truth: League Config YAML

The excluded game types are defined in each league's YAML config file (`leagues/nba.yaml`, `leagues/cbb.yaml`):

```yaml
# leagues/nba.yaml
season:
  exclude_game_types:
    - preseason
    - allstar
```

**NEVER hardcode `['preseason', 'allstar']`** - always read from the league config.

### How to Access

**In `bball/` classes** (StatHandler, PERCalculator, etc.):
```python
# Use the _exclude_game_types property
query['game_type'] = {'$nin': self._exclude_game_types}
```

**In `web/app.py`** (Flask context):
```python
league_config = getattr(g, "league", None)
exclude_game_types = league_config.exclude_game_types if league_config else ['preseason', 'allstar']
query['game_type'] = {'$nin': exclude_game_types}
```

### When This Filter is Required

- Feature calculations
- Training data generation
- Player stat aggregations (PPG, APG, RPG, PER, etc.)
- Team record calculations
- Any statistical analysis

## Common Commands
```bash
# Activate venv and run Python
source venv/bin/activate && python script.py

# Run with proper PYTHONPATH
source venv/bin/activate && PYTHONPATH=/Users/pranav/Documents/basketball python script.py

# Install package in editable mode
pip install -e .
```

## Known Technical Debt

1. **Training logic inline in `web/app.py`** - StandardScaler, SelectKBest, train_test_split inline. Should call `TrainingService`.
