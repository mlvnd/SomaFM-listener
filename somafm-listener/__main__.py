#!/usr/bin/env python
import sys
import os
from time import sleep
from db import Database
from somafm import STATIONS, now_playing
from spotify import Spotify


def usage():
    cmd = os.path.basename(sys.argv[0])
    sys.stderr.write("{0} SPOTIFY_USERNAME STATION_NAME\n".format(cmd))
    sys.exit(1)


def no_env():
    sys.stdout.write("""No env variables set.

Please define these variables in your shell:

export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
    """)
    sys.exit(1)


def check_env():
    if 'SPOTIPY_CLIENT_ID' not in os.environ:
        no_env()


def print_track(track):
    artist = track['artist']
    title = track['title']
    album = track['album']

    print '{0}\t{1}\t{2}'.format(artist, title, album)


class UnknownStationException(Exception):
    pass


class SomaListener(object):
    def __init__(self, username, station):
        if station not in STATIONS:
            raise UnknownStation
        self.station = station
        self.username = username
        self.db = Database(station)
        self.spotify = Spotify(username)

    def now_playing(self):
        return now_playing(self.station)

    def listen(self):
        previous = None
        while True:
            current = self.now_playing()
            if previous != current:
                print_track(current)
                self.store_track(current)
                previous = current
            else:
                sleep(60)
                continue

    def store_track(self, track):
        artist = track['artist']
        title = track['title']
        album = track['album']

        db = self.db
        db.add_to_history(artist, title, album)

        if title is None or title == "":
            return

        if not db.track_exists(artist, title, album):
            added = self.spotify.add_track(self.station, artist, title, album)
            db.add_to_spotify(artist, title, album, added)


def main(username, station):
    listener = SomaListener(username, station)
    listener.listen()


if __name__ == '__main__':
    check_env()
    if len(sys.argv) != 3:
        usage()

    username = sys.argv[1]
    station = sys.argv[2]
    os.chdir(os.path.dirname(__file__))

    try:
        main(username, station)

    except KeyboardInterrupt:
        print

    except UnknownStationException, e:
        sys.stderr.write('Unknown station.\n')
        sys.exit(1)
