#!/usr/bin/env python
import requests
import sys
from time import sleep

stations = {
    'defcon': 'http://somafm.com/recent/defcon.html'
}

def now_playing(station):
    lines = requests.get(stations[station]).text.splitlines()
    while len(lines) > 0:
        line = lines.pop(0)
        if line == u'<!-- line 1 -->':
            break
    lines.pop(0)
    line = lines.pop(0)
    
    results = []
    buff = ""
    in_tag = False
    for char in line:
        if char == '<':
            if len(buff) > 0:
                results.append(buff)
                buff = ""
    
            in_tag = True
    
        elif char == '>':
            in_tag = False
    
        elif not in_tag:
            buff += char
    
    while len(results) < 3:
        results.append("")
    
    return results[0:3]



if __name__ == '__main__':
    if len(sys.argv) < 2:
        station = 'defcon'
    else:
        station = sys.argv[1]

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
