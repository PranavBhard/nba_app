"""
Date utility functions for parsing game times and date handling.
"""

from datetime import datetime
from typing import Optional

from pytz import utc


def parse_gametime(event_date_str: str) -> Optional[datetime]:
    """Parse event date string (already in UTC) and return as UTC datetime.

    The date field from ESPN API is already in UTC. We parse and store it as-is.
    """
    if not event_date_str:
        return None

    try:
        # Try parsing with fromisoformat first (handles ISO 8601 format with timezone)
        try:
            # Replace 'Z' with '+00:00' for UTC
            iso_str = event_date_str.replace('Z', '+00:00')
            dt = datetime.fromisoformat(iso_str)
            # Ensure it's UTC timezone-aware
            if dt.tzinfo is None:
                dt = utc.localize(dt)
            elif dt.tzinfo != utc:
                # Convert to UTC if it has a different timezone
                dt = dt.astimezone(utc)
            return dt
        except (ValueError, AttributeError):
            # Fallback: parse manually
            pass

        # Manual parsing fallback
        if 'T' in event_date_str:
            # Has time component
            date_part = event_date_str.split('T')[0]
            time_part = event_date_str.split('T')[1]

            # Remove timezone indicators (Z, +00:00, etc.) - date is already UTC
            if time_part.endswith('Z'):
                time_part = time_part[:-1]
            elif '+' in time_part:
                time_part = time_part.split('+')[0]
            elif '-' in time_part and time_part.count('-') > 1:
                # Check if last part is timezone offset (has :)
                parts = time_part.rsplit('-', 1)
                if len(parts) == 2 and ':' in parts[1]:
                    time_part = parts[0]

            # Parse the datetime
            dt_str = f"{date_part}T{time_part}"
            try:
                dt = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S')
            except ValueError:
                try:
                    dt = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.%f')
                except ValueError:
                    dt = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M')

            # Localize to UTC (date is already in UTC)
            dt_utc = utc.localize(dt)
            return dt_utc
        else:
            # Just date, assume midnight UTC
            dt = datetime.strptime(event_date_str, '%Y-%m-%d')
            dt_utc = utc.localize(dt)
            return dt_utc

    except Exception as e:
        print(f"  Warning: Could not parse gametime '{event_date_str}': {e}")
        return None
