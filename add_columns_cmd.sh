#!/bin/bash
# CLI command to add the columns (equivalent to UI)

cd /Users/pranav/Documents/NBA/nba_app
source venv/bin/activate

python cli/populate_master_training_cols.py \
  --columns "player_per_1|season|raw|home,player_per_1|season|raw|diff,player_per_1|season|raw|away,player_per_2|season|raw|home,player_per_2|season|raw|diff,player_per_2|season|raw|away,player_per_3|season|raw|home,player_per_3|season|raw|diff,player_per_3|season|raw|away,player_per|season|top1_avg|diff,player_per|season|top1_avg|home,player_per|season|top1_avg|away,player_per|season|top2_avg|diff,player_per|season|top2_avg|home,player_per|season|top2_avg|away,player_per|season|top3_avg|diff,player_per|season|top3_avg|home,player_per|season|top3_avg|away,player_per|season|top1_weighted_MPG|diff,player_per|season|top1_weighted_MPG|home,player_per|season|top1_weighted_MPG|away,player_per|season|top2_weighted_MPG|diff,player_per|season|top2_weighted_MPG|home,player_per|season|top2_weighted_MPG|away,player_per|season|top3_weighted_MPG|diff,player_per|season|top3_weighted_MPG|home,player_per|season|top3_weighted_MPG|away" \
  --overwrite \
  --chunk-size 1000
