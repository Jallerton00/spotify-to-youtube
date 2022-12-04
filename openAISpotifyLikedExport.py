"""
This script imports the necessary libraries, reads in the user's Spotify credentials from a config file, and uses these
credentials to authenticate with the Spotify API. It then creates a DataFrame to store the user's liked songs,
retrieves the user's liked songs 50 at a time, adds the song information to the DataFrame, and saves the DataFrame as a
CSV file.
"""

import pandas as pd  # Import the pandas library for data manipulation
import spotipy  # Import the spotipy library for access to the Spotify API
from spotipy.oauth2 import SpotifyOAuth  # Import the SpotifyOAuth class for authentication

import config  # Import the config file containing user credentials

scope = "user-library-read"  # Set the required scope for accessing the user's saved tracks

# Read in the user's Spotify credentials from the config file
SPOTIFY_CLIENT_ID = config.SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET = config.SPOTIFY_CLIENT_SECRET
SPOTIFY_CLIENT_REDIRECT = config.SPOTIFY_CLIENT_REDIRECT


def export_liked_songs():
    # Authenticate with Spotify using the user's credentials
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET,
                                                   redirect_uri=SPOTIFY_CLIENT_REDIRECT, scope=scope))

    # Create a DataFrame with the appropriate columns for storing the liked songs
    df = pd.DataFrame(
        columns=[
            "song_name",  # The name of the song
            "artist",  # The artist(s) of the song
            "album",  # The album the song is from
            "release_date",  # The release date of the album
            "duration_ms",  # The duration of the song in milliseconds
            "popularity",  # The popularity of the song on Spotify
        ]
    )

    # Get the user's liked songs, 50 at a time (the maximum limit)
    for offset in range(0, 1500,
                        50):  # Loop through pages of saved tracks, starting at 0 and incrementing by 50 (max limit)
        liked_songs = sp.current_user_saved_tracks(limit=50,
                                                   offset=offset)  # Get the user's saved tracks for the current page

        for track in liked_songs["items"]:  # Loop through each track on the current page
            track_info = track["track"]  # Get the track information

            trackDF = pd.DataFrame.from_records([{  # Create a DataFrame for the current track
                "song_name": track_info["name"],  # The name of the song
                "artist": track_info["artists"][0]["name"],  # The artist(s) of the song
                "album": track_info["album"]["name"],  # The album the song is from
                "release_date": track_info["album"]["release_date"],  # The release date of the album
                "duration_ms": track_info["duration_ms"],  # The duration of the song in milliseconds
                "popularity": track_info["popularity"]  # The popularity of the song on Spotify
            }])
            df = pd.concat([df, trackDF])  # Add the current track's DataFrame to the main DataFrame

    # Save the DataFrame as a CSV file
    df.to_csv("liked_songs.csv",
              index=False)  # Save the DataFrame as a CSV file named "liked_songs.csv" without the index


export_liked_songs()
