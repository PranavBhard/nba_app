#!/usr/bin/env python
import sys
import os

# Add project root to path
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

import json
from bball.mongo import Mongo
from bson import json_util

db = Mongo().client.nba

# Get selected model config
config = db.model_config_nba.find_one({'selected': True})

if config:
    print(json.dumps(json.loads(json_util.dumps(config)), indent=2, default=str))
else:
    print("No selected config found")
