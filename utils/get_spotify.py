from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import configparser
from utils.logger import logging

class SpotifyManager:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        CLIENT_ID = config['Configuration']['SPOTIFY_CLIENT_ID']
        CLIENT_SECRET = config['Configuration']['SPOTIFY_CLIENT_SECRET']

        client_credentials_manager = SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET
        )
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def get_tracks(self, playlist_id):
        "Returns all the tracks present in the playlist"
        try:
            tracks = self.sp.playlist_tracks(playlist_id)
            tracks_dict = {
                idx + 1: f"{item['track']['name']} - {', '.join(artist['name'] for artist in item['track']['artists'])}"
                for idx, item in enumerate(tracks['items'])
            }

            logging.info(f"Successfully retrieved tracks for playlist ID {playlist_id}.")
            return tracks_dict

        except Exception as e:
            logging.error(f"An error occurred while retrieving tracks: {e}")
            return {}

if __name__ == '__main__':
    playlist_id = '5KWSvWPrcmCfff6zBdQw1L'  # Replace with your actual playlist ID

    spotify_manager = SpotifyManager()
    tracks = spotify_manager.get_tracks(playlist_id)
    logging.info(tracks)
