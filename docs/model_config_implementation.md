# Model Configuration Infrastructure Documentation

This document describes the infrastructure for managing model configurations, training results, and prediction settings in a machine learning web application. The system provides a web-based interface for configuring models, saving/loading configurations, tracking training history, and managing which configuration is used for predictions.

## Overview

The model configuration system consists of:
- A web interface for selecting models, features, and hyperparameters
- MongoDB storage for persistent configuration and training results
- A "selected" configuration mechanism for default prediction settings
- Automatic saving of training results
- A results history viewer with pagination
- Backward compatibility with JSON file storage

## Core Concepts

### Feature Set Hash

Configurations are uniquely identified by a **feature set hash**, which is an MD5 hash of a sorted, comma-separated list of feature names. This ensures that:
- Configurations with identical feature sets are treated as the same configuration
- The hash is deterministic (same features always produce the same hash)
- The hash serves as part of the unique identifier for MongoDB upserts

**Implementation:**
```python
import hashlib

features_sorted = sorted(feature_list)
features_str = ','.join(features_sorted)
feature_set_hash = hashlib.md5(features_str.encode()).hexdigest()
```

### Unique Identifier

Configurations are uniquely identified by the combination of:
- `model_type`: The type of model (e.g., "LogisticRegression", "RandomForest")
- `feature_set_hash`: The MD5 hash of the feature set

This allows multiple model types to share the same feature set while maintaining separate training results.

## MongoDB Collection Structure

### Document Schema

```javascript
{
  "_id": ObjectId,
  "model_type": String,              // e.g., "LogisticRegression"
  "feature_set_hash": String,        // MD5 hash of sorted features
  "features": [String],              // Sorted list of feature names
  "feature_count": Number,
  "name": String,                    // User-editable name
  "selected": Boolean,               // Only one config can be selected
  "accuracy": Number,                // Best accuracy achieved
  "std_dev": Number,                 // Standard deviation of accuracy
  "brier_score": Number,             // Brier score
  "log_loss": Number,                // Log loss
  "features_ranked": [               // Feature importance rankings
    {
      "rank": Number,
      "name": String,
      "score": Number
    }
  ],
  "c_values": {                      // For models with C hyperparameter
    "0.01": Number,                  // Maps C-value to accuracy
    "0.1": Number,
    "1.0": Number
  },
  "best_c_value": Number,            // C-value with best accuracy
  "best_c_accuracy": Number,         // Accuracy of best C-value
  "trained_at": DateTime,
  "updated_at": DateTime,
  "training_stats": {                // Optional training metadata
    "total_games": Number,
    "training_instances": Number,
    "augmented_instances": Number
  },
  "cv_results": {                    // Optional cross-validation results
    "mean": Number,
    "std": Number
  }
}
```

## API Endpoints

### 1. Save Configuration (`POST /api/config/save`)

Saves the current UI configuration to MongoDB. This endpoint:

1. **Validates input**: Ensures model types, features, and C-values are provided
2. **Generates feature set hash**: Creates MD5 hash from sorted feature list
3. **Manages selected flag**: 
   - Unsets `selected: true` for all existing configs
   - Sets `selected: true` for the first model type in the request
4. **Upserts by unique identifier**: Uses `model_type` + `feature_set_hash` as the unique key
5. **Preserves existing data**: When updating an existing config:
   - Preserves custom name if it was edited
   - Preserves training results (accuracy, rankings, etc.)
   - Updates feature list and C-values if changed
6. **Backward compatibility**: Also saves to JSON file for systems not using MongoDB

**Request Body:**
```json
{
  "model_types": ["LogisticRegression", "RandomForest"],
  "features": ["feature1", "feature2", "feature3"],
  "c_values": [0.01, 0.1, 1.0]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Config saved successfully for 2 model type(s)",
  "saved_configs": [
    {"model_type": "LogisticRegression", "feature_set_hash": "abc123..."},
    {"model_type": "RandomForest", "feature_set_hash": "abc123..."}
  ]
}
```

**Upsert Logic:**
```python
# Check if config exists
existing = db.model_configs.find_one({
    'model_type': model_type,
    'feature_set_hash': feature_set_hash
})

if existing:
    # Update: preserve name and training results
    update_doc = {
        'features': features_sorted,
        'feature_count': len(features),
        'updated_at': datetime.now(),
        'selected': True  # Only for first model type
    }
    # Preserve custom name if it exists
    if existing.get('name') and not existing['name'].startswith(model_type + ' - '):
        update_doc['name'] = existing['name']
    
    db.model_configs.update_one(
        {'model_type': model_type, 'feature_set_hash': feature_set_hash},
        {'$set': update_doc}
    )
else:
    # Insert new config
    doc = {
        'model_type': model_type,
        'feature_set_hash': feature_set_hash,
        'features': features_sorted,
        'name': f"{model_type} - {feature_set_hash[:8]}",
        'selected': True,  # Only for first model type
        'trained_at': datetime.now(),
        'updated_at': datetime.now()
    }
    db.model_configs.insert_one(doc)
```

### 2. Load Configuration (`GET /api/config/load`)

Loads configuration from JSON file (backward compatibility). This endpoint:
- Reads from a JSON file in the cache directory
- Returns the configuration in the same format as the save endpoint
- Used as fallback when MongoDB is not available

**Response:**
```json
{
  "success": true,
  "config": {
    "model_types": ["LogisticRegression"],
    "features": ["feature1", "feature2"],
    "c_values": [0.1],
    "saved_at": "2024-01-01T12:00:00"
  }
}
```

### 3. Get All Configurations (`GET /api/model-configs`)

Retrieves all saved configurations from MongoDB, sorted by training date (most recent first).

**Response:**
```json
{
  "configs": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "model_type": "LogisticRegression",
      "feature_set_hash": "abc123...",
      "name": "My Custom Config",
      "selected": true,
      "accuracy": 85.5,
      "feature_count": 50,
      "trained_at": "2024-01-01T12:00:00"
    }
  ]
}
```

### 4. Update Configuration (`PUT /api/model-configs/<config_id>`)

Updates a configuration's name or selected status.

**Request Body:**
```json
{
  "name": "Updated Config Name",
  "selected": true
}
```

**Selected Flag Management:**
When setting `selected: true`:
- All other configs are automatically set to `selected: false`
- Only one config can be selected at a time
- The selected config is used as the default for predictions

**Implementation:**
```python
if data.get('selected') == True:
    # Unset all other configs
    db.model_configs.update_many(
        {'selected': True},
        {'$set': {'selected': False}}
    )
    # Set this config as selected
    update_fields['selected'] = True
else:
    update_fields['selected'] = False

db.model_configs.update_one(
    {'_id': ObjectId(config_id)},
    {'$set': update_fields}
)
```

### 5. Get Selected Configuration (`GET /api/model-configs/selected`)

Retrieves the currently selected configuration (the one with `selected: true`).

**Response:**
```json
{
  "config": {
    "_id": "507f1f77bcf86cd799439011",
    "model_type": "LogisticRegression",
    "features": ["feature1", "feature2"],
    "selected": true,
    "best_c_value": 0.1,
    "accuracy": 85.5
  }
}
```

### 6. Get Last Configuration (`GET /api/model-configs/last`)

Retrieves the most recently trained configuration (by `trained_at` timestamp).

### 7. Training Endpoint (`POST /api/train`)

Executes training and automatically saves results to MongoDB. This endpoint:

1. **Runs training** with the provided configuration
2. **Tracks best C-value**: For models with C hyperparameter, tracks which C-value performed best
3. **Accumulates results**: Groups results by `(model_type, feature_set_hash)` combination
4. **Saves to MongoDB**: After training completes, calls `save_model_config_to_mongo()` for each unique combination

**Best C-Value Tracking:**
```python
# During training loop
for c_value in c_values:
    accuracy = train_model(model_type, features, c_value)
    
    # Track best C-value
    if accuracy > best_accuracy:
        best_c_value = c_value
        best_accuracy = accuracy
        best_results = {
            'c_value': c_value,
            'accuracy': accuracy,
            'std_dev': std_dev,
            'brier_score': brier_score,
            'log_loss': log_loss
        }

# After training, save with best C-value
save_model_config_to_mongo(
    model_type=model_type,
    features=features,
    accuracy=best_accuracy,
    best_c_value=best_c_value,
    c_values={c_val: acc for c_val, acc in all_results},
    ...
)
```

**Auto-Save After Training:**
```python
# After all training completes
for (model_type, feature_set_hash), config_data in model_configs.items():
    best = config_data['best']
    save_model_config_to_mongo(
        model_type=model_type,
        features=config_data['features'],
        accuracy=best['accuracy'],
        std_dev=best['std_dev'],
        brier_score=best['brier_score'],
        log_loss=best['log_loss'],
        feature_rankings=config_data['feature_rankings'],
        c_values=config_data['c_values'],
        ...
    )
```

## Frontend Implementation

### Save Config Button Behavior

When the user clicks "Save Config":
1. Collects current UI state:
   - Selected model types
   - Selected features (from checkboxes)
   - Selected C-values
2. Validates that at least one of each is selected
3. Sends POST request to `/api/config/save`
4. Shows success/error alert

**JavaScript Implementation:**
```javascript
async function saveConfig() {
    const modelTypes = Array.from(document.querySelectorAll('input[name="model_types"]:checked'))
        .map(cb => cb.value);
    const cValues = Array.from(document.querySelectorAll('input[name="c_values"]:checked'))
        .map(cb => parseFloat(cb.value));
    const selectedFeatures = Array.from(document.querySelectorAll('.feature-checkbox:checked'))
        .map(cb => cb.value);
    
    // Validation
    if (modelTypes.length === 0 || selectedFeatures.length === 0 || cValues.length === 0) {
        alert('Please select at least one model type, feature, and C-value');
        return;
    }
    
    // Save to MongoDB
    const response = await fetch('/api/config/save', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            model_types: modelTypes,
            features: selectedFeatures,
            c_values: cValues
        })
    });
    
    const data = await response.json();
    if (data.success) {
        alert('Configuration saved successfully!');
    }
}
```

### Load Config Button Behavior

When the user clicks "Load Config":
1. Fetches all configurations from `/api/model-configs`
2. Displays a modal with list of saved configs
3. Each config shows:
   - Radio button (selected config is pre-checked)
   - Editable name field
   - Model type, accuracy, feature count, training date
4. User can:
   - Select a config (sets it as `selected: true`)
   - Edit the config name
   - Load the config into the UI

**Config Selection Modal:**
```javascript
function displayConfigModal(configs) {
    const modal = document.getElementById('configModal');
    let html = '';
    
    configs.forEach(config => {
        const isSelected = config.selected || false;
        html += `
            <div class="config-item ${isSelected ? 'selected' : ''}">
                <input type="radio" name="configSelect" value="${config._id}" 
                       ${isSelected ? 'checked' : ''} 
                       onchange="selectConfig('${config._id}')">
                <input type="text" value="${config.name}" 
                       onblur="updateConfigName('${config._id}', this.value)">
                <div>Model: ${config.model_type}</div>
                <div>Accuracy: ${config.accuracy}%</div>
                <div>Features: ${config.feature_count}</div>
            </div>
        `;
    });
    
    modal.innerHTML = html;
    modal.style.display = 'block';
}
```

**Loading Config into UI:**
```javascript
async function loadConfigIntoUI(config) {
    // Set model types
    document.querySelectorAll('input[name="model_types"]').forEach(cb => {
        cb.checked = (config.model_types || []).includes(cb.value);
    });
    
    // Set features
    document.querySelectorAll('.feature-checkbox').forEach(cb => {
        cb.checked = (config.features || []).includes(cb.value);
    });
    
    // Set C-values
    document.querySelectorAll('input[name="c_values"]').forEach(cb => {
        cb.checked = (config.c_values || []).includes(parseFloat(cb.value));
    });
    
    updateFeatureCount();
}
```

### Auto-Load Selected Config on Page Load

When the page loads:
1. Server-side: Attempts to load selected config from MongoDB
2. Falls back to JSON file if MongoDB config not found
3. Passes config to template as `default_config`
4. Client-side: JavaScript auto-populates UI with config values

**Server-Side (Flask):**
```python
@app.route('/model-config')
def model_config():
    # Try MongoDB first
    selected_config = None
    mongo_config = db.model_configs.find_one({'selected': True})
    
    if mongo_config:
        selected_config = {
            'model_types': [mongo_config.get('model_type')],
            'features': mongo_config.get('features', []),
            'c_values': []
        }
        # Extract C-values
        if mongo_config.get('best_c_value'):
            selected_config['c_values'] = [mongo_config['best_c_value']]
        elif mongo_config.get('c_values'):
            selected_config['c_values'] = [float(c) for c in mongo_config['c_values'].keys()]
    
    # Fallback to JSON file
    if not selected_config:
        config_path = 'cache/default_config.json'
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                selected_config = json.load(f)
    
    return render_template('model_config.html', default_config=selected_config)
```

**Client-Side Auto-Load:**
```javascript
window.addEventListener('DOMContentLoaded', function() {
    // Check if default_config was passed from server
    const defaultConfig = {{ default_config|tojson|safe }};
    
    if (defaultConfig) {
        // Populate UI with default config
        loadConfigIntoUI(defaultConfig);
    }
    
    // Also load selected config from MongoDB on page load
    loadSelectedConfigOnPageLoad();
});

async function loadSelectedConfigOnPageLoad() {
    try {
        const response = await fetch('/api/model-configs/selected');
        const data = await response.json();
        
        if (data.config) {
            loadConfigIntoUI(data.config);
        }
    } catch (error) {
        console.error('Could not load selected config:', error);
    }
}
```

### Results History Display

The results section displays training history with:
- **Pagination**: 5 results per page
- **Expandable panels**: Each result can be expanded to show details
- **Sorting**: Most recent first (by `trained_at` timestamp)
- **Display format**: Shows accuracy, log loss, brier score, std dev, feature rankings

**Results Structure:**
```javascript
{
  "results": [
    {
      "model_type": "LogisticRegression",
      "c_value": 0.1,
      "accuracy": 85.5,
      "std_dev": 2.3,
      "log_loss": 0.45,
      "brier_score": 0.12,
      "feature_rankings": [
        {"rank": 1, "name": "feature1", "score": 0.95},
        {"rank": 2, "name": "feature2", "score": 0.87}
      ],
      "timestamp": "2024-01-01T12:00:00"
    }
  ],
  "total_tested": 10
}
```

**Pagination Implementation:**
```javascript
let currentPage = 1;
const resultsPerPage = 5;

function displayResultsPaginated(results) {
    const startIndex = (currentPage - 1) * resultsPerPage;
    const endIndex = startIndex + resultsPerPage;
    const pageResults = results.slice(startIndex, endIndex);
    
    // Display pageResults
    pageResults.forEach(result => {
        displayResultPanel(result);
    });
    
    // Update pagination controls
    updatePaginationControls(results.length);
}

function changePage(page) {
    currentPage = page;
    displayResultsPaginated(allResults);
}
```

**Loading Results from MongoDB:**
```javascript
async function loadAllResults() {
    try {
        const response = await fetch('/api/model-configs');
        const data = await response.json();
        
        // Convert MongoDB configs to results format
        const results = data.configs.map(config => ({
            model_type: config.model_type,
            c_value: config.best_c_value || config.c_value,
            accuracy: config.accuracy,
            std_dev: config.std_dev,
            log_loss: config.log_loss,
            brier_score: config.brier_score,
            feature_rankings: config.features_ranked || [],
            timestamp: config.trained_at
        }));
        
        // Sort by timestamp (most recent first)
        results.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
        
        displayResultsPaginated(results);
    } catch (error) {
        console.error('Error loading results:', error);
    }
}
```

## Backward Compatibility

The system maintains backward compatibility with a JSON file storage mechanism:

1. **Save Config**: When saving, also writes to `cache/default_config.json`
2. **Load Config**: Falls back to JSON file if MongoDB is unavailable
3. **File Format**:
```json
{
  "model_types": ["LogisticRegression"],
  "features": ["feature1", "feature2"],
  "c_values": [0.1],
  "saved_at": "2024-01-01T12:00:00"
}
```

**Implementation:**
```python
# Save to both MongoDB and JSON file
config = {
    'model_types': model_types,
    'features': features,
    'c_values': c_values,
    'saved_at': datetime.now().isoformat()
}

# MongoDB
db.model_configs.update_one(...)

# JSON file (backward compatibility)
config_path = os.path.join(base_dir, 'cache', 'default_config.json')
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)
```

## Prediction Configuration Priority

When making predictions, the system uses the following priority order:

1. **Command-line arguments** (if provided)
2. **Selected config from MongoDB** (`selected: true`)
3. **Default config file** (`cache/default_config.json`)
4. **Cached config** (in-memory)
5. **Hardcoded defaults**

**Implementation:**
```python
def get_prediction_config(cli_args=None):
    # Priority 1: Command-line arguments
    if cli_args and cli_args.get('model_type'):
        return cli_args
    
    # Priority 2: Selected config from MongoDB
    selected_config = db.model_configs.find_one({'selected': True})
    if selected_config:
        return {
            'model_type': selected_config['model_type'],
            'features': selected_config['features'],
            'c_value': selected_config.get('best_c_value') or selected_config.get('c_value')
        }
    
    # Priority 3: Default config file
    config_path = 'cache/default_config.json'
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    
    # Priority 4: Hardcoded defaults
    return {
        'model_type': 'LogisticRegression',
        'features': ['default_feature1', 'default_feature2'],
        'c_value': 0.1
    }
```

## Implementation Checklist

To implement this infrastructure in a new project:

### Backend

- [ ] Create MongoDB collection for model configurations
- [ ] Implement feature set hash generation (MD5 of sorted features)
- [ ] Create `/api/config/save` endpoint with upsert logic
- [ ] Create `/api/config/load` endpoint (JSON fallback)
- [ ] Create `/api/model-configs` endpoint (GET all)
- [ ] Create `/api/model-configs/<id>` endpoint (PUT update)
- [ ] Create `/api/model-configs/selected` endpoint (GET selected)
- [ ] Create `/api/model-configs/last` endpoint (GET last)
- [ ] Implement selected flag management (only one selected at a time)
- [ ] Implement config name preservation on updates
- [ ] Implement best C-value tracking during training
- [ ] Implement auto-save after training completes
- [ ] Implement backward compatibility JSON file save/load

### Frontend

- [ ] Create "Save Config" button with validation
- [ ] Create "Load Config" button that opens modal
- [ ] Implement config selection modal UI
- [ ] Implement config name editing (inline)
- [ ] Implement config selection (radio buttons)
- [ ] Implement auto-load selected config on page load
- [ ] Implement results history display
- [ ] Implement results pagination (5 per page)
- [ ] Implement expandable result panels
- [ ] Implement feature count display
- [ ] Implement UI population from config data

### Database

- [ ] Create index on `model_type` and `feature_set_hash` (compound index)
- [ ] Create index on `selected` field
- [ ] Create index on `trained_at` field (for sorting)

## Best Practices

1. **Always sort features** before hashing to ensure consistency
2. **Preserve user data** when updating configs (names, training results)
3. **Validate inputs** before saving to prevent invalid configurations
4. **Handle errors gracefully** with fallbacks (MongoDB → JSON file → defaults)
5. **Use transactions** if updating multiple configs (e.g., unsetting selected flags)
6. **Cache frequently accessed data** (selected config) to reduce database queries
7. **Log important operations** (saves, loads, selections) for debugging
8. **Version your schema** if the document structure changes over time

## Security Considerations

1. **Validate user input** before saving to prevent injection attacks
2. **Sanitize config names** to prevent XSS in the UI
3. **Limit config size** to prevent DoS (e.g., max features, max name length)
4. **Authenticate requests** if the system has multiple users
5. **Rate limit** save/load operations to prevent abuse

