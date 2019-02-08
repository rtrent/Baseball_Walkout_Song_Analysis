from urllib.request import urlopen
import requests
import json
import csv
import pandas as pd
import numpy as np

artists = []
genres = []

with open("data/music.csv") as csvfile:
    reader = csv.reader(csvfile)
    next(reader) #if the header is in the body of the CSV - this skips that first row
    for row in reader:
        artists.append(row)

artist_base = "http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags"

for artist in artists:

    payload = {'artist': artist,
            'api_key': 'YOUR_API_KEY',
            'format': 'json'}

    r = requests.get(artist_base, params=payload)
    # print(r.url)

    parsed_json = json.loads(r.content.decode('utf-8'))
    try:
        tag1 = parsed_json['toptags']['tag'][0]['name']
        tag2 = parsed_json['toptags']['tag'][1]['name']
        tag3 = parsed_json['toptags']['tag'][2]['name']
    except:
        tag1 = 'error'
        tag2 = 'error'
        tag3 = 'error'

    tags = [tag1, tag2, tag3]
    genres.append(tags)



artists_df = pd.DataFrame(artists)
genres_df = pd.DataFrame(genres)

df = pd.concat([artists_df.reset_index(drop=True), genres_df.reset_index(drop=True)], axis=1)
print(df)

df.to_csv("artist_tags.csv")
