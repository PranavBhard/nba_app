# Project Instructions for Claude Code

## Python Environment
- Always run `source venv/bin/activate` before executing Python commands
- Use `python` (not `python3`) after activating the venv
- Set `PYTHONPATH=/Users/pranav/Documents/NBA` when running scripts that import `nba_app`

## MongoDB Access
- Use `from nba_app.cli.Mongo import Mongo` to connect to the database
- The Mongo wrapper handles connection details automatically

## Common Commands
```bash
# Activate venv and run Python
source venv/bin/activate && python script.py

# Run with proper PYTHONPATH
source venv/bin/activate && PYTHONPATH=/Users/pranav/Documents/NBA python script.py
```
