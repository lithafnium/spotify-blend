#!/usr/bin/env python3
import os
import csv
import random
import spotipy
import time
import joblib
import numpy as np
import pandas as pd
import pprint
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.model_selection import GridSearchCV


features = [
    "mood",
    "acousticness",
    "danceability",
    "energy",
    "instrumentalness",
    "liveness",
    "loudness",
    "speechiness",
    "tempo",
    "valence",
    "mode",
]


def search_song(sp: spotipy.Spotify, title: str):
    results = sp.search(title, limit=10, type="track")
    if results is not None:
        track_id = results["tracks"]["items"][0]["id"]
        track_features = sp.audio_features(track_id)

        if track_features is not None and track_features[0] is not None:
            filtered = filter_features(track_features[0], features)
            return filtered
        else:
            return None
    else:
        return None


def filter_features(track_features, desired_features):
    ret = []

    for feature in desired_features:
        if feature in track_features:
            ret.append(track_features[feature])

    return ret


def get_playlist(sp: spotipy.Spotify, id: str):
    playlist_items = sp.playlist_items(id)

    audio_feautures = []

    print("playlist id:", id)

    while playlist_items:
        for i, track in enumerate(playlist_items["items"]):
            if track["track"] is None:
                continue

            track_id = track["track"]["id"]

            if track_id is None:
                continue

            track_features = sp.audio_features(track_id)
            if track_features is not None and track_features[0] is not None:
                filtered = filter_features(track_features[0], features)
                audio_feautures.append(filtered)

        if playlist_items["next"]:
            playlist_items = sp.next(playlist_items)
        else:
            playlist_items = None

    return audio_feautures


def write_to_csv(data):
    with open("data.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(features)
        csvwriter.writerows(data)


def setup():
    client_id = os.environ["SPOTIFY_CLIENT_ID"]
    client_secret = os.environ["SPOTIFY_CLIENT_SECRET"]
    cc_manager = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
    return spotipy.Spotify(client_credentials_manager=cc_manager)


def main():
    pp = pprint.PrettyPrinter(indent=4)
    sp = setup()
    # get_tracks = sp.search("don't stop me now", limit=10)
    # pp.pprint(get_tracks)
    # get_track = sp.track("7hQJA50XrCWABAu5v6QZ4i")
    # pp.pprint(get_track)
    # write_to_csv(audio_features)


if __name__ == "__main__":
    main()
