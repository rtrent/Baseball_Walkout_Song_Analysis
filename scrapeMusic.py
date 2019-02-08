from bs4 import BeautifulSoup
from urllib.request import urlopen
import numpy as np
import pandas as pd

url1 = "https://www.mlb.com/entertainment/walk-up/"

# teams = ['ari', 'atl', 'bal', 'bos', 'chc',
# 'cws', 'cin', 'col', 'cle', 'det', 'hou', 'kc', 'laa', 
# 'lad', 'mia', 'mil', 'min', 'nym', 'nyy', 'oak',
# 'phi', 'pit', 'sd', 'sf', 'sea', 'stl', 'tb', 'tex', 'tor', 'wsh']


teams = ['cle']

for team in teams:

    name_list_clean = []
    song_list_clean = []

    url_combined = url1 + team
    page = urlopen(url_combined)
    soup = BeautifulSoup(page, 'html.parser')

#get player names
    name_list = soup.find_all(class_="player-name")
    for name in name_list:
        name = name.text.strip()
        name_list_clean.append(name)

#get music details
#scraped details include song name and artist
#we are using this broader tag because there is too much variation between teams
    song_list = soup.find_all(class_="song-name")
    for song in song_list:
        # song = song.text.strip()
        song_list_clean.append(song)

    baseball =  [
            ("player_name", name_list_clean),
            ("song", song_list_clean),
            ('team', team),
            ]

    df = pd.DataFrame.from_items(baseball)


    filename = team + "_baseball.csv"
    df.to_csv(filename)
