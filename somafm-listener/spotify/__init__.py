#!/usr/bin/env python
import spotipy
import spotipy.util as util


SCOPES = [
    'user-library-read',
    'playlist-read-private',
    'playlist-modify-private',
    'playlist-modify-public'
]


class Spotify(object):

    def __init__(self, username):
        scope = " ".join(SCOPES)
        self.token = util.prompt_for_user_token(username, scope)
        self.sp = None

        if self.token is None:
            sys.stderr.write("Can't get token for {0}\n".format(username))
            sys.exit(1)

        self.sp = spotipy.Spotify(auth=self.token)
        self.user_id = self.sp.me()['id']

    def search(self, artist, track):
        query = 'artist:{0} track:{1}'.format(artist, track)
        result = self.sp.search(q=query, type='track')
        if 'tracks' in result.keys():
            tracks = result['tracks']
            if 'items' in tracks.keys():
                return tracks['items']

    def get_playlists(self):
        result = self.sp.user_playlists(self.user_id)
        if 'items' in result.keys():
            return result['items']

    def get_playlist(self, id):
        result = self.sp.user_playlists(self.user_id, id)
        if 'items' in result.keys():
            return result['items']

    def find_playlist(self, name):
        playlists = self.get_playlists()
        for playlist in playlists:
            if playlist['name'] == name:
                return playlist['id']

    def add_track(self, playlist_name, artist, track, album):
        result = False

        playlist_id = self.find_playlist(playlist_name)
        if playlist_id is None:
            return

        search_results = self.search(artist, track)
        if len(search_results) == 0:
            return result

        track_id = search_results[0]['id']
        self.sp.user_playlist_add_tracks(self.user_id, playlist_id, [track_id])
        result = True

        return result
