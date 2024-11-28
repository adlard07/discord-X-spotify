from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import configparser
from logger import logging


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
        self.playlists = {}

    def get_playlists(self, user_id):
        "Returns all the playlists of the given user_id"
        try:
            playlists = self.sp.user_playlists(user_id)
            self.playlists = {playlist['name']: playlist['id'] for playlist in playlists['items']}

            logging.info(f"Successfully retrieved playlists for user {user_id}.")
            return self.playlists

        except Exception as e:
            logging.error(f"An error occurred while retrieving playlists: {e}")
            return {}

    def get_tracks(self, playlist_name):
        "Returns all the tracks present in the playlist"
        try:
            if not self.playlists:
                logging.warning("Playlists not retrieved. Please call get_playlists first.")
                return {}

            playlist_id = self.playlists.get(playlist_name)
            if not playlist_id:
                logging.warning(f"Playlist '{playlist_name}' not found.")
                return {}

            tracks = self.sp.playlist_tracks(playlist_id)
            tracks_dict = {
                idx + 1: f"{item['track']['name']} - {', '.join(artist['name'] for artist in item['track']['artists'])}"
                for idx, item in enumerate(tracks['items'])
            }

            logging.info(f"Successfully retrieved tracks for playlist {playlist_name}.")
            return tracks_dict

        except Exception as e:
            logging.error(f"An error occurred while retrieving tracks: {e}")
            return {}


if __name__ == '__main__':
    user_id = '31wc6kr3n7x5wjkh3lk2yh6olsmm'
    playlist_name = 'You weirdo'

    spotify_manager = SpotifyManager()
    playlists = spotify_manager.get_playlists(user_id)
    tracks = spotify_manager.get_tracks(playlist_name)
    logging.info(tracks)
