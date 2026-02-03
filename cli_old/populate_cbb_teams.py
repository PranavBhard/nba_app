#!/usr/bin/env python
"""Populate cbb_teams collection from ESPN API."""

import requests
import yaml
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from nba_app.core.mongo import Mongo


def load_league_config():
    config_path = Path(__file__).resolve().parents[1] / "leagues" / "cbb.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def fetch_teams():
    """Fetch all CBB teams from ESPN API."""
    url = "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams"
    params = {"limit": 500}

    all_teams = []
    page = 1

    while True:
        params["page"] = page
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

        teams = data.get("sports", [{}])[0].get("leagues", [{}])[0].get("teams", [])
        if not teams:
            break

        all_teams.extend(teams)

        # Check if there are more pages
        page_count = data.get("sports", [{}])[0].get("leagues", [{}])[0].get("pageCount", 1)
        if page >= page_count:
            break
        page += 1

    return all_teams


def main():
    config = load_league_config()
    collection_name = config["mongo"]["collections"]["teams"]

    print(f"Fetching teams from ESPN API...")
    teams_data = fetch_teams()
    print(f"Found {len(teams_data)} teams")

    # Transform to our schema (matching teams_nba structure)
    from datetime import datetime

    documents = []
    for item in teams_data:
        team = item.get("team", {})
        team_id = team.get("id")
        display_name = team.get("displayName")

        if not team_id or not display_name:
            continue

        # Extract primary logo URL
        logos = team.get("logos", [])
        logo_url = logos[0].get("href") if logos else None

        documents.append({
            "team_id": team_id,
            "id": team_id,
            "abbreviation": team.get("abbreviation"),
            "displayName": display_name,
            "shortDisplayName": team.get("shortDisplayName"),
            "name": team.get("name"),
            "location": team.get("location"),
            "slug": team.get("slug"),
            "uid": team.get("uid"),
            "color": team.get("color"),
            "alternateColor": team.get("alternateColor"),
            "logo": logo_url,
            "links": team.get("links", []),
            "nickname": team.get("nickname"),
            "isActive": team.get("isActive"),
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
        })

    print(f"Prepared {len(documents)} documents")

    # Insert into MongoDB
    db = Mongo()
    collection = db.db[collection_name]

    # Clear existing and insert new
    collection.delete_many({})
    if documents:
        result = collection.insert_many(documents)
        print(f"Inserted {len(result.inserted_ids)} documents into {collection_name}")

    # Create index on team_id
    collection.create_index("team_id", unique=True)
    print("Created unique index on team_id")

    # Show sample
    print("\nSample documents:")
    for doc in collection.find().limit(3):
        print(f"  {doc['team_id']}: {doc['displayName']} ({doc['abbreviation']}) - {doc['location']}")


if __name__ == "__main__":
    main()
