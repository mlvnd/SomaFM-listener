#!/usr/bin/env python
import requests

STATIONS = {
    'defcon': 'http://somafm.com/recent/defcon.html',
    'groovesalad': 'http://somafm.com/recent/groovesalad.html'
}


def now_playing(station):
    keys = ['artist', 'title', 'album']
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

    return dict(zip(keys, results[0:3]))
