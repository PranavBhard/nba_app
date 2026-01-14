"""
Modeler Agent - LangChain-based agent for NBA modeling assistance
"""

import sys
import os
import json
from typing import Dict, List, Optional, Any
from pathlib import Path

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Try to import LangChain
try:
    from langchain.agents import create_agent
    from langchain_core.tools import StructuredTool
    from langchain_openai import ChatOpenAI
    LANGCHAIN_AVAILABLE = True
except ImportError as e:
    LANGCHAIN_AVAILABLE = False
    # Create dummy classes for type hints
    class StructuredTool:
        pass
    class AgentGraph:
        pass

from nba_app.agents.tools.data_schema import get_data_schema
from nba_app.agents.tools.dataset_builder import DatasetBuilder
from nba_app.agents.tools.experiment_runner import ExperimentRunner
from nba_app.agents.tools.support_tools import SupportTools
from nba_app.agents.tools.code_executor import CodeExecutor
from nba_app.agents.tools.run_tracker import RunTracker
from nba_app.agents.tools.dataset_augmenter import DatasetAugmenter
from nba_app.agents.tools.blend_experimenter import BlendExperimenter
from nba_app.agents.tools.stacking_tool import StackingTrainer
from nba_app.cli.Mongo import Mongo
from nba_app.agents.utils.json_compression import encode_message_content


class ModelerAgent:
    """LangChain-based agent for NBA modeling assistance"""
    
    def __init__(self, session_id: str, db=None, llm=None):
        """
        Initialize ModelerAgent.
        
        Args:
            session_id: Chat session identifier
            db: MongoDB database instance (optional)
            llm: LangChain LLM instance (optional, will create if not provided)
        """
        if db is None:
            mongo = Mongo()
            self.db = mongo.db
        else:
            self.db = db
        
        self.session_id = session_id
        self.run_tracker = RunTracker(db=self.db)
        self.dataset_builder = DatasetBuilder(db=self.db)
        self.experiment_runner = ExperimentRunner(db=self.db)
        self.support_tools = SupportTools(db=self.db)
        self.blend_experimenter = BlendExperimenter(db=self.db)
        self.code_executor = CodeExecutor(db=self.db)
        self.dataset_augmenter = DatasetAugmenter(db=self.db)
        self.stacking_trainer = StackingTrainer(db=self.db)
        
        # Load system message
        system_message_path = Path(__file__).parent / 'system_message.txt'
        with open(system_message_path, 'r') as f:
            self.system_message = f.read()
        
        # Load additional conversational context from session
        try:
            from bson import ObjectId
            session_doc = self.db.nba_modeler_sessions.find_one({'_id': ObjectId(session_id)})
            if session_doc and 'system_info' in session_doc and session_doc['system_info']:
                system_info = session_doc['system_info']
                if system_info:
                    # Append additional context section
                    context_section = "\n\n## Additional Conversational Context\n\n"
                    context_section += "The following contextual information has been provided for this conversation:\n\n"
                    for i, info_item in enumerate(system_info, 1):
                        context_section += f"--- Context Item {i} ---\n{info_item}\n\n"
                    self.system_message += context_section
        except Exception as e:
            # If there's an error loading system_info, continue with base system message
            print(f"Warning: Could not load system_info for session {session_id}: {e}")
        
        # Load metadata
        metadata_path = Path(__file__).parent / 'metadata.json'
        with open(metadata_path, 'r') as f:
            self.metadata = json.load(f)
        
        self.max_runs_per_request = self.metadata.get('max_runs_per_request', 15)
        self.runs_this_request = 0
        self.baseline_run_id = None
        
        # Initialize LLM if not provided
        if llm is None and LANGCHAIN_AVAILABLE:
            # Get OpenAI API key from config
            from nba_app.config import config
            api_key = config.get('openai_api_key')
            if api_key:
                # Set as environment variable for LangChain (it reads from env by default)
                import os
                os.environ['OPENAI_API_KEY'] = api_key
                self.llm = ChatOpenAI(
                    model='gpt-4o',
                    temperature=self.metadata.get('config', {}).get('temperature', 0.1)
                )
            else:
                raise ValueError("openai_api_key not found in config.py")
        else:
            self.llm = llm
        
        # Create tools
        self.tools = self._create_tools()
        
        # Create agent if LangChain is available
        if LANGCHAIN_AVAILABLE and self.llm:
            self.agent_executor = self._create_agent_executor()
        else:
            self.agent_executor = None
    
    def _create_tools(self) -> List[Any]:
        """Create LangChain tools from our tool functions"""
        tools = []
        
        if not LANGCHAIN_AVAILABLE:
            return tools
        
        # get_data_schema
        tools.append(StructuredTool.from_function(
            func=get_data_schema,
            name="get_data_schema",
            description="Get comprehensive schema documentation for all MongoDB collections, including field definitions, time fields, and relationships."
        ))
        
        # get_available_features
        tools.append(StructuredTool.from_function(
            func=self.support_tools.get_available_features,
            name="get_available_features",
            description="Get list of currently available features from pre-computed feature set. Returns list of feature names and total count."
        ))
        
        # get_features_by_block
        tools.append(StructuredTool.from_function(
            func=self.support_tools.get_features_by_block,
            name="get_features_by_block",
            description="Get list of features for specified feature blocks (e.g., ['offensive_engine', 'defensive_engine']). Returns features organized by block, total count, and lists of valid/invalid block names."
        ))
        
        # get_last_run_features
        tools.append(StructuredTool.from_function(
            func=self.support_tools.get_last_run_features,
            name="get_last_run_features",
            description="Get features used in the most recent experiment run for this session. Returns feature blocks, actual feature names, run_id, and metrics. Useful for understanding what features were used in the last turn."
        ))
        
        # explain_feature_calculation
        tools.append(StructuredTool.from_function(
            func=self.support_tools.explain_feature_calculation,
            name="explain_feature_calculation",
            description="Explain how a specific feature is calculated. Takes a feature name (e.g., 'wins_blend|none|blend:season:0.80/games_12:0.20|diff') and returns the calculation formula, weights, time periods, and component details. Use this to understand the exact calculation for any feature in the master training CSV."
        ))
        
        # build_dataset
        tools.append(StructuredTool.from_function(
            func=self.dataset_builder.build_dataset,
            name="build_dataset",
            description="Build a training dataset from specification. Returns dataset_id, schema, row_count, feature_count, and csv_path. Caches datasets by spec hash."
        ))
        
        # augment_dataset
        tools.append(StructuredTool.from_function(
            func=self.dataset_augmenter.augment_dataset,
            name="augment_dataset",
            description="Merge new feature columns with existing dataset from pre-computed features. Takes master_features (list of existing feature names), new_feature_csv_path (path to CSV with new features), and optional date_range. Returns augmented dataset_id and csv_path."
        ))
        
        # experiment_blend_weights
        tools.append(StructuredTool.from_function(
            func=self.blend_experimenter.experiment_blend_weights,
            name="experiment_blend_weights",
            description="Experiment with different blend feature weight configurations. Takes blend_feature_name (e.g., 'wins', 'points_net', 'off_rtg_net', 'efg_net'), weight_configs (list of dicts with 'season_weight' and 'games_12_weight' keys, e.g., [{'season_weight': 0.8, 'games_12_weight': 0.2}, {'season_weight': 0.7, 'games_12_weight': 0.3}]), optional time_period (defaults to last 2 full seasons), and optional model_type (defaults to 'LogisticRegression'). Generates blend variants, runs lightweight experiments to get importance scores, and returns comparison table. Use this to test different weight combinations for blend features."
        ))
        
        # run_experiment
        # Import ExperimentConfig for schema
        from nba_app.agents.schemas.experiment_config import ExperimentConfig
        
        def run_experiment_with_budget(**kwargs) -> Dict:
            """Run experiment with budget enforcement.
            
            Args:
                **kwargs: Experiment configuration fields (unpacked from ExperimentConfig)
            """
            if self.runs_this_request >= self.max_runs_per_request:
                raise ValueError(f"Run budget exceeded. Maximum {self.max_runs_per_request} runs per request.")
            self.runs_this_request += 1
            # Reconstruct ExperimentConfig from kwargs, then convert to dict
            try:
                exp_config = ExperimentConfig(**kwargs)
                # Convert to dict for experiment_runner
                config_dict = exp_config.model_dump() if hasattr(exp_config, 'model_dump') else exp_config.dict() if hasattr(exp_config, 'dict') else dict(exp_config)
            except Exception as e:
                # If validation fails, try to use kwargs directly as dict
                config_dict = kwargs
            return self.experiment_runner.run_experiment(config_dict, self.session_id)
        
        tools.append(StructuredTool.from_function(
            func=run_experiment_with_budget,
            name="run_experiment",
            description=f"Run a complete experiment (build dataset, train model, evaluate, store). Supports both binary classification (task='binary_home_win') and points regression (task='points_regression'). Returns run_id, metrics, diagnostics, and artifacts. Budget: {self.max_runs_per_request} runs per request.",
            args_schema=ExperimentConfig
        ))
        
        # list_runs
        tools.append(StructuredTool.from_function(
            func=self.support_tools.list_runs,
            name="list_runs",
            description="List experiment runs with optional filters (session_id, model_type, limit). Returns list of run summaries."
        ))
        
        # compare_runs
        tools.append(StructuredTool.from_function(
            func=self.support_tools.compare_runs,
            name="compare_runs",
            description="Compare multiple runs and generate leaderboard with pairwise comparisons. Takes list of run_ids."
        ))
        
        # explain_run - wrapper to pass session_id for better error messages
        def explain_run_with_session(run_id: str) -> Dict:
            """Get detailed explanation of a run, with session context for better error messages."""
            return self.support_tools.explain_run(run_id, session_id=self.session_id)
        
        tools.append(StructuredTool.from_function(
            func=explain_run_with_session,
            name="explain_run",
            description="Get detailed explanation of a run including ALL feature importances (not just top features), F-scores, error analysis, and calibration info. Returns feature_importances_sorted (all features sorted by model importance) and f_scores_sorted (all features sorted by F-score). Always display ALL features when reporting results, not just the top 5 or top 10."
        ))
        
        # feature_audit
        tools.append(StructuredTool.from_function(
            func=self.support_tools.feature_audit,
            name="feature_audit",
            description="Audit a dataset for data quality issues including missingness, variance, correlation clusters, and stability over time."
        ))
        
        # predict
        tools.append(StructuredTool.from_function(
            func=self.support_tools.predict,
            name="predict",
            description="Make predictions using a trained model. Takes model_id and prediction_spec."
        ))
        
        # run_code
        tools.append(StructuredTool.from_function(
            func=self.code_executor.run_code,
            name="run_code",
            description="Execute Python code in a sandboxed environment with time/memory limits. Includes MongoDB access via 'db', helper functions 'get_games(query_dict, limit)', 'get_player_stats(query_dict, limit)', and 'save_feature_csv(df, filename)'. Returns stdout, stderr, result, preview tables, and artifacts (created file paths)."
        ))
        
        # run_ablation_study
        def run_ablation_study_with_budget(
            baseline_run_id: str,
            feature_subsets: List[Dict],
            experiment_config: Optional[Dict] = None,
            ablation_names: Optional[List[str]] = None
        ) -> Dict:
            """Run ablation study with budget enforcement.
            
            Args:
                baseline_run_id: Run ID of baseline experiment (must exist)
                feature_subsets: List of feature subset configs. Each dict should have either 'feature_blocks' (list of block names) or 'individual_features' (list of feature names), matching DatasetSpec format.
                experiment_config: Optional base experiment config. If not provided, uses config from baseline run. Only features will vary across ablation runs.
                ablation_names: Optional list of names for each ablation run (for readability). Must match length of feature_subsets.
            """
            return self._run_ablation_study(
                baseline_run_id=baseline_run_id,
                feature_subsets=feature_subsets,
                experiment_config=experiment_config,
                ablation_names=ablation_names
            )
        
        tools.append(StructuredTool.from_function(
            func=run_ablation_study_with_budget,
            name="run_ablation_study",
            description=f"Run an ablation study by testing multiple feature subsets. Takes baseline_run_id, list of feature_subsets (each with 'feature_blocks' or 'individual_features'), optional experiment_config override, and optional ablation_names. Returns summary table (metrics deltas vs baseline) and full comparison. Each ablation run counts against budget ({self.max_runs_per_request} runs per request)."
        ))
        
        # run_stacking_experiment
        def run_stacking_experiment_with_budget(
            base_run_ids: List[str],
            dataset_spec: Dict,
            meta_c_value: float = 0.1,
            stacking_mode: str = 'naive',
            meta_features: Optional[List[str]] = None
        ) -> Dict:
            """Run stacking experiment with budget enforcement.
            
            Args:
                base_run_ids: List of run_ids for base models to stack (must have at least 2 models)
                dataset_spec: Dataset specification dict (must match base models' configs)
                meta_c_value: C-value for meta-model Logistic Regression (default: 0.1)
                stacking_mode: 'naive' (default) or 'informed'. Informed adds derived features (disagreements, confidences) and optional user features.
                meta_features: Optional list of feature names from dataset to include in meta-model (only used when stacking_mode='informed')
            """
            if self.runs_this_request >= self.max_runs_per_request:
                raise ValueError(f"Run budget exceeded. Maximum {self.max_runs_per_request} runs per request.")
            self.runs_this_request += 1
            return self.stacking_trainer.train_stacked_model(
                base_run_ids=base_run_ids,
                dataset_spec=dataset_spec,
                session_id=self.session_id,
                meta_c_value=meta_c_value,
                stacking_mode=stacking_mode,
                meta_features=meta_features
            )
        
        tools.append(StructuredTool.from_function(
            func=run_stacking_experiment_with_budget,
            name="run_stacking_experiment",
            description=f"Train a stacked model that combines predictions from multiple base models. Takes list of base_run_ids (at least 2), dataset_spec dict (must match base models' time-based calibration config), optional meta_c_value (default: 0.1), optional stacking_mode ('naive' default or 'informed'), and optional meta_features (list of feature names for informed stacking). Base models must have been trained with same time-based calibration config (begin_year, calibration_years, evaluation_year). Returns run_id, metrics, diagnostics, and artifacts. Counts against budget ({self.max_runs_per_request} runs per request)."
        ))
        
        return tools
    
    def _create_agent_executor(self) -> Any:
        """Create LangChain agent using new API"""
        if not LANGCHAIN_AVAILABLE:
            return None
        
        # Create agent using new create_agent API
        # The new API uses the model directly and tools
        # create_agent already returns a compiled graph
        agent_graph = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=self.system_message,
            debug=False
        )
        
        return agent_graph
    
    def _run_ablation_study(
        self,
        baseline_run_id: str,
        feature_subsets: List[Dict],
        experiment_config: Optional[Dict] = None,
        ablation_names: Optional[List[str]] = None
    ) -> Dict:
        """
        Run an ablation study by testing multiple feature subsets.
        
        Args:
            baseline_run_id: Run ID of baseline experiment (must exist)
            feature_subsets: List of feature subset configs. Each dict should have either
                'feature_blocks' (list of block names) or 'individual_features' (list of feature names)
            experiment_config: Optional base experiment config. If not provided, uses config from baseline run.
                Only features will vary across ablation runs.
            ablation_names: Optional list of names for each ablation run (for readability).
                Must match length of feature_subsets.
        
        Returns:
            Dict with:
                - baseline_run_id: Baseline run ID
                - ablation_runs: List of ablation run results
                - summary_table: Summary of metrics deltas vs baseline
                - full_comparison: Full comparison from compare_runs
        """
        # Validate baseline run exists
        baseline_run = self.run_tracker.get_run(baseline_run_id)
        if not baseline_run:
            # Get recent runs to suggest alternatives
            recent_runs = self.run_tracker.list_runs(session_id=self.session_id, limit=10)
            run_ids = [run.get('run_id') for run in recent_runs if run.get('run_id')]
            
            # Check if it looks like a UUID format
            import re
            uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
            is_uuid_format = bool(re.match(uuid_pattern, baseline_run_id.lower()))
            
            if is_uuid_format:
                # Valid UUID format but run doesn't exist - might be from different session or deleted
                error_msg = (
                    f"Baseline run '{baseline_run_id}' not found. "
                    f"This run_id doesn't exist in the database. "
                    f"It may have been deleted, or it might be from a different session. "
                    f"Use list_runs() to see available runs and their run_ids. "
                )
            else:
                # Not a UUID format - likely a name or description
                error_msg = (
                    f"Baseline run '{baseline_run_id}' not found. "
                    f"Run IDs are UUIDs (e.g., '550e8400-e29b-41d4-a716-446655440000'). "
                    f"'{baseline_run_id}' appears to be a name or description, not a run_id. "
                )
            
            if run_ids:
                error_msg += (
                    f"Use `list_runs()` to see available runs and their run_ids. "
                    f"Recent run_ids for this session: {run_ids[:3]}"
                )
            else:
                error_msg += "No runs found for this session. Create a run first using `run_experiment()`."
            
            raise ValueError(error_msg)
        
        # Get baseline config if not provided
        if experiment_config is None:
            experiment_config = baseline_run.get('config', {})
        
        # Validate ablation_names length
        if ablation_names and len(ablation_names) != len(feature_subsets):
            raise ValueError(f"ablation_names length ({len(ablation_names)}) must match feature_subsets length ({len(feature_subsets)})")
        
        # Check budget
        n_ablation_runs = len(feature_subsets)
        if self.runs_this_request + n_ablation_runs > self.max_runs_per_request:
            raise ValueError(
                f"Ablation study would exceed budget. "
                f"Current runs: {self.runs_this_request}, "
                f"Ablation runs needed: {n_ablation_runs}, "
                f"Budget: {self.max_runs_per_request}"
            )
        
        # Get baseline metrics for comparison
        baseline_metrics = baseline_run.get('metrics', {})
        
        # Run ablation experiments
        ablation_runs = []
        ablation_run_ids = [baseline_run_id]  # Include baseline in comparison
        
        for i, feature_subset in enumerate(feature_subsets):
            # Check budget before each run
            if self.runs_this_request >= self.max_runs_per_request:
                raise ValueError(
                    f"Run budget exceeded during ablation study. "
                    f"Completed {len(ablation_runs)}/{n_ablation_runs} runs."
                )
            
            # Create experiment config with this feature subset (deep copy to avoid mutations)
            import copy
            ablation_config = copy.deepcopy(experiment_config)
            
            # Update features in config
            if 'features' not in ablation_config:
                ablation_config['features'] = {}
            
            # Set feature subset
            # Support both 'features' and 'individual_features' as aliases
            if 'individual_features' in feature_subset:
                ablation_config['features']['features'] = feature_subset['individual_features']
                ablation_config['features']['blocks'] = []  # Clear blocks when using individual features
            elif 'features' in feature_subset:
                # 'features' is an alias for 'individual_features'
                ablation_config['features']['features'] = feature_subset['features']
                ablation_config['features']['blocks'] = []  # Clear blocks when using individual features
            elif 'feature_blocks' in feature_subset:
                ablation_config['features']['blocks'] = feature_subset['feature_blocks']
                ablation_config['features']['features'] = None  # Clear individual features when using blocks
            else:
                raise ValueError(
                    f"Feature subset {i} must have either 'feature_blocks', 'individual_features', or 'features'. "
                    f"Got: {list(feature_subset.keys())}"
                )
            
            # Run experiment
            ablation_name = ablation_names[i] if ablation_names else f"ablation_{i+1}"
            try:
                result = self.experiment_runner.run_experiment(ablation_config, self.session_id)
                ablation_run_id = result['run_id']
                ablation_run_ids.append(ablation_run_id)
                self.runs_this_request += 1
                
                # Get run details
                ablation_run = self.run_tracker.get_run(ablation_run_id)
                ablation_metrics = ablation_run.get('metrics', {})
                
                # Calculate deltas vs baseline
                deltas = {}
                for metric_name in ['accuracy_mean', 'log_loss_mean', 'brier_mean', 'auc']:
                    baseline_val = baseline_metrics.get(metric_name, 0)
                    ablation_val = ablation_metrics.get(metric_name, 0)
                    if metric_name == 'log_loss_mean' or metric_name == 'brier_mean':
                        # Lower is better - positive delta means worse
                        delta = ablation_val - baseline_val
                    else:
                        # Higher is better - negative delta means worse
                        delta = ablation_val - baseline_val
                    deltas[metric_name] = delta
                
                ablation_runs.append({
                    'run_id': ablation_run_id,
                    'name': ablation_name,
                    'feature_subset': feature_subset,
                    'metrics': ablation_metrics,
                    'deltas_vs_baseline': deltas
                })
            except Exception as e:
                # Continue with other runs even if one fails
                ablation_runs.append({
                    'run_id': None,
                    'name': ablation_name,
                    'feature_subset': feature_subset,
                    'error': str(e)
                })
        
        # Create summary table
        summary_table = []
        for ablation_run in ablation_runs:
            if 'error' in ablation_run:
                continue
            summary_table.append({
                'name': ablation_run['name'],
                'run_id': ablation_run['run_id'],
                'feature_subset': ablation_run['feature_subset'],
                'accuracy_delta': ablation_run['deltas_vs_baseline'].get('accuracy_mean', 0),
                'log_loss_delta': ablation_run['deltas_vs_baseline'].get('log_loss_mean', 0),
                'brier_delta': ablation_run['deltas_vs_baseline'].get('brier_mean', 0),
                'auc_delta': ablation_run['deltas_vs_baseline'].get('auc', 0)
            })
        
        # Get full comparison (includes baseline)
        full_comparison = None
        if len(ablation_run_ids) >= 2:
            try:
                full_comparison = self.support_tools.compare_runs(ablation_run_ids)
            except Exception as e:
                # Comparison might fail if some runs failed
                pass
        
        return {
            'baseline_run_id': baseline_run_id,
            'baseline_metrics': baseline_metrics,
            'ablation_runs': ablation_runs,
            'summary_table': summary_table,
            'full_comparison': full_comparison,
            'n_ablation_runs': len(ablation_runs),
            'n_successful_runs': len([r for r in ablation_runs if 'error' not in r])
        }
    
    def chat(self, message: str, conversation_history: List = None) -> Dict:
        """
        Process a chat message and return response.
        
        Args:
            message: User message
            conversation_history: Optional list of previous messages (LangChain message objects)
            
        Returns:
            Dict with:
                - response: Agent response text
                - run_ids: List of run IDs created
                - metrics: Any metrics from runs
                - baseline_run_id: Current baseline run ID
                - tool_calls: List of tool invocations with inputs/outputs
        """
        # Reset run counter for new request
        self.runs_this_request = 0
        
        # Get current baseline
        baseline = self.run_tracker.get_baseline(self.session_id)
        if baseline:
            self.baseline_run_id = baseline['run_id']
        
        tool_calls = []
        
        if self.agent_executor:
            # Use LangChain agent (new API)
            try:
                # Import message types for the new API
                from langchain_core.messages import HumanMessage, ToolMessage
                
                # Build message list with conversation history
                # Filter out ToolMessage objects (tool outputs) to reduce context size
                messages = []
                if conversation_history:
                    for msg in conversation_history:
                        # Skip ToolMessage objects (tool outputs) - they're large and not needed in history
                        if isinstance(msg, ToolMessage):
                            continue
                        # Encode any JSON content in message content
                        if hasattr(msg, 'content') and msg.content:
                            msg.content = encode_message_content(msg.content)
                        messages.append(msg)
                messages.append(HumanMessage(content=message))
                
                # Invoke the compiled agent graph with full conversation history
                result = self.agent_executor.invoke({"messages": messages})
                
                # Extract response from messages
                if isinstance(result, dict):
                    messages = result.get('messages', [])
                    # Get the last assistant message
                    for msg in reversed(messages):
                        if hasattr(msg, 'content') and msg.content:
                            response_text = msg.content
                            break
                        elif isinstance(msg, dict) and msg.get('content'):
                            response_text = msg['content']
                            break
                    else:
                        response_text = str(result)
                else:
                    response_text = str(result)
                
                # Extract tool calls from messages (if available)
                # In the new API, tool calls are embedded in messages
                if isinstance(result, dict):
                    messages = result.get('messages', [])
                    for msg in messages:
                        # Check for tool calls in various formats
                        msg_tool_calls = None
                        if hasattr(msg, 'tool_calls'):
                            msg_tool_calls = msg.tool_calls
                        elif isinstance(msg, dict) and 'tool_calls' in msg:
                            msg_tool_calls = msg['tool_calls']
                        
                        if msg_tool_calls:
                            for tool_call in msg_tool_calls:
                                # Handle different tool call formats
                                if isinstance(tool_call, dict):
                                    tool_name = tool_call.get('name', 'unknown')
                                    tool_input = tool_call.get('args', {})
                                elif hasattr(tool_call, 'name'):
                                    tool_name = tool_call.name
                                    tool_input = getattr(tool_call, 'args', {})
                                else:
                                    tool_name = 'unknown'
                                    tool_input = {}
                                
                                tool_calls.append({
                                    'name': tool_name,
                                    'input': tool_input,
                                    'output': None  # Output comes in subsequent messages
                                })
            except Exception as e:
                import traceback
                response_text = f"Error: {str(e)}\n{traceback.format_exc()}"
        else:
            # Fallback: simple response
            response_text = "LangChain not available. Please install langchain and set OPENAI_API_KEY."
        
        # Get recent runs
        recent_runs = self.run_tracker.list_runs(session_id=self.session_id, limit=10)
        run_ids = [run['run_id'] for run in recent_runs]
        
        return {
            'response': response_text,
            'run_ids': run_ids,
            'runs_this_request': self.runs_this_request,
            'baseline_run_id': self.baseline_run_id,
            'run_budget_remaining': self.max_runs_per_request - self.runs_this_request,
            'tool_calls': tool_calls
        }
    
    def set_baseline(self, run_id: str) -> bool:
        """
        Set a run as the baseline for this session.
        
        Args:
            run_id: Run identifier
            
        Returns:
            True if successful
        """
        success = self.run_tracker.set_baseline(run_id, self.session_id)
        if success:
            self.baseline_run_id = run_id
        return success

