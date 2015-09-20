#!/usr/bin/env python
import requests
import sys
from time import sleep

STATIONS = {
    'defcon': 'http://somafm.com/recent/defcon.html',
    'groovesalad': 'http://somafm.com/recent/groovesalad.html'
}

def now_playing(station):
    results = []
    lines = requests.get(STATIONS[station]).text.splitlines()
    while len(lines) > 0:
        line = lines.pop(0)
        if line == '<!-- line 1 -->':
            break
    lines.pop(0)
    line = lines.pop(0)

    buff = ''
    in_tag = False
    for char in line:
        if char == '<':
            in_tag = True
            if len(buff) > 0:
                results.append(buff)
                buff = ''
        elif char == '>':
            in_tag = False
        elif not in_tag:
            buff += char
 
    while len(results) < 3:
        results.append("")

    return results[0:3]

if __name__ == '__main__':
    station = sys.argv[1] if len(sys.argv) == 2 else 'defcon'
    old = None
    try:
        while True:
            artist, track, album = now_playing(station)
            if (artist, track, album) != old:
                old = (artist, track, album)
                print '{0}\t{1}\t{2}'.format(artist, track, album)
                with open(station + '.log', 'a') as f:
                    f.write('{0}\t{1}\t{2}\n'.format(artist, track, album))
            sleep(60)

    except KeyboardInterrupt:
        pass
