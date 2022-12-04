"""
This code imports the necessary libraries and reads in the user's YouTube playlist ID from a config file.
It then reads in the user's liked songs from a CSV file, creates an empty DataFrame to store tracks that could not be
added to the playlist, and loops through the liked songs. For each song, it searches for the song on YouTube Music and
attempts to add it to the user's playlist. If the search does not return a result or the song cannot be added to the
playlist, the track's information is added to the empty DataFrame. Finally, the DataFrame of tracks that could not be
added to the playlist is saved as a CSV file.
"""

import pandas as pd  # Import the pandas library for data manipulation
from ytmusicapi import YTMusic  # Import the ytmusicapi library for accessing YouTube Music

import config  # Import the config file containing the user's playlist ID

ytMusic = YTMusic('ytAuth.json')  # Authenticate with YouTube Music using the user's credentials stored in a JSON file

playlistId = config.playlistId  # Read in the user's YouTube Music playlist ID from the config file

spotifyLiked = pd.read_csv("liked_songs.csv", header=0)  # Read in the user's liked songs from a CSV file

noVideoID = pd.DataFrame(columns=spotifyLiked.columns)  # Create an empty DataFrame to store tracks that could not be
# added to the playlist

numberOfTracks = spotifyLiked.shape[0]  # Get the number of tracks in the liked songs DataFrame

for i in range(0, numberOfTracks - 1):  # Loop through the liked songs
    if (i % 10) == 0:  # Print the current track number and total number of tracks every 10 tracks
        print("Track number " + str(i + 1) + " of " + str(numberOfTracks))
    track = spotifyLiked.loc[i]  # Get the current track's information

    trackDF = pd.DataFrame.from_records([{  # Create a DataFrame for the current track
        "song_name": track["song_name"],  # The name of the song
        "artist": track["artist"],  # The artist(s) of the song
        "album": track["album"],  # The album the song is from
        "release_date": track["release_date"],  # The release date of the album
        "duration_ms": track["duration_ms"],  # The duration of the song in milliseconds
        "popularity": track["popularity"]  # The popularity of the song on Spotify
    }])

    search_results = ytMusic.search(track["song_name"] + " - " + track["artist"],
                                    "songs")  # Search for the current track on YouTube Music
    try:  # Try to add the track to the user's YouTube Music playlist
        ytMusic.add_playlist_items(playlistId, [search_results[0]['videoId']])
    except:  # If the track cannot be added, add the track's information to the noVideoID DataFrame
        print("Couldn't find a videoID for track: " + track["song_name"] + " - " + track["artist"])
        noVideoID = pd.concat([noVideoID, trackDF])

noVideoID.to_csv("liked_songs_not_added.csv",
                 index=False)  # Save the noVideoID DataFrame as a CSV file without the index
