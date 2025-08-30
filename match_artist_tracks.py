#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to match artist names to their IDs and fetch their top 3 hottest tracks.
Outputs results as JSON.
"""

import orjson
from pyncm.apis.cloudsearch import GetSearchResult, ARTIST
from pyncm.apis.artist import GetArtistTracks

# Read artist names from artist.txt
with open("/home/da1sypetals/dev/pyncm/artist.txt", "r", encoding="utf-8") as file:
    artist_names = [line.strip() for line in file if line.strip()]

artists_data = []
processed_ids = set()

# Process each artist
for name in artist_names:
    print(f"Processing artist: {name}")

    # Search for artist ID
    search_result = GetSearchResult(name, stype=ARTIST, limit=1)
    if not search_result.get("result") or not search_result["result"].get("artists"):
        print(f"No artist found for: {name}")
        continue

    artist_id = search_result["result"]["artists"][0]["id"]

    # Skip if artist already processed
    if artist_id in processed_ids:
        print(f"Skipping duplicate artist ID: {artist_id}")
        continue

    processed_ids.add(artist_id)
    print(f"Found artist ID: {artist_id}")

    # Fetch top 3 hottest tracks
    tracks_result = GetArtistTracks(artist_id, limit=3, order="hot")
    if not tracks_result.get("songs"):
        print(f"No tracks found for artist ID: {artist_id}")
        continue

    # Prepare tracks data
    tracks = []
    for track in tracks_result["songs"][:3]:
        artists = track.get("artists", [{"name": "Unknown Artist"}])
        tracks.append({"name": track["name"], "artists": [ar["name"] for ar in artists]})

    # Add to artists data
    artists_data.append({"name": name, "id": artist_id, "top_tracks": tracks})

# Output as JSON
with open("artists_output.json", "wb") as f:
    f.write(orjson.dumps(artists_data, option=orjson.OPT_INDENT_2))

print("Data saved to artists_output.json")
