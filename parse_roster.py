#!/usr/bin/env python3
"""Parse Hurst roster HTML and write CSV of player bio info."""
import csv
from bs4 import BeautifulSoup

INPUT = 'roster_page.html'
OUTPUT = 'roster.csv'

def get_text_or_empty(tag):
    return tag.get_text(strip=True) if tag else ''

def parse():
    with open(INPUT, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    players = []

    # 1) try detailed player header blocks (individual bio layout)
    for block in soup.select('div.sidearm-roster-player-header-details'):
        num_tag = block.select_one('.sidearm-roster-player-jersey-number')
        number = get_text_or_empty(num_tag).strip()

        name_block = block.select_one('.sidearm-roster-player-name')
        first = last = ''
        if name_block:
            spans = name_block.find_all('span')
            if len(spans) >= 2:
                first = spans[0].get_text(strip=True)
                last = spans[1].get_text(strip=True)
            elif len(spans) == 1:
                parts = spans[0].get_text(strip=True).split()
                first = parts[0] if parts else ''
                last = ' '.join(parts[1:]) if len(parts) > 1 else ''

        fields = {}
        for dl in block.select('dl'):
            dt = dl.find('dt')
            dd = dl.find('dd')
            if dt and dd:
                key = dt.get_text(strip=True).rstrip(':')
                val = dd.get_text(strip=True)
                fields[key] = val

        player = {
            'number': number,
            'first_name': first,
            'last_name': last,
            'position': fields.get('Position', ''),
            'weight': fields.get('Weight', ''),
            'height': fields.get('Height', ''),
            'hometown': fields.get('Hometown', ''),
            'class': fields.get('Class', ''),
            'high_school': fields.get('High School', ''),
        }
        players.append(player)

    # 2) try card/list layout (roster page list of players)
    for li in soup.select('li.sidearm-list-card-item'):
        # number
        num = ''
        num_tag = li.select_one('.sidearm-roster-player-jersey span')
        if num_tag:
            num = num_tag.get_text(strip=True)
        else:
            # fallback: sometimes jersey is in a small element
            num = li.get('data-player-id', '')

        # names
        first = get_text_or_empty(li.select_one('.sidearm-roster-player-first-name'))
        last = get_text_or_empty(li.select_one('.sidearm-roster-player-last-name'))

        # position (short)
        pos = get_text_or_empty(li.select_one('.sidearm-roster-player-position-short'))

        # height/weight/class
        height = get_text_or_empty(li.select_one('.sidearm-roster-player-height'))
        weight = get_text_or_empty(li.select_one('.sidearm-roster-player-weight'))
        cls = get_text_or_empty(li.select_one('.sidearm-roster-player-academic-year'))

        # hometown and high school/previous school
        hometown = get_text_or_empty(li.select_one('.sidearm-roster-player-hometown'))
        # try highschool then previous-school then previous-school/previous
        highschool = get_text_or_empty(li.select_one('.sidearm-roster-player-highschool'))
        if not highschool:
            highschool = get_text_or_empty(li.select_one('.sidearm-roster-player-previous-school'))
        if not highschool:
            highschool = get_text_or_empty(li.select_one('.sidearm-roster-player-previous'))

        player = {
            'number': num,
            'first_name': first,
            'last_name': last,
            'position': pos,
            'weight': weight.replace('lbs','').replace('lbs.','').strip(),
            'height': height,
            'hometown': hometown,
            'class': cls,
            'high_school': highschool,
        }
        players.append(player)

    # write CSV
    with open(OUTPUT, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['number','first_name','last_name','position','weight','height','hometown','class','high_school'])
        writer.writeheader()
        for p in players:
            writer.writerow(p)

    print(f'Wrote {len(players)} players to {OUTPUT}')

if __name__ == '__main__':
    parse()
