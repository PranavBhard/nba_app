"""
JSON compression utilities for LLM context windows.

Uses toon encoding to compress JSON data before passing to LLM,
significantly reducing token usage.
"""

import json
from typing import Any, Union, Dict, List


def encode_json_for_llm(data: Any) -> Union[str, Any]:
    """
    Encode JSON/dict/list data using toon compression for LLM context.
    
    Args:
        data: Data to encode (dict, list, or any JSON-serializable object)
        
    Returns:
        Compressed string if data is JSON-serializable, otherwise returns data as-is
    """
    try:
        from toon.encoder import encode as toon_encode
    except ImportError:
        # Fallback to JSON if toon is not available
        if isinstance(data, (dict, list)):
            return json.dumps(data)
        return data
    
    # Only encode dict/list structures (JSON-like data)
    if isinstance(data, (dict, list)):
        try:
            # Convert to JSON first to ensure it's serializable
            json_str = json.dumps(data)
            json_data = json.loads(json_str)
            # Encode with toon
            compressed = toon_encode(json_data)
            return compressed
        except (TypeError, ValueError, json.JSONDecodeError):
            # If encoding fails, return as JSON string
            try:
                return json.dumps(data)
            except (TypeError, ValueError):
                return str(data)
    
    # For non-dict/list data, return as-is
    return data


def decode_json_from_llm(compressed_str: str) -> Any:
    """
    Decode toon-compressed JSON string back to Python object.
    
    Args:
        compressed_str: Compressed string from toon encoding
        
    Returns:
        Decoded Python object (dict, list, etc.)
    """
    try:
        from toon.decoder import decode as toon_decode
    except ImportError:
        # Fallback to JSON if toon is not available
        try:
            return json.loads(compressed_str)
        except json.JSONDecodeError:
            return compressed_str
    
    try:
        decoded = toon_decode(compressed_str)
        return decoded
    except Exception:
        # If decoding fails, try JSON
        try:
            return json.loads(compressed_str)
        except json.JSONDecodeError:
            return compressed_str


def encode_tool_output(output: Any) -> Any:
    """
    Encode tool output for LLM context.
    
    If output is a dict/list, encodes it with toon.
    Otherwise returns as-is.
    
    Args:
        output: Tool output (usually dict or list)
        
    Returns:
        Encoded output (compressed string if dict/list, otherwise unchanged)
    """
    return encode_json_for_llm(output)


def encode_message_content(content: Any) -> str:
    """
    Encode message content for LLM context.
    
    If content contains JSON structures, encodes them.
    Otherwise returns content as string.
    
    Args:
        content: Message content (string, dict, list, etc.)
        
    Returns:
        Encoded content as string
    """
    if isinstance(content, str):
        # Check if it's already a JSON string
        try:
            json_data = json.loads(content)
            # If it parses as JSON, encode it
            return encode_json_for_llm(json_data)
        except json.JSONDecodeError:
            # Not JSON, return as-is
            return content
    else:
        # Encode dict/list structures
        return encode_json_for_llm(content)

