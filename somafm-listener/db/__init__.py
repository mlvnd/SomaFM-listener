#!/usr/bin/env python
import sqlite3

STATEMENTS = {
    'ddl': {
        'history': """
            CREATE TABLE HISTORY (
                DATETIME DATETIME DEFAULT CURRENT_TIMESTAMP,
                ARTIST TEXT,
                TRACK TEXT,
                ALBUM TEXT
            )
            """,
        'spotify': """
            CREATE TABLE SPOTIFY (
                ARTIST TEXT,
                TRACK TEXT,
                ALBUM TEXT,
                FOUND BOOLEAN
            )
            """
    },
    'queries': {
        'find_table': """
            SELECT NAME
              FROM SQLITE_MASTER
             WHERE TYPE='table'
               AND NAME=?
            """,
        'track_exists': """
            SELECT COUNT(*) COUNT
              FROM SPOTIFY
             WHERE ARTIST = ?
               AND TRACK = ?
               AND ALBUM = ?
            """
    },
    'inserts': {
        'history': """
            INSERT INTO HISTORY (
                ARTIST,
                TRACK,
                ALBUM
            ) VALUES (
                ?,
                ?,
                ?
            )
            """,
        'spotify': """
            INSERT INTO SPOTIFY (
                ARTIST,
                TRACK,
                ALBUM,
                FOUND
            ) VALUES (
                ?,
                ?,
                ?,
                ?
            )
            """
    },
    'updates': {
        'spotify': """
            UPDATE SPOTIFY
               SET FOUND = ?
             WHERE ARTIST = ?
               AND TRACK = ?
               AND ALBUM = ?
            """
    }
}


class Database(object):

    def __init__(self, station):
        sqlite3.register_adapter(bool, int)
        sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))

        conn = sqlite3.connect('{0}.sqlite'.format(station),
                               detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row

        self.station = station
        self.conn = conn

        if not self._table_exists('history'):
            self._create_table('history')

        if not self._table_exists('spotify'):
            self._create_table('spotify')

    def _table_exists(self, table_name):
        sql = STATEMENTS['queries']['find_table']
        result = False

        conn = self.conn
        cur = conn.cursor()
        cur.execute(sql, (table_name,))

        if cur.fetchone() is not None:
            result = True
        cur.close()

        return result

    def _create_table(self, table_name):
        ddl = STATEMENTS['ddl'][table_name]
        self.conn.execute(ddl)

    def add_to_history(self, artist, track, album):
        conn = self.conn
        sql = STATEMENTS['inserts']['history']
        conn.execute(sql, (artist, track, album,))
        conn.commit()

    def track_exists(self, artist, track, album):
        conn = self.conn
        sql = STATEMENTS['queries']['track_exists']
        cur = conn.cursor()
        cur.execute(sql, (artist, track, album,))
        row = cur.fetchone()
        result = row['count'] > 0
        cur.close()

        return result

    def add_to_spotify(self, artist, track, album, found):
        conn = self.conn

        if self.track_exists(artist, track, album):
            sql = STATEMENTS['updates']['spotify']
            conn.execute(sql, (found, artist, track, album,))
        else:
            sql = STATEMENTS['inserts']['spotify']
            conn.execute(sql, (artist, track, album, found,))

        conn.commit()
