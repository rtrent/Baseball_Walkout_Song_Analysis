from urllib.request import urlopen
import requests
import json
import csv
import pandas as pd
import numpy as np

base = "http://lookup-service-prod.mlb.com/json/named."

player_search = "search_player_all.bam?sport_code='mlb'&active_sw='Y'&name_part="
stats_id = "sport_pitching_tm.bam?league_list_id='mlb'&game_type='R'&season='2018'&player_id="

player_info_list = []
stats_list = []

players = []
with open("data/player_names.csv") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        players.append(row[0])


# players = ["Ryan Zimmerman", "Clay Buchholz"]

for player in players:

    player_name = "'" + player + "'"

    q = base+player_search+player_name
    #print(q)

    r = requests.get(q)

    #http://lookup-service-prod.mlb.com/json/named.sport_pitching_tm.bam

    if r.status_code == 200:

        parsed_json = json.loads(r.content.decode('utf-8'))
        #print(parsed_json['search_player_all']['queryResults']['totalSize'])
        if parsed_json['search_player_all']['queryResults']['totalSize'] == '1':
            position = parsed_json['search_player_all']['queryResults']['row']['position']
            team = parsed_json['search_player_all']['queryResults']['row']['team_full']
            birth_country = parsed_json['search_player_all']['queryResults']['row']['birth_country']
            bat_hand = parsed_json['search_player_all']['queryResults']['row']['bats']
            throw_hand = parsed_json['search_player_all']['queryResults']['row']['throws']
            birth_date = parsed_json['search_player_all']['queryResults']['row']['birth_date']
            weight = parsed_json['search_player_all']['queryResults']['row']['weight']
            height = parsed_json['search_player_all']['queryResults']['row']['height_inches']

            #print(id_number)
            player_info = [player, position, team, birth_country, bat_hand, throw_hand, birth_date, weight, height]
            player_info_list.append(player_info)


player_df = pd.DataFrame(player_info_list)
print(player_df)

player_df.to_csv("player_info.csv")


