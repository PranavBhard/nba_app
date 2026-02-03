#!/bin/bash
#
# Populate Vegas betting lines in stats_nba collection
# Reads from nba_2008-2025.csv and adds vegas object to game documents
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
NBA_DIR="$(cd "$APP_DIR/.." && pwd)"

echo "================================"
echo "Populate Vegas Lines"
echo "================================"
echo "App directory: $APP_DIR"
echo "NBA directory: $NBA_DIR"

# Activate virtual environment
cd "$APP_DIR"
source venv/bin/activate

# Run the Python script with proper PYTHONPATH
PYTHONPATH="$NBA_DIR" python -u "$SCRIPT_DIR/populate_vegas_lines.py"

echo ""
echo "Done."
