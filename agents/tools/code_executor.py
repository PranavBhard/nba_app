"""
Code Executor Tool - Sandboxed Python code execution
"""

import sys
import os
import io
import contextlib
import signal
import threading
import logging
from typing import Dict, Optional, List
import traceback
import tempfile
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

logger = logging.getLogger(__name__)

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


class TimeoutError(Exception):
    """Timeout exception"""
    pass


def timeout_handler(signum, frame):
    """Signal handler for timeout"""
    raise TimeoutError("Code execution timed out")


class CodeExecutor:
    """Sandboxed code executor with time and memory limits"""
    
    def __init__(self, max_execution_time: int = 30, max_memory_mb: int = 512, db=None):
        """
        Initialize CodeExecutor.
        
        Args:
            max_execution_time: Maximum execution time in seconds
            max_memory_mb: Maximum memory usage in MB (not enforced, just documented)
            db: MongoDB database instance (optional)
        """
        self.max_execution_time = max_execution_time
        self.max_memory_mb = max_memory_mb
        
        # Initialize MongoDB if not provided
        if db is None:
            from nba_app.cli.Mongo import Mongo
            mongo = Mongo()
            self.db = mongo.db
        else:
            self.db = db
        
        # Create artifacts directory for saved files
        self.artifacts_dir = os.path.join(parent_dir, 'model_output', 'feature_artifacts')
        os.makedirs(self.artifacts_dir, exist_ok=True)
    
    def run_code(self, code: str, globals_dict: Optional[Dict] = None) -> Dict:
        """
        Execute Python code in a sandboxed environment.
        
        Args:
            code: Python code string to execute
            globals_dict: Optional globals dictionary (for exposing datasets)
            
        Returns:
            Dict with:
                - stdout: Standard output
                - stderr: Standard error
                - result: Return value (if any)
                - artifacts: List of created files
                - preview_tables: Dataframe previews (first 10 rows)
        """
        logger.info(f"[CODE_EXECUTOR] Executing code ({len(code)} chars)")
        logger.debug(f"[CODE_EXECUTOR] Full code:\n{code}")
        # Set up restricted globals
        if globals_dict is None:
            globals_dict = {}
        
        # Import common libraries
        import pandas as pd
        import numpy as np
        from sklearn import preprocessing, metrics
        
        # Helper functions for MongoDB and CSV operations
        def get_games(query_dict: Dict, limit: Optional[int] = None) -> List[Dict]:
            """Query stats_nba collection for games.
            
            Args:
                query_dict: MongoDB query dictionary (e.g., {'season': '2023-2024', 'year': 2023})
                limit: Optional limit on number of games to return
                
            Returns:
                List of game documents
            """
            cursor = self.db.stats_nba.find(query_dict)
            if limit:
                cursor = cursor.limit(limit)
            return list(cursor)
        
        def get_player_stats(query_dict: Dict, limit: Optional[int] = None) -> List[Dict]:
            """Query stats_nba_players collection for player statistics.
            
            Args:
                query_dict: MongoDB query dictionary
                limit: Optional limit on number of records to return
                
            Returns:
                List of player stat documents
            """
            cursor = self.db.stats_nba_players.find(query_dict)
            if limit:
                cursor = cursor.limit(limit)
            return list(cursor)
        
        def get_player_games_in_season(season: str, player_id: str, team: str = None) -> List[str]:
            """Get list of game IDs where a player played (stats.min > 0) in a season.
            
            Args:
                season: Season string (YYYY-YYYY format, e.g., '2024-2025')
                player_id: Player ID (ESPN player identifier)
                team: Optional team abbreviation (e.g., 'LAL', 'BOS'). If provided, filters to games for that team.
                
            Returns:
                List of game IDs (strings) where the player played, sorted by date ascending (oldest first)
            """
            query = {
                'season': season,
                'player_id': player_id,
                'stats.min': {'$gt': 0}  # Only games where player played
            }
            
            if team:
                query['team'] = team
            
            # Get games and sort by date ascending
            games = list(self.db.stats_nba_players.find(
                query,
                {'game_id': 1, 'date': 1}
            ).sort('date', 1))
            
            # Extract game IDs
            game_ids = [str(game.get('game_id', '')) for game in games if game.get('game_id')]
            
            return game_ids
        
        def save_feature_csv(df: pd.DataFrame, filename: str) -> str:
            """Save a DataFrame as CSV with validation.
            
            Validates that the DataFrame has required metadata columns:
            - Year, Month, Day, Home, Away, HomeWon
            
            Args:
                df: pandas DataFrame with feature columns
                filename: Filename (will be saved in feature_artifacts directory)
                
            Returns:
                Full path to saved CSV file
                
            Raises:
                ValueError: If required columns are missing
            """
            required_cols = ['Year', 'Month', 'Day', 'Home', 'Away', 'HomeWon']
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                raise ValueError(f"DataFrame missing required metadata columns: {missing_cols}")
            
            # Ensure HomeWon is last column
            feature_cols = [c for c in df.columns if c not in required_cols]
            col_order = required_cols + feature_cols
            # Move HomeWon to end
            col_order.remove('HomeWon')
            col_order.append('HomeWon')
            df = df[col_order]
            
            # Save to artifacts directory
            if not filename.endswith('.csv'):
                filename += '.csv'
            filepath = os.path.join(self.artifacts_dir, filename)
            df.to_csv(filepath, index=False)
            
            return filepath
        
        safe_globals = {
            '__builtins__': {
                'print': print,
                'len': len,
                'range': range,
                'str': str,
                'int': int,
                'float': float,
                'list': list,
                'dict': dict,
                'tuple': tuple,
                'set': set,
                'min': min,
                'max': max,
                'sum': sum,
                'abs': abs,
                'round': round,
                'sorted': sorted,
                'enumerate': enumerate,
                'zip': zip,
                'isinstance': isinstance,
                'type': type,
                'hasattr': hasattr,
                'getattr': getattr,
                'setattr': setattr,
                'ValueError': ValueError,
                'TypeError': TypeError,
                'KeyError': KeyError,
                'IndexError': IndexError
            },
            'pd': pd,
            'np': np,
            'preprocessing': preprocessing,
            'metrics': metrics,
            'db': self.db,  # MongoDB database access
            'get_games': get_games,
            'get_player_stats': get_player_stats,
            'get_player_games_in_season': get_player_games_in_season,
            'save_feature_csv': save_feature_csv,
            'datetime': datetime,
            **globals_dict
        }
        
        # Capture stdout/stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        result = None
        error = None
        use_signal_timeout = False  # Track if we're using signal-based timeout
        
        # Helper function to execute code
        # We need to pass stdout/stderr captures to the function so they work in threads
        def execute_code(stdout_io, stderr_io):
            """Execute code in a separate function for timeout handling"""
            exec_globals = safe_globals.copy()
            
            # Redirect stdout/stderr to the provided StringIO objects
            with contextlib.redirect_stdout(stdout_io), \
                 contextlib.redirect_stderr(stderr_io):
                exec(code, exec_globals)
            
            # Check for common result variables
            if 'result' in exec_globals:
                return exec_globals['result']
            elif 'df' in exec_globals:
                return exec_globals['df']
            elif 'output' in exec_globals:
                return exec_globals['output']
            return None
        
        try:
            # Use threading-based timeout that works in any thread
            # Check if we're in the main thread (signal only works there)
            is_main_thread = threading.current_thread() is threading.main_thread()
            
            if is_main_thread and hasattr(signal, 'SIGALRM'):
                # Try to use signal-based timeout in main thread (more reliable)
                try:
                    signal.signal(signal.SIGALRM, timeout_handler)
                    signal.alarm(self.max_execution_time)
                    use_signal_timeout = True
                except ValueError:
                    # Signal failed (shouldn't happen in main thread, but handle gracefully)
                    # Fall through to threading-based timeout
                    try:
                        signal.alarm(0)
                    except:
                        pass
                    use_signal_timeout = False
            
            if use_signal_timeout:
                # Use signal-based timeout
                with contextlib.redirect_stdout(stdout_capture), \
                     contextlib.redirect_stderr(stderr_capture):
                    result = execute_code(stdout_capture, stderr_capture)
                signal.alarm(0)
            else:
                # Use threading-based timeout for non-main threads or when signal fails
                # Note: stdout/stderr redirection happens inside execute_code for thread safety
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(execute_code, stdout_capture, stderr_capture)
                    try:
                        result = future.result(timeout=self.max_execution_time)
                    except FuturesTimeoutError:
                        error = f"Code execution timed out after {self.max_execution_time} seconds"
                        result = None
        
        except TimeoutError:
            error = f"Code execution timed out after {self.max_execution_time} seconds"
        except Exception as e:
            error = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
        finally:
            # Cancel signal timeout if it was set
            if use_signal_timeout:
                try:
                    signal.alarm(0)
                except (ValueError, OSError):
                    pass  # Ignore errors when canceling alarm
        
        # Extract output
        stdout = stdout_capture.getvalue()
        stderr = stderr_capture.getvalue() if not error else error
        
        # Log execution results for debugging
        logger.info(f"[CODE_EXECUTOR] Execution completed. stdout length: {len(stdout)}, stderr length: {len(stderr)}, result: {result is not None}")
        
        # Warn if code executed successfully but produced no output
        if not error and len(stdout) == 0 and len(stderr) == 0 and result is None:
            logger.warning(f"[CODE_EXECUTOR] WARNING: Code executed successfully but produced NO OUTPUT (no stdout, stderr, or result variable). The code should use print() statements to output results.")
        
        if stdout:
            logger.info(f"[CODE_EXECUTOR] stdout ({len(stdout)} chars): {stdout[:1000]}")
        if stderr and not error:
            logger.debug(f"[CODE_EXECUTOR] stderr: {stderr[:500]}")
        if result is not None:
            logger.info(f"[CODE_EXECUTOR] result type: {type(result)}, value: {str(result)[:500]}")
        
        # Extract preview tables (dataframes)
        preview_tables = {}
        if result is not None and isinstance(result, pd.DataFrame):
            preview_tables['result'] = result.head(10).to_dict('records')
        elif 'df' in safe_globals and isinstance(safe_globals.get('df'), pd.DataFrame):
            preview_tables['df'] = safe_globals['df'].head(10).to_dict('records')
        
        # Track created files (artifacts)
        artifacts = []
        # Check if any CSVs were created in artifacts directory during execution
        # We can't directly track this, but we can check stdout for save_feature_csv calls
        # For now, we'll scan the artifacts directory for recently created files
        # (within last minute, which should cover the execution time)
        try:
            current_time = datetime.now().timestamp()
            for filename in os.listdir(self.artifacts_dir):
                filepath = os.path.join(self.artifacts_dir, filename)
                if os.path.isfile(filepath) and filename.endswith('.csv'):
                    # Check if file was modified recently (within last 2 minutes)
                    mtime = os.path.getmtime(filepath)
                    if current_time - mtime < 120:  # 2 minutes
                        artifacts.append(filepath)
        except Exception:
            pass  # Ignore errors in artifact tracking
        
        from nba_app.agents.utils.json_compression import encode_tool_output
        
        return encode_tool_output({
            'stdout': stdout,
            'stderr': stderr,
            'result': str(result) if result is not None else None,
            'artifacts': artifacts,
            'preview_tables': preview_tables,
            'success': error is None
        })

