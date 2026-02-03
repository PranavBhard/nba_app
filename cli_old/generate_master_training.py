#!/usr/bin/env python3
"""
Script to generate or regenerate the master training data CSV.

This script creates a master training CSV with ALL possible features.
Use this when:
- PER calculation logic changes (e.g., perWeighted weighting method)
- New features are added
- You need to rebuild the master from scratch

Usage:
    python cli/generate_master_training.py [--limit N]
    
    Options:
        --limit N    Limit the number of games to process (for testing).
                     When specified, output file will be named MASTER_TRAINING_limit-N.csv
                     instead of overwriting the master file.
"""

import sys
import os
import argparse
from datetime import datetime, timedelta

import logging
# Keep CLI output focused on progress; suppress debug noise from libraries
logging.basicConfig(level=logging.WARNING)

# Add project root to path
script_dir = os.path.dirname(os.path.abspath(__file__))
nba_app_dir = os.path.dirname(script_dir)
project_root = os.path.dirname(nba_app_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from nba_app.core.mongo import Mongo
from nba_app.cli_old.master_training_data import (
    generate_master_training_data,
    create_or_update_master_metadata,
    update_master_training_data_incremental,
    MASTER_TRAINING_PATH,
    get_master_training_path
)
from nba_app.core.league_config import load_league_config


def main():
    """Generate master training data CSV."""
    parser = argparse.ArgumentParser(
        description='Generate or regenerate the master training data CSV',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli/generate_master_training.py
  python cli/generate_master_training.py --limit 100
  python cli/generate_master_training.py --games 5,10,15 --months 1,2,3 --days 7,14
  python cli/generate_master_training.py --season 2023-2024 --skip-months 2
  python cli/generate_master_training.py --no-player --season 2023-2024
  python cli/generate_master_training.py --min-season 2008-2009
  python cli/generate_master_training.py --date-range 2024-01-01,2024-01-31
        """
    )
    parser.add_argument(
        '--league',
        type=str,
        default=os.environ.get("LEAGUE_ID", "nba"),
        help='League id to use (e.g., nba, cbb). Defaults to LEAGUE_ID env var or "nba".'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Limit the number of games to process (for testing). When specified, '
             'output file will be named MASTER_TRAINING_limit-N.csv instead of '
             'overwriting the master file.'
    )
    parser.add_argument(
        '--games',
        type=str,
        default=None,
        help='Comma-separated list of game window sizes (e.g., "5,10,15"). Defaults to [10] if not specified.'
    )
    parser.add_argument(
        '--months',
        type=str,
        default=None,
        help='Comma-separated list of month window sizes (e.g., "1,2,3"). Defaults to [1] if not specified.'
    )
    parser.add_argument(
        '--days',
        type=str,
        default=None,
        help='Comma-separated list of day window sizes (e.g., "7,14,30"). Defaults to [10] if not specified.'
    )
    parser.add_argument(
        '--season',
        type=str,
        default=None,
        help='Filter games by specific season (e.g., "2023-2024"). Must be in YYYY-YYYY format.'
    )
    parser.add_argument(
        '--min-season',
        type=str,
        default=None,
        help='Filter games by minimum season (e.g., "2008-2009"). Only includes games from this season or later. Must be in YYYY-YYYY format.'
    )
    parser.add_argument(
        '--skip-months',
        type=int,
        default=0,
        help='Skip the first N months of games in the season. Defaults to 0 (include all months).'
    )
    parser.add_argument(
        '--no-player',
        action='store_true',
        help='Skip player-level features (PER, injuries). This significantly speeds up generation by only including team-level features.'
    )
    parser.add_argument(
        '--date-range',
        type=str,
        default=None,
        help='Date range to regenerate (format: YYYY-MM-DD,YYYY-MM-DD). Removes existing rows in this range and regenerates them based on current columns.'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=None,
        help='Number of parallel workers for processing chunks. Defaults to CPU count if not specified.'
    )
    parser.add_argument(
        '-y', '--yes',
        action='store_true',
        help='Skip confirmation prompts (for automated/scripted runs).'
    )

    args = parser.parse_args()

    league = load_league_config(args.league)
    league_master_path = get_master_training_path(league)
    
    # Parse comma-separated lists
    games_list = None
    if args.games:
        try:
            games_list = [int(x.strip()) for x in args.games.split(',')]
        except ValueError:
            print(f"Error: Invalid --games format: {args.games}. Expected comma-separated integers.")
            return
    
    months_list = None
    if args.months:
        try:
            months_list = [int(x.strip()) for x in args.months.split(',')]
        except ValueError:
            print(f"Error: Invalid --months format: {args.months}. Expected comma-separated integers.")
            return
    
    days_list = None
    if args.days:
        try:
            days_list = [int(x.strip()) for x in args.days.split(',')]
        except ValueError:
            print(f"Error: Invalid --days format: {args.days}. Expected comma-separated integers.")
            return
    
    print("=" * 80)
    print("GENERATE MASTER TRAINING DATA")
    print("=" * 80)
    print()
    
    # Validate season format if provided
    if args.season:
        import re
        if not re.match(r'^\d{4}-\d{4}$', args.season):
            print(f"Error: Invalid --season format: {args.season}. Expected YYYY-YYYY format (e.g., '2023-2024').")
            return
    
    # Validate min_season format if provided
    if args.min_season:
        import re
        if not re.match(r'^\d{4}-\d{4}$', args.min_season):
            print(f"Error: Invalid --min-season format: {args.min_season}. Expected YYYY-YYYY format (e.g., '2008-2009').")
            return
    
    # Check that both --season and --min-season are not provided
    if args.season and args.min_season:
        print("Error: Cannot specify both --season and --min-season. Use --season for exact match or --min-season for minimum season filter.")
        return
    
    # Validate skip_months
    if args.skip_months < 0:
        print(f"Error: --skip-months must be >= 0. Got: {args.skip_months}")
        return
    
    # Parse and validate date range if provided
    start_date = None
    end_date = None
    if args.date_range:
        try:
            parts = args.date_range.split(',')
            if len(parts) != 2:
                print(f"Error: Invalid --date-range format: {args.date_range}. Expected YYYY-MM-DD,YYYY-MM-DD")
                return
            start_date_str = parts[0].strip()
            end_date_str = parts[1].strip()
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            if start_date > end_date:
                print(f"Error: Start date ({start_date_str}) must be <= end date ({end_date_str})")
                return
        except ValueError as e:
            print(f"Error: Invalid date format in --date-range: {args.date_range}. Use YYYY-MM-DD,YYYY-MM-DD")
            return
    
    # Display configuration
    config_items = []
    if games_list or months_list or days_list:
        config_items.append("Time Period Configuration:")
        if games_list:
            config_items.append(f"  Games windows: {games_list}")
        if months_list:
            config_items.append(f"  Months windows: {months_list}")
        if days_list:
            config_items.append(f"  Days windows: {days_list}")
    
    if args.season:
        config_items.append(f"Season filter: {args.season}")
    
    if args.min_season:
        config_items.append(f"Minimum season filter: {args.min_season} (and later)")
    
    if args.skip_months > 0:
        config_items.append(f"Skipping first {args.skip_months} months of games")
    
    if args.no_player:
        config_items.append("Player features: DISABLED (PER, injuries)")
    
    if args.date_range:
        config_items.append(f"Date range regeneration: {start_date} to {end_date}")
    
    if config_items:
        print("\n".join(config_items))
        print()
    
    # Determine output path
    if args.limit is not None and args.limit > 0:
        base_name = os.path.splitext(league_master_path)[0]
        output_path = f"{base_name}_limit-{args.limit}.csv"
        print(f"This will create a limited master training CSV with {args.limit} games.")
        print(f"Output file: {output_path}")
        print("(The actual master file will NOT be overwritten)")
    else:
        output_path = league_master_path
        print("This will create/regenerate the master training CSV with ALL possible features.")
        print(f"Output file: {output_path}")
    
    print()

    # Confirm (skip if --yes flag is set)
    if not args.yes:
        response = input("Continue? This may take a while. (y/N): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return

    print()
    print("Connecting to MongoDB...")
    mongo = Mongo()
    db = mongo.db
    print("Connected!")
    print()
    
    # Handle date range regeneration (remove and regenerate rows)
    if args.date_range:
        if not os.path.exists(league_master_path):
            print(f"Error: Master training CSV not found at {league_master_path}. Generate it first without --date-range.")
            return
        
        print(f"Regenerating rows for date range: {start_date} to {end_date}")
        print("This will:")
        print("  1. Remove existing rows in this date range from master CSV")
        print("  2. Regenerate training data columns for games in this date range")
        print("  3. Append regenerated rows back to master CSV")
        print()

        if not args.yes:
            response = input("Continue? (y/N): ")
            if response.lower() != 'y':
                print("Cancelled.")
                return
        
        print()
        print("Regenerating rows...")
        try:
            import pandas as pd
            
            # Read existing master CSV
            master_df = pd.read_csv(league_master_path)
            initial_count = len(master_df)
            
            # Convert date range to date strings for comparison
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')
            
            # Filter out rows in the date range
            # Create a date column for comparison
            def is_in_date_range(row):
                from datetime import date as date_class
                row_date = date_class(year=int(row['Year']), month=int(row['Month']), day=int(row['Day']))
                return start_date <= row_date <= end_date
            
            rows_to_remove = master_df.apply(is_in_date_range, axis=1)
            removed_count = rows_to_remove.sum()
            
            if removed_count > 0:
                print(f"Removing {removed_count} rows from date range {start_date_str} to {end_date_str}...")
                master_df_filtered = master_df[~rows_to_remove].copy()
                
                # Write filtered master (temporarily, will be overwritten)
                master_df_filtered.to_csv(league_master_path, index=False)
                print(f"Removed {removed_count} rows. {len(master_df_filtered)} rows remaining.")
            else:
                print(f"No rows found in date range {start_date_str} to {end_date_str}.")
                master_df_filtered = master_df
            
            # Regenerate rows for the date range using incremental update
            # Note: start_date should be exclusive, end_date inclusive for the incremental function
            # To include start_date, we use start_date - 1 day as exclusive
            exclusive_start_date = (start_date - timedelta(days=1)).strftime('%Y-%m-%d')
            
            print(f"Regenerating training data for date range {start_date_str} to {end_date_str}...")
            games_regenerated, updated_path = update_master_training_data_incremental(
                db,
                exclusive_start_date,
                end_date_str,
                league_master_path,
                league=league,
            )
            
            if games_regenerated > 0:
                print(f"Regenerated {games_regenerated} games for date range {start_date_str} to {end_date_str}")
            else:
                print(f"No games found in MongoDB for date range {start_date_str} to {end_date_str}")
            
            # Read final master CSV to get final count
            final_df = pd.read_csv(league_master_path)
            final_count = len(final_df)
            
            print()
            print("=" * 80)
            print("DATE RANGE REGENERATION COMPLETE")
            print("=" * 80)
            print(f"Rows removed: {removed_count}")
            print(f"Rows regenerated: {games_regenerated}")
            print(f"Initial row count: {initial_count}")
            print(f"Final row count: {final_count}")
            print(f"Master CSV: {league_master_path}")
            print()
            
        except Exception as e:
            import traceback
            print()
            print("=" * 80)
            print("ERROR")
            print("=" * 80)
            print(f"Failed to regenerate date range: {e}")
            print()
            traceback.print_exc()
            sys.exit(1)
        
        return
    
    if args.limit:
        print(f"Generating limited master training data ({args.limit} games)...")
    else:
        print("Generating master training data...")
        print("(This may take several minutes depending on the number of games)")
    print()
    
    # Progress callback with ETA and throughput; throttled to avoid spam
    # Note: The callback receives different patterns:
    # Pattern 1: (increment, skipped, total) - from _process_game_chunk
    # Pattern 2: (current, total, progress_pct) - from log_progress_if_needed/chunk completion
    import time
    start_time = time.time()
    last_print_ts = 0.0
    last_cumulative = 0  # Track last cumulative value
    cumulative_current = 0  # Track cumulative progress internally
    total_games = None  # Will be set from first callback
    
    def progress_callback(arg1, arg2, arg3):
        nonlocal last_print_ts, last_cumulative, cumulative_current, total_games
        now = time.time()
        elapsed = now - start_time
        
        # Detect calling pattern:
        # Pattern 1: (increment, skipped, total) - from _process_game_chunk
        #   - arg1: increment (int, small number like 10, 50, etc.)
        #   - arg2: skipped (int, 0 or 1)
        #   - arg3: total (int, large number like 501)
        # Pattern 2: (current, total, progress_pct) - from log_progress_if_needed/chunk completion
        #   - arg1: current (int, cumulative count)
        #   - arg2: total (int, same as Pattern 1's arg3)
        #   - arg3: progress_pct (float, 0-100)
        
        # Strict detection: Pattern 2 only if arg3 is clearly a percentage (0-100)
        # AND arg2 is a reasonable total (>= 10, typically hundreds)
        # AND arg1 <= arg2 (current can't exceed total)
        is_pattern2 = (
            isinstance(arg3, (int, float)) and 
            0 <= arg3 <= 100 and
            isinstance(arg2, (int, float)) and
            arg2 >= 10 and  # Total should be at least 10
            isinstance(arg1, (int, float)) and
            arg1 <= arg2  # Current can't exceed total
        )
        
        if is_pattern2:
            # Pattern 2: (current, total, progress_pct) - cumulative values
            current = int(arg1)
            total = int(arg2)
            progress_pct = float(arg3)
            cumulative_current = current
            if total_games is None or total_games != total:
                total_games = total
        else:
            # Pattern 1: (increment, skipped, total) - incremental values
            increment = int(arg1) if arg1 else 0
            skipped = int(arg2) if arg2 else 0
            total = int(arg3) if arg3 else (total_games or 0)
            
            if total_games is None and total > 0:
                total_games = total
            
            cumulative_current += increment
            if skipped > 0:
                cumulative_current += skipped
            
            # Cap cumulative_current at total to avoid >100%
            cumulative_current = min(cumulative_current, total_games or total)
            progress_pct = (cumulative_current / (total_games or total)) * 100 if (total_games or total) > 0 else 0
        
        # Use total_games (should be set by now)
        effective_total = total_games or 501  # Fallback if somehow not set
        
        # Stop printing if we've already reached 100% and printed it
        if cumulative_current >= effective_total and last_cumulative >= effective_total:
            return  # Already at 100%, don't print again
        
        # Compute instantaneous rate over last interval
        delta_items = max(0, cumulative_current - last_cumulative)
        delta_time = max(1e-6, now - (last_print_ts or start_time))
        inst_rate = delta_items / delta_time
        avg_rate = cumulative_current / max(1e-6, elapsed)
        remaining = max(0, (effective_total - cumulative_current))
        eta_sec = remaining / avg_rate if avg_rate > 0 else 0
        
        # Throttle to ~every 2s, but always print at completion (once) and key milestones
        should_print = (
            (now - last_print_ts >= 2.0) or 
            (cumulative_current >= effective_total and last_cumulative < effective_total) or  # Print once when reaching 100%
            cumulative_current == 1 or 
            (effective_total > 0 and cumulative_current % max(1, effective_total // 10) == 0)
        )
        if should_print:
            eta_str = time.strftime('%H:%M:%S', time.gmtime(eta_sec)) if cumulative_current < effective_total else '00:00:00'
            elapsed_str = time.strftime('%H:%M:%S', time.gmtime(elapsed))
            # Clamp progress_pct to 0-100 for display
            display_pct = min(100.0, max(0.0, progress_pct))
            print(f"  Progress: {cumulative_current}/{effective_total} ({display_pct:.1f}%) | avg {avg_rate:.1f}/s | inst {inst_rate:.1f}/s | elapsed {elapsed_str} | ETA {eta_str}")
            last_print_ts = now
            last_cumulative = cumulative_current
    
    try:
        # Generate master training data
        csv_path, feature_list, game_count = generate_master_training_data(
            query=None,  # Uses default query
            output_path=output_path,
            progress_callback=progress_callback,
            limit=args.limit,
            games_list=games_list,
            months_list=months_list,
            days_list=days_list,
            season=args.season,
            min_season=args.min_season,
            skip_months=args.skip_months,
            no_player=args.no_player,
            league=league,
            max_workers=args.workers,
        )
        
        end_time = __import__('time').time()
        total_elapsed = end_time - start_time
        print()
        print("=" * 80)
        print("MASTER TRAINING DATA GENERATED")
        print("=" * 80)
        print(f"File: {csv_path}")
        print(f"Games: {game_count}")
        print(f"Features: {len(feature_list)}")
        print(f"Elapsed: {time.strftime('%H:%M:%S', time.gmtime(total_elapsed))} | Avg throughput: {game_count / max(1e-6, total_elapsed):.1f} games/s")
        print()
        
        # Get latest date from the CSV
        import pandas as pd
        df = pd.read_csv(csv_path)
        if len(df) > 0:
            df_sorted = df.sort_values(['Year', 'Month', 'Day'], ascending=False)
            latest_row = df_sorted.iloc[0]
            last_date = f"{int(latest_row['Year'])}-{int(latest_row['Month']):02d}-{int(latest_row['Day']):02d}"
        else:
            last_date = datetime.now().strftime('%Y-%m-%d')
        
        # Update metadata in MongoDB only if not using limit (limit files are for testing)
        if args.limit is None or args.limit <= 0:
            print("Updating metadata in MongoDB...")
            options = {
                'regenerated': True,
                'regenerated_at': datetime.utcnow().isoformat(),
                'games_list': games_list or [10],
                'months_list': months_list or [1],
                'days_list': days_list or [10],
                'season': args.season,
                'min_season': args.min_season,
                'skip_months': args.skip_months,
                'no_player': args.no_player
            }
            metadata_id = create_or_update_master_metadata(
                db,
                csv_path,
                feature_list,
                len(feature_list),
                last_date,
                options=options,
                league=league,
            )
            print(f"Metadata updated (ID: {metadata_id})")
            print()
        
        print("=" * 80)
        print("SUCCESS!")
        print("=" * 80)
        print(f"Training data is ready at: {csv_path}")
        if args.limit is None or args.limit <= 0:
            print("You can now use this for training with the 'Use Cached Master Training Data' option.")
        else:
            print(f"(Limited to {args.limit} games - master file not overwritten)")
        print()
        
    except Exception as e:
        import traceback
        print()
        print("=" * 80)
        print("ERROR")
        print("=" * 80)
        print(f"Failed to generate master training data: {e}")
        print()
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

