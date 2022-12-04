# Spotify to Youtube Playlist Conversion

This is a couple of scripts mostly written and commented by ChatGPT to export a user's saved tracks on Spotify to a CSV and to read a CSV of a playlist and import it to an existing playlist on Youtube Music.

## Usage

1. Change the values in `config.py` as appropriate:
    - `playlistId = ""` - ID of the Youtube Music Playlist you want to add to (the end of this URL https://music.youtube.com/playlist?list=)
    - Create an app on the [Spotify Development Dashboard](https://developer.spotify.com/dashboard/applications) and fill out `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET`
    - `SPOTIFY_CLIENT_REDIRECT = "http://localhost:8080"` - this is most likely ok, just make sure to add the same value to your [Spotify developer project](https://developer.spotify.com/dashboard/applications)
2. Follow the instructions [at the ytmusicapi docs](https://ytmusicapi.readthedocs.io/en/latest/setup.html#authenticated-requests) to grab credentials and save them to `ytAuth.json`
3. Install the requirements `pip install -r requirements.txt`
4. Export you Spotify saved tracks `python3 openAISpotifyLikedExport.py`
5. Import the CSV into YT Music `python3 importCSVYTMusic.py`

## Limitations

It is likely the import script won't work perfectly - Spotify and YT don't necessarily have the same songs, and this was written in a morning...
