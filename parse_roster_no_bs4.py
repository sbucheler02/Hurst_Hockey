#!/usr/bin/env python3
"""Parse roster_page.html using regex (no external deps) and write roster.csv."""
import re
import csv

INPUT = 'roster_page.html'
OUTPUT = 'roster.csv'

def extract(text, pattern, default=''):
    m = re.search(pattern, text, re.S)
    return m.group(1).strip() if m else default

def parse():
    with open(INPUT, 'r', encoding='utf-8') as f:
        html = f.read()

    players = []

    # split into list-card items
    items = re.split(r'<li[^>]*class="sidearm-list-card-item"', html)
    for it in items[1:]:
        block = it
        number = extract(block, r'sidearm-roster-player-jersey[^>]*>\s*<span>\s*([^<\n]+)', '')
        if not number:
            number = extract(block, r'roster_jerseynum \">\s*([0-9]+)', '')

        first = extract(block, r'class="sidearm-roster-player-first-name">([^<]+)<')
        last = extract(block, r'class="sidearm-roster-player-last-name">([^<]+)<')

        position = extract(block, r'sidearm-roster-player-position-short">\s*([^<]+)<')
        height = extract(block, r'sidearm-roster-player-height">([^<]+)<')
        weight = extract(block, r'sidearm-roster-player-weight">([^<]+)<')
        cls = extract(block, r'sidearm-roster-player-academic-year">([^<]+)<')
        hometown = extract(block, r'sidearm-roster-player-hometown">([^<]+)<')
        highschool = extract(block, r'sidearm-roster-player-highschool">([^<]+)<')
        if not highschool:
            highschool = extract(block, r'sidearm-roster-player-previous-school">([^<]+)<')
        if not highschool:
            highschool = extract(block, r'player_highschool "">\s*<dd>([^<]+)<')

        # normalize
        weight = weight.replace('lbs','').replace('lbs.','').strip()

        players.append({
            'number': number,
            'first_name': first,
            'last_name': last,
            'position': position,
            'weight': weight,
            'height': height,
            'hometown': hometown,
            'class': cls,
            'high_school': highschool,
        })

    # write CSV
    with open(OUTPUT, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['number','first_name','last_name','position','weight','height','hometown','class','high_school']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for p in players:
            writer.writerow(p)

    print(f'Wrote {len(players)} players to {OUTPUT}')

if __name__ == '__main__':
    parse()
