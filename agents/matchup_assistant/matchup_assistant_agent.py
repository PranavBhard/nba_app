"""
Matchup Assistant Agent - LangChain-based agent for NBA matchup analysis
"""

import sys
import os
import json
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime, date

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

from nba_app.agents.tools.matchup_predict import predict as predict_matchup
from nba_app.agents.tools.player_stats_tools import get_player_stat, get_player_season_stats, get_player_last_stats, get_player_games_in_season
from nba_app.agents.tools.game_tools import get_game, get_rosters, get_team_games, get_team_last_games
from nba_app.agents.tools.code_executor import CodeExecutor
from nba_app.core.mongo import Mongo
from nba_app.core.utils import get_season_from_date
from nba_app.agents.utils.json_compression import encode_message_content

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MatchupAssistantAgent:
    """LangChain-based agent for NBA matchup analysis"""

    def __init__(self, session_id: str, game_id: str, db=None, llm=None, league=None, league_id: str = "nba"):
        """
        Initialize MatchupAssistantAgent.

        Args:
            session_id: Chat session identifier
            game_id: Game ID for the matchup
            db: MongoDB database instance (optional)
            llm: LangChain LLM instance (optional, will create if not provided)
            league: LeagueConfig instance (optional)
            league_id: League identifier string (default: "nba")
        """
        if db is None:
            mongo = Mongo()
            self.db = mongo.db
        else:
            self.db = db

        self.session_id = session_id
        self.game_id = game_id
        self.league = league
        self.league_id = league_id
        self.code_executor = CodeExecutor(db=self.db)

        # Get games collection based on league config
        if league:
            games_collection = league.collections.get('games', 'stats_nba')
        else:
            games_collection = 'stats_nba'

        # Load game context
        game_doc = self.db[games_collection].find_one({'game_id': game_id})
        if not game_doc:
            raise ValueError(f"Game {game_id} not found")
        
        # Extract game info
        home_team = game_doc.get('homeTeam', {}).get('name', '')
        away_team = game_doc.get('awayTeam', {}).get('name', '')
        game_date_str = game_doc.get('date', '')
        
        if not home_team or not away_team:
            raise ValueError(f"Game {game_id} missing team information")
        
        # Parse date
        if game_date_str:
            try:
                game_date_obj = datetime.strptime(game_date_str, '%Y-%m-%d').date()
            except:
                game_date_obj = date.today()
        else:
            game_date_obj = date.today()
            game_date_str = game_date_obj.strftime('%Y-%m-%d')
        
        self.home_team = home_team
        self.away_team = away_team
        self.game_date = game_date_str
        self.game_date_obj = game_date_obj
        self.season = get_season_from_date(game_date_obj)
        
        # Load system message
        system_message_path = Path(__file__).parent / 'system_message.txt'
        with open(system_message_path, 'r') as f:
            self.system_message = f.read()
        
        # Build context and append to system message
        context_section = self._build_context()
        self.system_message += context_section
        
        # Load metadata
        metadata_path = Path(__file__).parent / 'metadata.json'
        with open(metadata_path, 'r') as f:
            self.metadata = json.load(f)
        
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
                    temperature=self.metadata.get('config', {}).get('temperature', 0.3)
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
    
    def _build_context(self) -> str:
        """Build context string from game, teams, rosters, and model config."""
        context_parts = []
        
        context_parts.append("\n\n## Matchup Context\n\n")
        context_parts.append(f"**Game**: {self.away_team} @ {self.home_team}\n")
        context_parts.append(f"**Game ID**: {self.game_id}\n")
        context_parts.append(f"**Date**: {self.game_date}\n")
        context_parts.append(f"**Season**: {self.season}\n\n")

        # Get league-aware collection names
        games_coll = self.league.collections.get('games', 'stats_nba') if self.league else 'stats_nba'
        teams_coll = self.league.collections.get('teams', 'teams_nba') if self.league else 'teams_nba'
        rosters_coll = self.league.collections.get('rosters', 'nba_rosters') if self.league else 'nba_rosters'
        players_coll = self.league.collections.get('players', 'players_nba') if self.league else 'players_nba'
        model_config_coll = self.league.collections.get('model_config_classifier', 'model_config_nba') if self.league else 'model_config_nba'

        # Get pregame lines (market odds)
        game_doc = self.db[games_coll].find_one({'game_id': self.game_id})
        pregame_lines = game_doc.get('pregame_lines', {}) if game_doc else {}
        if pregame_lines:
            context_parts.append("**Market Odds (Pregame Lines)**:\n")
            if pregame_lines.get('spread') is not None:
                spread = pregame_lines['spread']
                context_parts.append(f"- Spread: {self.home_team} {spread:+.1f}\n")
            if pregame_lines.get('over_under') is not None:
                context_parts.append(f"- Over/Under: {pregame_lines['over_under']:.1f}\n")
            if pregame_lines.get('home_ml') is not None:
                home_ml = pregame_lines['home_ml']
                context_parts.append(f"- {self.home_team} Moneyline: {home_ml:+d}\n")
            if pregame_lines.get('away_ml') is not None:
                away_ml = pregame_lines['away_ml']
                context_parts.append(f"- {self.away_team} Moneyline: {away_ml:+d}\n")
            context_parts.append("\n")

        # Get team metadata
        home_team_data = self.db[teams_coll].find_one({'abbreviation': self.home_team}) or {}
        away_team_data = self.db[teams_coll].find_one({'abbreviation': self.away_team}) or {}
        
        context_parts.append("**Teams**:\n")
        if home_team_data.get('displayName'):
            context_parts.append(f"- {self.home_team}: {home_team_data.get('displayName')}\n")
        if away_team_data.get('displayName'):
            context_parts.append(f"- {self.away_team}: {away_team_data.get('displayName')}\n")
        context_parts.append("\n")
        
        # Get rosters
        home_roster = self.db[rosters_coll].find_one({'season': self.season, 'team': self.home_team})
        away_roster = self.db[rosters_coll].find_one({'season': self.season, 'team': self.away_team})

        if home_roster:
            roster_list = home_roster.get('roster', [])
            player_ids = [str(p.get('player_id', '')) for p in roster_list]
            players = list(self.db[players_coll].find(
                {'player_id': {'$in': player_ids}},
                {'player_id': 1, 'player_name': 1}
            ))
            player_map = {str(p.get('player_id', '')): p.get('player_name', '') for p in players}

            context_parts.append(f"**{self.home_team} Roster** ({len(roster_list)} players):\n")
            for roster_entry in roster_list[:15]:  # Limit to first 15 for context size
                player_id = str(roster_entry.get('player_id', ''))
                player_name = player_map.get(player_id, '')
                starter = "✓" if roster_entry.get('starter', False) else " "
                injured = "⚠" if roster_entry.get('injured', False) else " "
                context_parts.append(f"  {starter} {injured} {player_id}: {player_name}\n")
            context_parts.append("\n")

        if away_roster:
            roster_list = away_roster.get('roster', [])
            player_ids = [str(p.get('player_id', '')) for p in roster_list]
            players = list(self.db[players_coll].find(
                {'player_id': {'$in': player_ids}},
                {'player_id': 1, 'player_name': 1}
            ))
            player_map = {str(p.get('player_id', '')): p.get('player_name', '') for p in players}

            context_parts.append(f"**{self.away_team} Roster** ({len(roster_list)} players):\n")
            for roster_entry in roster_list[:15]:  # Limit to first 15 for context size
                player_id = str(roster_entry.get('player_id', ''))
                player_name = player_map.get(player_id, '')
                starter = "✓" if roster_entry.get('starter', False) else " "
                injured = "⚠" if roster_entry.get('injured', False) else " "
                context_parts.append(f"  {starter} {injured} {player_id}: {player_name}\n")
            context_parts.append("\n")

        # Get selected model config
        model_config = self.db[model_config_coll].find_one({'selected': True})
        if model_config:
            context_parts.append("**Selected Model Configuration**:\n")
            context_parts.append(f"- Model Type: {model_config.get('model_type', 'N/A')}\n")
            context_parts.append(f"- Accuracy: {model_config.get('accuracy', 0):.3f}\n")
            
            features = model_config.get('features', [])
            if features:
                context_parts.append(f"- Features ({len(features)}): {', '.join(features[:10])}")
                if len(features) > 10:
                    context_parts.append(f", ... ({len(features) - 10} more)\n")
                else:
                    context_parts.append("\n")
            
            # Feature importance rankings
            feature_rankings = model_config.get('features_ranked', [])
            if feature_rankings:
                context_parts.append(f"- Top 10 Most Important Features:\n")
                for i, ranking in enumerate(feature_rankings[:10], 1):
                    context_parts.append(f"  {i}. {ranking.get('name', 'N/A')}: {ranking.get('score', 0):.4f}\n")
            context_parts.append("\n")
        
        return ''.join(context_parts)
    
    def _create_tools(self) -> List[Any]:
        """Create LangChain tools from our tool functions"""
        tools = []
        
        if not LANGCHAIN_AVAILABLE:
            return tools
        
        # Get league-aware collection names
        games_coll = self.league.collections.get('games', 'stats_nba') if self.league else 'stats_nba'
        player_stats_coll = self.league.collections.get('player_stats', 'stats_nba_players') if self.league else 'stats_nba_players'
        rosters_coll = self.league.collections.get('rosters', 'nba_rosters') if self.league else 'nba_rosters'

        # Create wrapper for predict that includes game context and league
        def predict_with_context(home: str = None, away: str = None, home_injuries: List[str] = None, away_injuries: List[str] = None, home_starters: List[str] = None, away_starters: List[str] = None) -> Dict:
            """Generate prediction for the matchup."""
            home_team = home or self.home_team
            away_team = away or self.away_team
            return predict_matchup(
                home=home_team,
                away=away_team,
                game_id=self.game_id,
                game_date=self.game_date,
                home_injuries=home_injuries or [],
                away_injuries=away_injuries or [],
                home_starters=home_starters or [],
                away_starters=away_starters or [],
                db=self.db,
                league=self.league,
                games_collection=games_coll
            )

        tools.append(StructuredTool.from_function(
            func=predict_with_context,
            name="predict",
            description=f"Generate prediction for the matchup ({self.away_team} @ {self.home_team}). Takes optional home/away team abbreviations (defaults to current matchup), optional home_injuries (list of player IDs), optional away_injuries (list of player IDs), optional home_starters (list of player IDs), optional away_starters (list of player IDs). Returns prediction with win probabilities (home_win_prob, away_win_prob), MODEL-derived odds (model_home_odds, model_away_odds - these are NOT market odds), and point predictions (home_points_pred, away_points_pred)."
        ))

        # Create league-aware wrappers for player stats tools
        def get_player_stat_wrapper(game_id: str, player_id: str) -> Dict:
            """Get player statistics for a specific game."""
            return get_player_stat(game_id, player_id, db=self.db, player_stats_collection=player_stats_coll)

        def get_player_season_stats_wrapper(season: str, player_id: str) -> Dict:
            """Get season averages for a player."""
            return get_player_season_stats(season, player_id, db=self.db, player_stats_collection=player_stats_coll)

        def get_player_last_stats_wrapper(N: int, player_id: str) -> List[Dict]:
            """Get the last N games for a player."""
            return get_player_last_stats(N, player_id, db=self.db, player_stats_collection=player_stats_coll)

        def get_player_games_in_season_wrapper(season: str, player_id: str, team: str = None) -> List[str]:
            """Get list of game IDs where a player played in a season."""
            return get_player_games_in_season(season, player_id, team=team, db=self.db, player_stats_collection=player_stats_coll)

        # Create league-aware wrappers for game tools
        def get_game_wrapper(game_id: str) -> Dict:
            """Get game information."""
            return get_game(game_id, db=self.db, games_collection=games_coll)

        def get_team_games_wrapper(team: str, season: str, before_date: str = None, home_only: bool = False, away_only: bool = False, limit: int = None) -> List[Dict]:
            """Get games for a team in a season."""
            return get_team_games(team, season, before_date=before_date, home_only=home_only, away_only=away_only, limit=limit, db=self.db, games_collection=games_coll)

        def get_team_last_games_wrapper(N: int, team: str, season: str = None, before_date: str = None) -> List[Dict]:
            """Get the last N games for a team."""
            return get_team_last_games(N, team, season=season, before_date=before_date, db=self.db, games_collection=games_coll)

        def get_rosters_wrapper(team: str, season: str = None) -> Dict:
            """Get team roster."""
            players_coll = self.league.collections.get('players', 'players_nba') if self.league else 'players_nba'
            return get_rosters(team, season=season, db=self.db, rosters_collection=rosters_coll, players_collection=players_coll)

        tools.append(StructuredTool.from_function(
            func=get_player_stat_wrapper,
            name="get_player_stat",
            description="Get player statistics for a specific game. Takes game_id and player_id. Returns player game stats."
        ))

        tools.append(StructuredTool.from_function(
            func=get_player_season_stats_wrapper,
            name="get_player_season_stats",
            description="Get season averages for a player. Takes season (YYYY-YYYY format) and player_id. Returns season statistics and averages."
        ))

        tools.append(StructuredTool.from_function(
            func=get_player_last_stats_wrapper,
            name="get_player_last_stats",
            description="Get the last N games for a player. Takes N (number of games) and player_id. Returns list of game statistics sorted by date descending (most recent first)."
        ))

        tools.append(StructuredTool.from_function(
            func=get_player_games_in_season_wrapper,
            name="get_player_games_in_season",
            description="Get list of game IDs where a player played (stats.min > 0) in a season. Takes season (YYYY-YYYY format), player_id, optional team (abbreviation). Returns list of game IDs sorted by date ascending (oldest first). Use this to find which games a player participated in, then cross-reference with team games to calculate records with/without that player."
        ))

        tools.append(StructuredTool.from_function(
            func=get_game_wrapper,
            name="get_game",
            description="Get game information. Takes game_id. Returns game details including teams, date, season, and outcome (if completed)."
        ))

        tools.append(StructuredTool.from_function(
            func=get_team_games_wrapper,
            name="get_team_games",
            description="Get games for a team in a season. Takes team (abbreviation), season (YYYY-YYYY format), optional before_date (YYYY-MM-DD), optional home_only (bool), optional away_only (bool), optional limit (int). Returns list of games sorted by date descending (most recent first). Use this to answer questions about team records, home/away splits, or game history."
        ))

        tools.append(StructuredTool.from_function(
            func=get_team_last_games_wrapper,
            name="get_team_last_games",
            description="Get the last N games for a team. Takes N (number of games), team (abbreviation), optional season (YYYY-YYYY format), optional before_date (YYYY-MM-DD). Returns list of last N games sorted by date descending (most recent first). Use this to answer questions like 'team's record in last 10 games', 'team's home record in last 5 games', etc."
        ))

        tools.append(StructuredTool.from_function(
            func=get_rosters_wrapper,
            name="get_rosters",
            description="Get team roster. Takes team (abbreviation) and optional season (YYYY-YYYY format). Returns roster with player IDs, names, starter status, and injured status."
        ))
        
        tools.append(StructuredTool.from_function(
            func=self.code_executor.run_code,
            name="run_code",
            description="Execute Python code in a sandboxed environment with time/memory limits. Includes MongoDB access via 'db', helper functions 'get_games(query_dict, limit)', 'get_player_stats(query_dict, limit)', 'get_player_games_in_season(season, player_id, team)', and 'save_feature_csv(df, filename)'. Also includes pandas (pd), numpy (np), and standard Python builtins. Returns stdout, stderr, result, preview tables, and artifacts (created file paths). Use this for calculations after retrieving data with other tools."
        ))
        
        return tools
    
    def _create_agent_executor(self) -> Any:
        """Create LangChain agent using new API"""
        if not LANGCHAIN_AVAILABLE:
            return None
        
        # Create agent using new create_agent API
        agent_graph = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=self.system_message,
            debug=False
        )
        
        return agent_graph
    
    def chat(self, message: str, conversation_history: List = None) -> Dict:
        """
        Process a chat message and return response.
        
        Args:
            message: User message
            conversation_history: Optional list of previous messages (LangChain message objects)
            
        Returns:
            Dict with:
                - response: Agent response text
                - tool_calls: List of tool invocations with inputs/outputs
        """
        logger.info(f"[MATCHUP_ASSISTANT] Session {self.session_id}: Processing message: {message[:100]}...")
        tool_calls = []
        tool_errors = []
        all_tool_outputs = []
        
        if self.agent_executor:
            # Use LangChain agent (new API)
            try:
                # Import message types for the new API
                from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
                
                # Build message list with conversation history
                messages = []
                if conversation_history:
                    logger.debug(f"[MATCHUP_ASSISTANT] Loading {len(conversation_history)} messages from history")
                    for msg in conversation_history:
                        # Skip ToolMessage objects (tool outputs) to reduce context size
                        if isinstance(msg, ToolMessage):
                            continue
                        # Encode any JSON content in message content
                        if hasattr(msg, 'content') and msg.content:
                            msg.content = encode_message_content(msg.content)
                        messages.append(msg)
                messages.append(HumanMessage(content=message))
                
                logger.debug(f"[MATCHUP_ASSISTANT] Invoking agent with {len(messages)} messages")
                
                # Invoke the compiled agent graph with full conversation history
                result = self.agent_executor.invoke({"messages": messages})
                
                logger.debug(f"[MATCHUP_ASSISTANT] Agent returned result type: {type(result)}")
                
                # Extract all messages from result
                result_messages = []
                if isinstance(result, dict):
                    result_messages = result.get('messages', [])
                elif hasattr(result, 'messages'):
                    result_messages = result.messages
                else:
                    result_messages = [result] if result else []
                
                logger.debug(f"[MATCHUP_ASSISTANT] Found {len(result_messages)} messages in result")
                
                # Process all messages to extract tool calls, tool outputs, and errors
                assistant_messages = []
                for i, msg in enumerate(result_messages):
                    msg_type = type(msg).__name__
                    logger.debug(f"[MATCHUP_ASSISTANT] Message {i}: {msg_type}")
                    
                    # Check for tool calls
                    msg_tool_calls = None
                    if hasattr(msg, 'tool_calls'):
                        msg_tool_calls = msg.tool_calls
                    elif isinstance(msg, dict) and 'tool_calls' in msg:
                        msg_tool_calls = msg['tool_calls']
                    
                    if msg_tool_calls:
                        logger.info(f"[MATCHUP_ASSISTANT] Found {len(msg_tool_calls)} tool call(s) in {msg_type}")
                        for tool_call in msg_tool_calls:
                            if isinstance(tool_call, dict):
                                tool_name = tool_call.get('name', 'unknown')
                                tool_input = tool_call.get('args', {})
                                tool_call_id = tool_call.get('id', f'call_{len(tool_calls)}')
                            elif hasattr(tool_call, 'name'):
                                tool_name = tool_call.name
                                tool_input = getattr(tool_call, 'args', {})
                                tool_call_id = getattr(tool_call, 'id', f'call_{len(tool_calls)}')
                            else:
                                tool_name = 'unknown'
                                tool_input = {}
                                tool_call_id = f'call_{len(tool_calls)}'
                            
                            logger.info(f"[MATCHUP_ASSISTANT] Tool call: {tool_name} with input: {json.dumps(tool_input, default=str)[:200]}")
                            
                            tool_calls.append({
                                'name': tool_name,
                                'input': tool_input,
                                'output': None,
                                'call_id': tool_call_id
                            })
                    
                    # Check for tool outputs (ToolMessage)
                    if isinstance(msg, ToolMessage):
                        tool_output = msg.content if hasattr(msg, 'content') else str(msg)
                        # ToolMessage has tool_call_id attribute (not name)
                        tool_call_id = getattr(msg, 'tool_call_id', None) or getattr(msg, 'name', None)
                        
                        logger.info(f"[MATCHUP_ASSISTANT] Tool output received (call_id: {tool_call_id}): {str(tool_output)[:500]}")
                        
                        # Try to match tool output to tool call
                        if tool_call_id:
                            for tc in tool_calls:
                                if tc.get('call_id') == tool_call_id:
                                    tc['output'] = tool_output
                                    break
                        
                        all_tool_outputs.append({
                            'call_id': tool_call_id,
                            'output': tool_output
                        })
                        
                        # Check for errors in tool output
                        if isinstance(tool_output, dict):
                            if tool_output.get('error') or tool_output.get('stderr'):
                                error_msg = tool_output.get('error') or tool_output.get('stderr', '')
                                logger.error(f"[MATCHUP_ASSISTANT] Tool error detected: {error_msg[:500]}")
                                tool_errors.append({
                                    'tool': tool_call_id or 'unknown',
                                    'error': error_msg
                                })
                        elif isinstance(tool_output, str):
                            # Check for common error patterns
                            if 'error' in tool_output.lower() or 'exception' in tool_output.lower() or 'traceback' in tool_output.lower():
                                logger.warning(f"[MATCHUP_ASSISTANT] Possible error in tool output: {tool_output[:500]}")
                                tool_errors.append({
                                    'tool': tool_call_id or 'unknown',
                                    'error': tool_output[:1000]  # Limit error length
                                })
                    
                    # Collect assistant messages for response extraction
                    if isinstance(msg, AIMessage) or (isinstance(msg, dict) and msg.get('type') == 'ai'):
                        assistant_messages.append(msg)
                
                # Extract response from assistant messages (get the last one)
                response_text = None
                for msg in reversed(assistant_messages):
                    if hasattr(msg, 'content') and msg.content:
                        response_text = msg.content
                        break
                    elif isinstance(msg, dict) and msg.get('content'):
                        response_text = msg['content']
                        break
                
                if response_text is None:
                    # Fallback: try to get any content from result
                    if isinstance(result, dict):
                        response_text = str(result)
                    else:
                        response_text = "No response generated by agent."
                    logger.warning(f"[MATCHUP_ASSISTANT] No response text found, using fallback")
                
                logger.info(f"[MATCHUP_ASSISTANT] Response text length: {len(response_text)} chars")
                
                # If there were tool errors, append them to the response
                if tool_errors:
                    logger.warning(f"[MATCHUP_ASSISTANT] Found {len(tool_errors)} tool error(s), appending to response")
                    error_summary = "\n\n[DEBUG: Tool Errors Detected]\n"
                    for i, err in enumerate(tool_errors, 1):
                        error_summary += f"{i}. Tool '{err['tool']}': {err['error'][:500]}\n"
                    response_text += error_summary
                
                # If tools were called but no response mentions them, add debug info
                if tool_calls and len(tool_calls) > 0:
                    logger.info(f"[MATCHUP_ASSISTANT] Total tool calls: {len(tool_calls)}")
                    # Log which tools were called
                    tool_names = [tc['name'] for tc in tool_calls]
                    logger.info(f"[MATCHUP_ASSISTANT] Tools called: {', '.join(tool_names)}")
                    
                    # Check if any tool calls don't have outputs
                    missing_outputs = [tc for tc in tool_calls if tc.get('output') is None]
                    if missing_outputs:
                        logger.warning(f"[MATCHUP_ASSISTANT] {len(missing_outputs)} tool call(s) missing outputs: {[tc['name'] for tc in missing_outputs]}")
                else:
                    logger.warning(f"[MATCHUP_ASSISTANT] No tool calls detected in agent response")
                
            except Exception as e:
                import traceback
                error_trace = traceback.format_exc()
                logger.error(f"[MATCHUP_ASSISTANT] Exception in chat method: {str(e)}\n{error_trace}")
                response_text = f"[ERROR] Agent execution failed: {str(e)}\n\nTraceback:\n{error_trace}"
        else:
            # Fallback: simple response
            logger.error("[MATCHUP_ASSISTANT] Agent executor not available")
            response_text = "LangChain not available. Please install langchain and set OPENAI_API_KEY."
        
        logger.info(f"[MATCHUP_ASSISTANT] Returning response with {len(tool_calls)} tool call(s)")
        
        return {
            'response': response_text,
            'tool_calls': tool_calls
        }
