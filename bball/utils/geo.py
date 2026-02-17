#!/usr/bin/env python3
"""
Geocoding utility for NBA venues.

Provides helper functions for geocoding venues using Nominatim.
These functions can be imported and used by other scripts.
"""

import sys
import os

# Add project root to path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError, GeocoderInsufficientPrivileges
import json
import argparse


def get_geocoder():
    """Get a configured Nominatim geocoder instance."""
    return Nominatim(
        user_agent="NBA_Analytics_App/1.0",
        timeout=10
    )


def get_venue_from_json(venue_name):
    """Try to get venue coordinates from nba_venues.json"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, '../cli/nba_venues.json')
    
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            venues = json.load(f)
            for venue in venues:
                if venue_name.lower() in venue['fullName'].lower():
                    return venue['lat'], venue['lon'], venue['fullName']
    return None, None, None


def geocode_venue(query, geolocator=None):
    """
    Geocode a venue query string using Nominatim.
    
    Args:
        query: Query string to geocode (e.g., "Delta Center, Salt Lake City, UT")
        geolocator: Optional geocoder instance. If None, creates a new one.
    
    Returns:
        Tuple of (lat, lon) or (None, None) if failed.
    """
    if geolocator is None:
        geolocator = get_geocoder()
    
    try:
        location = geolocator.geocode(query)
        if location:
            return location.latitude, location.longitude
        return None, None
    except (GeocoderTimedOut, GeocoderServiceError, GeocoderInsufficientPrivileges) as e:
        print(f"  ⚠ Geocoding error: {e}")
        return None, None
    except Exception as e:
        print(f"  ⚠ Unexpected error: {e}")
        return None, None


def test_geocoding():
    """Test geocoding with a single venue (for command-line testing)."""
    venue_query = "Delta Center, Salt Lake City, UT"
    
    geolocator = get_geocoder()
    
    print("Testing geocoding with:", venue_query)
    print("-" * 70)
    
    try:
        location = geolocator.geocode(venue_query)
        if location:
            print(f"✓ Geocoded via Nominatim")
            print(f"Latitude: {location.latitude}, Longitude: {location.longitude}")
            print(f"Full address: {location.address}")
        else:
            print("Location not found via geocoding. Checking local venue database...")
            lat, lon, name = get_venue_from_json("Delta Center")
            if lat and lon:
                print(f"✓ Found in local database")
                print(f"Venue: {name}")
                print(f"Latitude: {lat}, Longitude: {lon}")
            else:
                print("Location not found in either geocoding service or local database.")
    except GeocoderInsufficientPrivileges:
        print("⚠ Geocoding service returned 403 (rate limited or blocked).")
        print("Falling back to local venue database...")
        lat, lon, name = get_venue_from_json("Delta Center")
        if lat and lon:
            print(f"✓ Found in local database")
            print(f"Venue: {name}")
            print(f"Latitude: {lat}, Longitude: {lon}")
        else:
            print("Location not found in local database.")
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"⚠ Geocoding service error: {e}")
        print("Falling back to local venue database...")
        lat, lon, name = get_venue_from_json("Delta Center")
        if lat and lon:
            print(f"✓ Found in local database")
            print(f"Venue: {name}")
            print(f"Latitude: {lat}, Longitude: {lon}")
        else:
            print("Location not found in local database.")
    except Exception as e:
        print(f"Error: {e}")
        print("Falling back to local venue database...")
        lat, lon, name = get_venue_from_json("Delta Center")
        if lat and lon:
            print(f"✓ Found in local database")
            print(f"Venue: {name}")
            print(f"Latitude: {lat}, Longitude: {lon}")
        else:
            print("Location not found in local database.")


def main():
    """Command-line entry point for testing geocoding."""
    parser = argparse.ArgumentParser(
        description='Geocoding utility for NBA venues',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/geo.py  # Test geocoding a single venue
        """
    )
    
    args = parser.parse_args()
    test_geocoding()


if __name__ == '__main__':
    main()
