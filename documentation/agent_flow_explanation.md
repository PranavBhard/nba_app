# LangChain Agent Flow Explanation

## Model Update
✅ Updated from `gpt-4` (8,192 token limit) to `gpt-4o` (128,000 token limit)

## Agent Flow: Step-by-Step Breakdown

### Example User Question:
> "Lets start out with team level stats (leave player level out of it). What are our strongest features and how quality (accuracy, brier score, log loss, std dev, etc) can we get it with just team level stats?"

---

## High-Level Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER SENDS MESSAGE                            │
│  "What are our strongest features with team level stats?"        │
└───────────────────────────┬───────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│             1. MESSAGE PREPARATION                               │
│  • Load conversation history from MongoDB                        │
│  • Convert to LangChain message format (HumanMessage/AIMessage) │
│  • Append current user message                                   │
│  • Build messages list: [history..., new_message]                │
└───────────────────────────┬───────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│             2. AGENT EXECUTOR INVOCATION                         │
│  agent_executor.invoke({"messages": messages})                   │
│  • LangGraph agent processes messages                            │
│  • System prompt injected (221 lines of instructions)            │
│  • Tools available: 11 tools with schemas                        │
└───────────────────────────┬───────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│             3. LLM REASONING (gpt-4o)                            │
│  • Analyzes user question                                       │
│  • Considers system prompt instructions                          │
│  • Reviews conversation history                                  │
│  • Decides which tools to use                                   │
│  • Generates tool call(s)                                       │
└───────────────────────────┬───────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│             4. TOOL SELECTION & CALLING                         │
│  Agent decides to call:                                          │
│  • get_available_features() - to see what team-level features   │
│  • build_dataset() - to create training data                    │
│  • run_experiment() - to test models                             │
└───────────────────────────┬───────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│             5. TOOL EXECUTION                                    │
│  Each tool executes and returns metadata (not raw data):         │
│  • Feature lists, dataset IDs, file paths                        │
│  • Metrics summaries, run IDs                                   │
│  • No actual CSV data or DB cursors in messages                 │
└───────────────────────────┬───────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│             6. RESULT ANALYSIS                                   │
│  LLM receives tool results and:                                  │
│  • Analyzes feature lists                                        │
│  • Interprets experiment metrics                                 │
│  • Compares model performance                                    │
│  • Decides if more tools needed                                 │
└───────────────────────────┬───────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│             7. RESPONSE FORMULATION                             │
│  LLM generates final response:                                   │
│  • Summarizes findings                                           │
│  • Presents metrics clearly                                      │
│  • Cites run_ids for evidence                                   │
│  • Suggests next steps                                           │
└───────────────────────────┬───────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│             8. RESPONSE RETURN                                  │
│  • Response text extracted                                       │
│  • Tool calls logged                                            │
│  • Saved to MongoDB chat_sessions                               │
│  • Returned to user                                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Detailed Step-by-Step Flow

### **Step 1: Message Preparation** (`chat()` method)

**Location:** `agents/modeler/modeler_agent.py:234-270`

```python
# Load conversation history from MongoDB
session_doc = db.chat_sessions.find_one({'_id': session_obj_id})
conversation_history = []
for msg in session_doc['messages']:
    if msg['role'] == 'user':
        conversation_history.append(HumanMessage(content=msg['content']))
    elif msg['role'] == 'assistant':
        conversation_history.append(AIMessage(content=msg['content']))

# Add current message
messages = []
messages.extend(conversation_history)  # All previous messages
messages.append(HumanMessage(content=message))  # New user message
```

**What's in `messages`?**
- System prompt (injected by LangChain, not in messages list)
- All previous conversation messages (user + assistant)
- Current user message

**Token count:**
- System message: ~2,000-3,000 tokens
- Conversation history: Variable (grows over time)
- Tool schemas: ~1,041 tokens
- Current message: ~50-200 tokens

---

### **Step 2: Agent Executor Invocation**

**Location:** `agents/modeler/modeler_agent.py:273`

```python
result = self.agent_executor.invoke({"messages": messages})
```

**What happens:**
- LangGraph agent (created by `create_agent()`) processes the messages
- Uses ReAct (Reasoning + Acting) pattern
- Agent can:
  1. Think/reason about the question
  2. Decide to call tools
  3. Analyze tool results
  4. Generate final response

**Agent Graph Structure:**
```
┌─────────────┐
│   START     │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Agent Node     │ ◄──┐
│  (LLM decides)  │    │
└──────┬──────────┘    │
       │               │
       ├─► Call Tool   │
       │   (if needed) │
       │               │
       ├─► Return      │
       │   Response    │
       │               │
       └───────────────┘
```

---

### **Step 3: LLM Reasoning (First Iteration)**

**What the LLM sees:**
1. **System Prompt** (221 lines):
   - Role definition (ML expert)
   - Critical rules (no data leakage, efficient dataset creation)
   - Required workflow (5 steps)
   - Available tools and their descriptions
   - Feature documentation
   - Model types and evaluation metrics

2. **Conversation History:**
   - Previous user questions
   - Previous assistant responses
   - Previous tool calls and results

3. **Current User Message:**
   > "Lets start out with team level stats (leave player level out of it). What are our strongest features and how quality (accuracy, brier score, log loss, std dev, etc) can we get it with just team level stats?"

**LLM Reasoning Process:**
```
1. Parse user intent:
   - User wants team-level features only (no player-level)
   - User wants to know "strongest features"
   - User wants quality metrics (accuracy, brier, log loss, std dev)

2. Plan approach:
   - First, see what team-level features are available
   - Then, run experiments to test feature quality
   - Compare results to find strongest features

3. Decide on tools:
   - get_available_features() - to see feature list
   - build_dataset() - to create training data with team-level features
   - run_experiment() - to test models and get metrics
```

**LLM generates tool call:**
```json
{
  "tool": "get_available_features",
  "input": {}
}
```

---

### **Step 4: Tool Execution (First Tool Call)**

**Tool:** `get_available_features()`

**Location:** `agents/tools/support_tools.py`

**What it does:**
1. Reads from `MASTER_TRAINING.csv` or MongoDB cache
2. Extracts feature names
3. Filters to team-level features (excludes `player_*` and `inj_*` if requested)

**Returns:**
```python
{
    'features': [
        'points|season|avg|diff',
        'wins|season|avg|diff',
        'shooting_efficiency|season|avg|diff',
        # ... more features
    ],
    'count': 45,
    'feature_blocks': ['outcome_strength', 'shooting_efficiency', ...]
}
```

**Important:** Returns feature **names** and **metadata**, NOT actual data values.

---

### **Step 5: LLM Analyzes Tool Result**

**LLM receives:**
- List of available team-level features
- Feature block names (e.g., `outcome_strength`, `shooting_efficiency`)

**LLM reasoning:**
```
1. I see team-level features available:
   - outcome_strength (points, wins)
   - shooting_efficiency (eFG%, TS%, 3P%)
   - offensive_engine, defensive_engine
   - rebounding, turnovers, pace
   - elo_rating

2. To answer "strongest features", I need to:
   - Build a dataset with team-level features
   - Run experiments with different feature combinations
   - Compare metrics to identify which features perform best

3. I'll start with a baseline using all team-level features,
   then do ablation studies to see which are most important.
```

**LLM generates next tool call:**
```json
{
  "tool": "build_dataset",
  "input": {
    "feature_blocks": [
      "outcome_strength",
      "shooting_efficiency",
      "offensive_engine",
      "defensive_engine",
      "rebounding",
      "turnovers",
      "pace",
      "elo_rating"
    ],
    "include_per": false,  // User said no player-level
    "begin_year": 2022,    // Use recent years for speed
    "end_year": 2024,
    "min_games_played": 15
  }
}
```

---

### **Step 6: Tool Execution (Second Tool Call)**

**Tool:** `build_dataset()`

**Location:** `agents/tools/dataset_builder.py`

**What it does:**
1. Checks if dataset exists in cache (by spec hash)
2. If cached, returns cached dataset metadata
3. If not cached:
   - Checks if features exist in `MASTER_TRAINING.csv`
   - If yes, carves subset from master CSV
   - If no, calls `NBAModel.create_training_data()` to generate from scratch
4. Saves dataset to cache
5. Returns metadata

**Returns:**
```python
{
    'dataset_id': 'abc123...',
    'schema': ['points|season|avg|diff', 'wins|season|avg|diff', ...],
    'row_count': 4349,
    'feature_count': 70,
    'csv_path': '/path/to/dataset_abc123.csv',
    'cached': False
}
```

**Important:** Returns file path and metadata, NOT the actual CSV data.

---

### **Step 7: LLM Analyzes Dataset Result**

**LLM receives:**
- Dataset created successfully
- 4,349 rows, 70 features
- Dataset ID for reference

**LLM reasoning:**
```
1. Dataset created with 4,349 games and 70 team-level features
2. Now I need to run experiments to test model quality
3. I'll start with a baseline model using all features
4. Then I can do ablation studies to identify strongest features

Let me run a baseline experiment with LogisticRegression
(common choice for binary classification).
```

**LLM generates next tool call:**
```json
{
  "tool": "run_experiment",
  "input": {
    "task": "binary_home_win",
    "model": {
      "type": "LogisticRegression",
      "c_value": 1.0
    },
    "features": {
      "blocks": [
        "outcome_strength",
        "shooting_efficiency",
        "offensive_engine",
        "defensive_engine",
        "rebounding",
        "turnovers",
        "pace",
        "elo_rating"
      ],
      "include_per": false,
      "diff_mode": "home_minus_away"
    },
    "splits": {
      "type": "time_split",
      "test_size": 0.2,
      "begin_year": 2022
    },
    "preprocessing": {
      "scaler": "standard",
      "impute": "median"
    },
    "description": "Baseline: All team-level features"
  }
}
```

---

### **Step 8: Tool Execution (Third Tool Call)**

**Tool:** `run_experiment()`

**Location:** `agents/tools/experiment_runner.py`

**What it does:**
1. Validates config against `ExperimentConfig` schema
2. Builds dataset (or uses existing one)
3. Loads CSV from file path
4. Trains model (LogisticRegression)
5. Evaluates using time-based split
6. Calculates metrics (accuracy, log_loss, brier, std dev)
7. Saves run to MongoDB
8. Returns metrics and diagnostics

**Returns:**
```python
{
    'run_id': 'run_xyz789...',
    'metrics': {
        'accuracy_mean': 0.682,
        'accuracy_std': 0.015,
        'log_loss_mean': 0.623,
        'brier_mean': 0.198,
        'auc': 0.745
    },
    'diagnostics': {
        'feature_importances': {
            'points|season|avg|diff': 0.145,
            'wins|season|avg|diff': 0.132,
            'shooting_efficiency|season|avg|diff': 0.098,
            # ... more features
        }
    },
    'dataset_id': 'abc123...',
    'artifacts': ['/path/to/model.pkl', '/path/to/scaler.pkl']
}
```

**Important:** Returns **summary metrics** and **feature importances**, NOT raw predictions or training data.

---

### **Step 9: LLM Analyzes Experiment Results**

**LLM receives:**
- Baseline metrics: 68.2% accuracy, 0.623 log loss, 0.198 brier score
- Feature importances showing which features matter most

**LLM reasoning:**
```
1. Baseline performance:
   - Accuracy: 68.2% (±1.5%)
   - Log Loss: 0.623
   - Brier Score: 0.198
   - AUC: 0.745

2. Top features by importance:
   - points|season|avg|diff: 0.145
   - wins|season|avg|diff: 0.132
   - shooting_efficiency: 0.098
   - ...

3. To identify "strongest features", I should:
   - Run ablation studies (remove one feature block at a time)
   - Compare performance to see which features are most critical
   - Or run experiments with individual feature blocks

4. Let me run a few more experiments to compare feature blocks.
```

**LLM may generate additional tool calls:**
- `run_experiment()` with different feature combinations
- `compare_runs()` to see relative performance

---

### **Step 10: Final Response Formulation**

**After all tool calls, LLM generates response:**

```
Based on my analysis of team-level features, here are the strongest features 
and the quality metrics we can achieve:

## Baseline Performance (All Team-Level Features)
- **Accuracy**: 68.2% (±1.5% std dev)
- **Log Loss**: 0.623
- **Brier Score**: 0.198
- **AUC**: 0.745

**Run ID**: run_xyz789...

## Top Features by Importance
1. **points|season|avg|diff** (importance: 0.145)
2. **wins|season|avg|diff** (importance: 0.132)
3. **shooting_efficiency|season|avg|diff** (importance: 0.098)
4. **offensive_engine|season|avg|diff** (importance: 0.087)
5. **defensive_engine|season|avg|diff** (importance: 0.082)

## Feature Blocks Analysis
The strongest feature blocks are:
- **outcome_strength** (points, wins) - highest importance
- **shooting_efficiency** - strong predictive power
- **offensive_engine** and **defensive_engine** - complementary signals

## Recommendations
To further identify the strongest features, I can run ablation studies 
(removing one feature block at a time) to see which have the most impact 
on performance. Would you like me to do that?
```

---

### **Step 11: Response Extraction & Storage**

**Location:** `agents/modeler/modeler_agent.py:275-289`

```python
# Extract response from messages
if isinstance(result, dict):
    messages = result.get('messages', [])
    # Get the last assistant message
    for msg in reversed(messages):
        if hasattr(msg, 'content') and msg.content:
            response_text = msg.content
            break
```

**Save to MongoDB:**
```python
db.chat_sessions.update_one(
    {'_id': session_obj_id},
    {
        '$push': {
            'messages': {
                'role': 'assistant',
                'content': response_text,
                'timestamp': datetime.utcnow(),
                'tool_calls': result.get('tool_calls', [])
            }
        }
    }
)
```

**Return to user:**
```python
return {
    'response': response_text,
    'run_ids': ['run_xyz789...'],
    'runs_this_request': 1,
    'baseline_run_id': None,
    'run_budget_remaining': 14,
    'tool_calls': [
        {
            'name': 'get_available_features',
            'input': {},
            'output': {...}
        },
        {
            'name': 'build_dataset',
            'input': {...},
            'output': {...}
        },
        {
            'name': 'run_experiment',
            'input': {...},
            'output': {...}
        }
    ]
}
```

---

## Key Points About Data Flow

### ✅ What IS Included in Token Window:
1. **System prompt** (~2,000-3,000 tokens)
2. **Conversation history** (all previous messages)
3. **Tool schemas** (~1,041 tokens)
4. **Tool results** (metadata only):
   - Feature names (strings)
   - Metrics (numbers)
   - File paths (strings)
   - Run IDs (strings)

### ❌ What is NOT Included:
1. **Raw CSV data** - Tools return file paths, not data
2. **Database cursors** - Tools query DB but return summaries
3. **Training data rows** - Only row counts are returned
4. **Model weights** - Only metrics and importances returned

### Why This Matters:
- Token window stays manageable
- Agent can reason about results without loading huge datasets
- File paths allow agent to reference data without including it
- Metrics and summaries are sufficient for decision-making

---

## Agent Decision-Making Flow

```
User Question
    │
    ▼
┌─────────────────────────────────────┐
│  LLM Analyzes Question              │
│  • What does user want?             │
│  • What tools do I need?            │
│  • What's my plan?                  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Tool Selection                     │
│  • get_available_features?          │
│  • build_dataset?                  │
│  • run_experiment?                 │
│  • compare_runs?                  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Tool Execution                     │
│  • Call tool with parameters       │
│  • Tool queries DB/files            │
│  • Tool returns metadata           │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Result Analysis                    │
│  • Did tool succeed?                │
│  • What do results mean?            │
│  • Do I need more tools?            │
└──────────────┬──────────────────────┘
               │
               ├─► Yes, need more ──┐
               │                    │
               │                    │
               ▼                    │
┌─────────────────────────────────────┐│
│  Generate Response                  ││
│  • Summarize findings               ││
│  • Cite run_ids                     ││
│  • Suggest next steps               ││
└─────────────────────────────────────┘│
                                       │
                                       │
                                       └──┐
                                          │
                                          ▼
```

---

## Example: Complete Flow for User Question

### User Question:
> "Lets start out with team level stats (leave player level out of it). What are our strongest features and how quality (accuracy, brier score, log loss, std dev, etc) can we get it with just team level stats?"

### Agent's Journey:

1. **Parse Intent:**
   - Team-level features only (no player-level)
   - Find strongest features
   - Get quality metrics

2. **Tool Call 1:** `get_available_features()`
   - Result: List of team-level feature blocks

3. **Tool Call 2:** `build_dataset()`
   - Input: Team-level feature blocks, exclude PER
   - Result: Dataset ID, 4,349 rows, 70 features

4. **Tool Call 3:** `run_experiment()`
   - Input: LogisticRegression, all team-level features
   - Result: Accuracy 68.2%, Log Loss 0.623, Brier 0.198

5. **Tool Call 4:** `run_experiment()` (optional - ablation)
   - Input: Remove one feature block
   - Result: Compare performance

6. **Tool Call 5:** `compare_runs()` (optional)
   - Input: List of run IDs
   - Result: Leaderboard showing best features

7. **Generate Response:**
   - Summarize findings
   - Present metrics clearly
   - Cite run_ids
   - Suggest next steps

---

## Summary

The LangChain agent uses a **ReAct (Reasoning + Acting)** pattern:
1. **Reason** about the user's question
2. **Act** by calling appropriate tools
3. **Observe** tool results
4. **Reason** about results
5. **Act** again if needed (iterative)
6. **Respond** with final answer

All data access happens **outside** the token window - tools query databases and files, but only return **metadata and summaries** to the agent. This keeps the token count manageable while allowing the agent to make informed decisions.

