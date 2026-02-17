#!/bin/bash
#
# Populate Vegas betting lines in stats_nba collection
# Reads from nba_2008-2025.csv and adds vegas object to game documents
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "================================"
echo "Populate Vegas Lines"
echo "================================"
echo "Project root: $PROJECT_ROOT"

# Activate virtual environment
cd "$PROJECT_ROOT"
source venv/bin/activate

# Run the Python script with proper PYTHONPATH
PYTHONPATH="$PROJECT_ROOT" python -u "$SCRIPT_DIR/populate_vegas_lines.py"

echo ""
echo "Done."
