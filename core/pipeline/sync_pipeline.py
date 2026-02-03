#!/usr/bin/env python3
"""
Data sync pipeline for pulling ESPN data into MongoDB.

Pulls/upserts ESPN data (games, players, venues, rosters, teams) into MongoDB
with flexible date filtering and data type selection.

Usage:
    python -m nba_app.core.pipeline.sync_pipeline nba --date 2024-01-15
    python -m nba_app.core.pipeline.sync_pipeline cbb --date-range 2024-01-01,2024-01-31
    python -m nba_app.core.pipeline.sync_pipeline nba --season 2024-2025
    python -m nba_app.core.pipeline.sync_pipeline nba --season 2024-2025 --with-injuries
"""

import argparse
import subprocess
import sys
import os
import time
from datetime import datetime, date, timedelta
from typing import List, Optional, Set

# Add project root to path for direct execution
script_dir = os.path.dirname(os.path.abspath(__file__))
nba_app_dir = os.path.dirname(os.path.dirname(script_dir))
project_root = os.path.dirname(nba_app_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from nba_app.core.league_config import load_league_config, get_available_leagues, LeagueConfig
from nba_app.core.mongo import Mongo


# Valid data types for sync
VALID_DATA_TYPES = {'games', 'players', 'player_stats', 'venues', 'rosters', 'teams'}


def parse_date(date_str: str) -> date:
    """Parse date string in YYYY-MM-DD format."""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD")


def parse_date_range(date_str: str) -> tuple:
    """Parse date range string like 'YYYY-MM-DD,YYYY-MM-DD' and return (start, end)."""
    parts = date_str.split(',')
    if len(parts) != 2:
        raise ValueError(f"Invalid date range format: {date_str}. Use YYYY-MM-DD,YYYY-MM-DD")

    start = parse_date(parts[0].strip())
    end = parse_date(parts[1].strip())

    if start > end:
        raise ValueError(f"Start date must be before end date: {start} > {end}")

    return start, end


def parse_season(season_str: str, league_config: LeagueConfig) -> tuple:
    """
    Parse season string like 'YYYY-YYYY' and return (start_date, end_date).

    Uses league config for season start/end month/day.
    """
    parts = season_str.split('-')
    if len(parts) != 2:
        raise ValueError(f"Invalid season format: {season_str}. Use YYYY-YYYY (e.g., 2024-2025)")

    try:
        start_year = int(parts[0])
        end_year = int(parts[1])
    except ValueError:
        raise ValueError(f"Invalid season years: {season_str}. Use YYYY-YYYY")

    if end_year != start_year + 1:
        raise ValueError(f"Season must span consecutive years: {season_str}")

    # Build dates from league config
    start_date = date(
        start_year,
        league_config.season_start_month,
        league_config.season_start_day
    )
    end_date = date(
        end_year,
        league_config.season_end_month,
        league_config.season_end_day
    )

    # For current season, cap at today if before season end
    today = date.today()
    if end_date > today:
        end_date = today

    return start_date, end_date


def parse_data_types(types_str: str) -> Set[str]:
    """Parse comma-separated data types."""
    types = set()
    for t in types_str.split(','):
        t = t.strip().lower()
        if t not in VALID_DATA_TYPES:
            raise ValueError(f"Invalid data type: {t}. Valid types: {', '.join(sorted(VALID_DATA_TYPES))}")
        types.add(t)
    return types


def run_espn_pull(
    league_config: LeagueConfig,
    start_date: date,
    end_date: date,
    dry_run: bool = False,
    verbose: bool = False
) -> dict:
    """
    Run ESPN data pull for a date range.

    Returns dict with statistics.
    """
    # Convert dates to ESPN format (YYYYMMDD,YYYYMMDD)
    date_str = f"{start_date.strftime('%Y%m%d')},{end_date.strftime('%Y%m%d')}"

    cmd = [
        sys.executable, "cli_old/espn_api.py",
        "--league", league_config.league_id,
        "--dates", date_str
    ]

    if dry_run:
        cmd.append("--dry-run")

    if verbose:
        print(f"  Running: {' '.join(cmd)}")

    stats = {
        'games_processed': 0,
        'players_processed': 0,
        'success': False,
        'error': None
    }

    try:
        env = {**os.environ, "PYTHONPATH": project_root, "PYTHONUNBUFFERED": "1"}
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd=nba_app_dir,
            env=env
        )

        for line in process.stdout:
            line = line.strip()
            if verbose:
                print(f"    {line}")

            # Parse progress from output
            line_lower = line.lower()
            if "stored game" in line_lower or "would store game" in line_lower:
                stats['games_processed'] += 1
            elif "player stats" in line_lower:
                import re
                match = re.search(r'(\d+)\s*player\s*stats', line_lower)
                if match:
                    stats['players_processed'] += int(match.group(1))

        process.wait()
        stats['success'] = process.returncode == 0
        if not stats['success']:
            stats['error'] = f"Exit code: {process.returncode}"

    except Exception as e:
        stats['error'] = str(e)

    return stats


def run_post_processing(
    league_config: LeagueConfig,
    data_types: Set[str],
    dry_run: bool = False,
    verbose: bool = False
) -> dict:
    """
    Run post-processing steps (venues, players).

    Returns dict with step results.
    """
    results = {}

    if 'venues' in data_types:
        print("  Refreshing venues...")
        cmd = [
            sys.executable, "cli_old/espn_api.py",
            "--league", league_config.league_id,
            "--refresh-venues"
        ]
        if dry_run:
            cmd.append("--dry-run")

        try:
            result = subprocess.run(
                cmd,
                cwd=nba_app_dir,
                env={**os.environ, "PYTHONPATH": project_root},
                capture_output=True,
                text=True,
                check=True
            )
            results['venues'] = {'success': True}
            if verbose:
                print(f"    {result.stdout[:500] if result.stdout else 'Done'}")
        except subprocess.CalledProcessError as e:
            results['venues'] = {'success': False, 'error': e.stderr[:200] if e.stderr else str(e)}

    if 'players' in data_types:
        print("  Refreshing players metadata...")
        cmd = [
            sys.executable, "cli_old/espn_api.py",
            "--league", league_config.league_id,
            "--refresh-players"
        ]
        if dry_run:
            cmd.append("--dry-run")

        try:
            result = subprocess.run(
                cmd,
                cwd=nba_app_dir,
                env={**os.environ, "PYTHONPATH": project_root},
                capture_output=True,
                text=True,
                check=True
            )
            results['players'] = {'success': True}
            if verbose:
                print(f"    {result.stdout[:500] if result.stdout else 'Done'}")
        except subprocess.CalledProcessError as e:
            results['players'] = {'success': False, 'error': e.stderr[:200] if e.stderr else str(e)}

    return results


def run_injuries(
    league_config: LeagueConfig,
    start_date: date = None,
    end_date: date = None,
    dry_run: bool = False,
    verbose: bool = False
) -> dict:
    """
    Run injury computation.

    Returns dict with statistics.
    """
    print("  Computing injuries...")

    cmd = [
        sys.executable, "-m", "nba_app.core.pipeline.injuries_pipeline",
        league_config.league_id
    ]

    if start_date and end_date:
        cmd.extend(["--date-range", f"{start_date.strftime('%Y-%m-%d')},{end_date.strftime('%Y-%m-%d')}"])

    if dry_run:
        cmd.append("--dry-run")

    if verbose:
        cmd.append("--verbose")

    try:
        result = subprocess.run(
            cmd,
            cwd=nba_app_dir,
            env={**os.environ, "PYTHONPATH": project_root},
            capture_output=True,
            text=True,
            check=True
        )
        if verbose:
            for line in result.stdout.split('\n')[:20]:
                print(f"    {line}")
        return {'success': True}
    except subprocess.CalledProcessError as e:
        return {'success': False, 'error': e.stderr[:200] if e.stderr else str(e)}


def run_elo_cache(
    league_config: LeagueConfig,
    dry_run: bool = False,
    verbose: bool = False
) -> dict:
    """
    Run ELO cache refresh.

    Returns dict with result.
    """
    print("  Caching ELO ratings...")

    cmd = [
        sys.executable, "cli_old/cache_elo_ratings.py",
        "--league", league_config.league_id
    ]

    if dry_run:
        print(f"    [DRY RUN] Would run: {' '.join(cmd)}")
        return {'success': True, 'dry_run': True}

    try:
        result = subprocess.run(
            cmd,
            cwd=nba_app_dir,
            env={**os.environ, "PYTHONPATH": project_root},
            capture_output=True,
            text=True,
            check=True
        )
        if verbose:
            print(f"    Done")
        return {'success': True}
    except subprocess.CalledProcessError as e:
        return {'success': False, 'error': e.stderr[:200] if e.stderr else str(e)}


def run_venue_geocoding(
    league_config: LeagueConfig,
    dry_run: bool = False,
    verbose: bool = False
) -> dict:
    """
    Geocode venues that don't have location data.

    Uses Nominatim geocoding service with rate limiting.

    Returns dict with statistics.
    """
    from nba_app.tools.geo import get_geocoder, geocode_venue

    print("  Geocoding venues without location...")

    # Get league-specific venues collection
    mongo = Mongo()
    venues_collection_name = f"{league_config.league_id}_venues"
    venues_collection = mongo.db[venues_collection_name]

    # Find venues without location
    venues_without_location = list(venues_collection.find(
        {'location': {'$exists': False}},
        {'venue_guid': 1, 'fullName': 1, 'address': 1}
    ))

    total = venues_collection.count_documents({})
    with_location = venues_collection.count_documents({'location': {'$exists': True}})

    print(f"    Collection: {venues_collection_name}")
    print(f"    Total venues: {total}")
    print(f"    Already geocoded: {with_location}")
    print(f"    Need geocoding: {len(venues_without_location)}")

    if not venues_without_location:
        return {
            'success': True,
            'total': total,
            'already_geocoded': with_location,
            'geocoded': 0,
            'failed': 0
        }

    # Initialize geocoder
    geolocator = get_geocoder()

    geocoded_count = 0
    failed_count = 0

    for i, venue in enumerate(venues_without_location, 1):
        venue_guid = venue.get('venue_guid')
        full_name = venue.get('fullName')
        address = venue.get('address') or {}

        city = address.get('city', '') if isinstance(address, dict) else ''
        state = address.get('state', '') if isinstance(address, dict) else ''

        if not full_name:
            if verbose:
                print(f"    [{i}/{len(venues_without_location)}] Skipping (no fullName)")
            failed_count += 1
            continue

        # Build query string
        query_parts = [full_name]
        if city:
            query_parts.append(city)
        if state:
            query_parts.append(state)
        venue_query = ", ".join(query_parts)

        if verbose:
            print(f"    [{i}/{len(venues_without_location)}] {venue_query}...", end=' ')

        # Rate limiting - Nominatim allows ~1 request/second
        if i > 1:
            time.sleep(1.1)

        lat, lon = geocode_venue(venue_query, geolocator)

        if lat and lon:
            location = {'lat': lat, 'lon': lon}

            if dry_run:
                if verbose:
                    print(f"would set lat={lat:.4f}, lon={lon:.4f}")
                geocoded_count += 1
            else:
                result = venues_collection.update_one(
                    {'venue_guid': venue_guid},
                    {'$set': {'location': location}}
                )
                if result.modified_count > 0:
                    if verbose:
                        print(f"OK lat={lat:.4f}, lon={lon:.4f}")
                    geocoded_count += 1
                else:
                    if verbose:
                        print("update failed")
                    failed_count += 1
        else:
            if verbose:
                print("geocoding failed")
            failed_count += 1

    print(f"    Geocoded: {geocoded_count}, Failed: {failed_count}")

    return {
        'success': True,
        'total': total,
        'already_geocoded': with_location,
        'geocoded': geocoded_count,
        'failed': failed_count
    }


def run_sync_pipeline(
    league_config: LeagueConfig,
    start_date: date,
    end_date: date,
    data_types: Set[str] = None,
    skip_types: Set[str] = None,
    with_injuries: bool = False,
    with_elo: bool = False,
    with_geocoding: bool = False,
    workers: int = 4,
    dry_run: bool = False,
    verbose: bool = False
) -> dict:
    """
    Run the full sync pipeline.

    Args:
        league_config: League configuration
        start_date: Start date for sync
        end_date: End date for sync
        data_types: Set of data types to sync (default: all)
        skip_types: Set of data types to skip
        with_injuries: Compute injuries after sync
        with_elo: Update ELO cache after sync
        with_geocoding: Geocode venues without location data
        workers: Number of parallel workers
        dry_run: Preview without database changes
        verbose: Detailed output

    Returns:
        Dict with pipeline statistics
    """
    pipeline_start = time.time()

    # Determine active data types
    active_types = data_types or VALID_DATA_TYPES.copy()
    if skip_types:
        active_types = active_types - skip_types

    # Calculate date range info
    days = (end_date - start_date).days + 1

    print(f"\n{'='*60}")
    print(f"  {league_config.display_name} Data Sync")
    print(f"{'='*60}")
    print(f"  Date range:      {start_date} to {end_date} ({days} days)")
    print(f"  Data types:      {', '.join(sorted(active_types))}")
    print(f"  With injuries:   {with_injuries}")
    print(f"  With ELO:        {with_elo}")
    print(f"  With geocoding:  {with_geocoding}")
    print(f"  Dry run:         {dry_run}")
    print(f"{'='*60}\n")

    results = {
        'steps': {},
        'success': True,
        'total_time': 0
    }

    # Step 1: ESPN data pull (games, player_stats)
    if 'games' in active_types or 'player_stats' in active_types:
        step_name = "ESPN Data Pull"
        print(f"[1] {step_name}...")

        step_start = time.time()
        espn_stats = run_espn_pull(
            league_config,
            start_date,
            end_date,
            dry_run=dry_run,
            verbose=verbose
        )
        step_time = time.time() - step_start

        results['steps']['espn_pull'] = {
            **espn_stats,
            'time': step_time
        }

        print(f"    Games: {espn_stats['games_processed']:,}")
        print(f"    Players: {espn_stats['players_processed']:,}")
        print(f"    Time: {step_time:.1f}s")

        if not espn_stats['success']:
            print(f"    Warning: {espn_stats.get('error', 'Unknown error')}")
            results['success'] = False

    # Step 2: Post-processing (venues, players metadata)
    post_types = active_types & {'venues', 'players'}
    if post_types:
        step_name = "Post-Processing"
        print(f"\n[2] {step_name}...")

        step_start = time.time()
        post_stats = run_post_processing(
            league_config,
            post_types,
            dry_run=dry_run,
            verbose=verbose
        )
        step_time = time.time() - step_start

        results['steps']['post_processing'] = {
            **post_stats,
            'time': step_time
        }

        for dtype, status in post_stats.items():
            status_str = "OK" if status.get('success') else f"FAILED: {status.get('error', 'Unknown')}"
            print(f"    {dtype}: {status_str}")
        print(f"    Time: {step_time:.1f}s")

    # Step 3: Venue Geocoding (optional)
    if with_geocoding and 'venues' in active_types:
        step_name = "Venue Geocoding"
        print(f"\n[3] {step_name}...")

        step_start = time.time()
        geocoding_stats = run_venue_geocoding(
            league_config,
            dry_run=dry_run,
            verbose=verbose
        )
        step_time = time.time() - step_start

        results['steps']['venue_geocoding'] = {
            **geocoding_stats,
            'time': step_time
        }

        print(f"    Time: {step_time:.1f}s")

    # Step 4: Injuries (optional)
    if with_injuries:
        step_name = "Injury Computation"
        print(f"\n[4] {step_name}...")

        step_start = time.time()
        injury_stats = run_injuries(
            league_config,
            start_date=start_date,
            end_date=end_date,
            dry_run=dry_run,
            verbose=verbose
        )
        step_time = time.time() - step_start

        results['steps']['injuries'] = {
            **injury_stats,
            'time': step_time
        }

        status_str = "OK" if injury_stats.get('success') else f"FAILED: {injury_stats.get('error', 'Unknown')}"
        print(f"    Status: {status_str}")
        print(f"    Time: {step_time:.1f}s")

    # Step 5: ELO (optional)
    if with_elo:
        step_name = "ELO Cache"
        print(f"\n[5] {step_name}...")

        step_start = time.time()
        elo_stats = run_elo_cache(
            league_config,
            dry_run=dry_run,
            verbose=verbose
        )
        step_time = time.time() - step_start

        results['steps']['elo_cache'] = {
            **elo_stats,
            'time': step_time
        }

        status_str = "OK" if elo_stats.get('success') else f"FAILED: {elo_stats.get('error', 'Unknown')}"
        print(f"    Status: {status_str}")
        print(f"    Time: {step_time:.1f}s")

    # Summary
    total_time = time.time() - pipeline_start
    results['total_time'] = total_time

    print(f"\n{'='*60}")
    print(f"  Sync Complete!")
    print(f"{'='*60}")
    print(f"  Total time: {total_time:.1f}s")
    if dry_run:
        print(f"  Mode: DRY RUN (no changes made)")
    print(f"{'='*60}\n")

    return results


def main():
    available_leagues = get_available_leagues()

    parser = argparse.ArgumentParser(
        description="Pull/upsert ESPN data into MongoDB",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python -m nba_app.core.pipeline.sync_pipeline nba --date 2024-01-15
    python -m nba_app.core.pipeline.sync_pipeline cbb --date-range 2024-01-01,2024-01-31
    python -m nba_app.core.pipeline.sync_pipeline nba --season 2024-2025
    python -m nba_app.core.pipeline.sync_pipeline nba --season 2024-2025 --with-injuries
    python -m nba_app.core.pipeline.sync_pipeline nba --only games,player_stats --dry-run

Data Types:
    games           Game box scores from ESPN scoreboard
    players         Player metadata
    player_stats    Individual player game stats
    venues          Arena/venue information
    rosters         Team rosters
    teams           Team metadata
        """
    )

    # Positional argument
    parser.add_argument(
        "league",
        choices=available_leagues,
        help=f"League to sync ({', '.join(available_leagues)})"
    )

    # Date filtering (mutually exclusive)
    date_group = parser.add_mutually_exclusive_group(required=True)
    date_group.add_argument(
        "--date",
        type=str,
        help="Single date (YYYY-MM-DD)"
    )
    date_group.add_argument(
        "--date-range",
        type=str,
        help="Date range (YYYY-MM-DD,YYYY-MM-DD)"
    )
    date_group.add_argument(
        "--season",
        type=str,
        help="Entire season (YYYY-YYYY)"
    )

    # Data selection
    parser.add_argument(
        "--only",
        type=str,
        help="Only sync specific data types (comma-separated)"
    )
    parser.add_argument(
        "--skip",
        type=str,
        help="Skip specific data types (comma-separated)"
    )

    # Post-processing
    parser.add_argument(
        "--with-injuries",
        action="store_true",
        help="Compute injuries after sync"
    )
    parser.add_argument(
        "--with-elo",
        action="store_true",
        help="Update ELO cache after sync"
    )
    parser.add_argument(
        "--with-geocoding",
        action="store_true",
        help="Geocode venues without location data (uses Nominatim, rate-limited)"
    )

    # Common options
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Parallel workers (default: 4)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview without database changes"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Detailed output"
    )

    args = parser.parse_args()

    # Load league config
    league_config = load_league_config(args.league)

    # Parse date arguments
    if args.date:
        start_date = parse_date(args.date)
        end_date = start_date
    elif args.date_range:
        start_date, end_date = parse_date_range(args.date_range)
    elif args.season:
        start_date, end_date = parse_season(args.season, league_config)

    # Parse data types
    data_types = None
    skip_types = None

    if args.only:
        data_types = parse_data_types(args.only)

    if args.skip:
        skip_types = parse_data_types(args.skip)

    # Run pipeline
    try:
        results = run_sync_pipeline(
            league_config=league_config,
            start_date=start_date,
            end_date=end_date,
            data_types=data_types,
            skip_types=skip_types,
            with_injuries=args.with_injuries,
            with_elo=args.with_elo,
            with_geocoding=args.with_geocoding,
            workers=args.workers,
            dry_run=args.dry_run,
            verbose=args.verbose
        )

        return 0 if results['success'] else 1

    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
