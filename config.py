import os

# IMPORTANT:
# - Do not hardcode secrets in this repo.
# - Set these via environment variables instead.
#
# Required env vars:
# - MONGO_CONN_STR (or MONGODB_URI)
# - OPENAI_API_KEY
config = {
    "mongo_conn_str": os.environ.get("MONGO_CONN_STR") or os.environ.get("MONGODB_URI", ""),
    "openai_api_key": os.environ.get("OPENAI_API_KEY", ""),
}

