from urllib.request import urlopen
import requests
import json
import csv
import pandas as pd
import numpy as np

base = "http://lookup-service-prod.mlb.com/json/named."

player_search = "search_player_all.bam?sport_code='mlb'&active_sw='Y'&name_part="
stats_id = "sport_hitting_tm.bam?league_list_id='mlb'&game_type='R'&season='2017'&player_id="

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

    #http://lookup-service-prod.mlb.com/json/named.sport_hitting_tm.bam

    if r.status_code == 200:

        parsed_json = json.loads(r.content.decode('utf-8'))
        #print(parsed_json['search_player_all']['queryResults']['totalSize'])
        if parsed_json['search_player_all']['queryResults']['totalSize'] == '1':
            id_number = parsed_json['search_player_all']['queryResults']['row']['player_id']
            position = parsed_json['search_player_all']['queryResults']['row']['position']
            team = parsed_json['search_player_all']['queryResults']['row']['team_full']
            #print(id_number)
            player_info = [player, position, team]
            player_info_list.append(player_info)


            player_id = "'" + id_number + "'"

            q2 = base+stats_id+player_id

            r = requests.get(q2)
            #print(q2)

            if r.status_code == 200:
                parsed_json = json.loads(r.content.decode('utf-8'))

                if parsed_json['sport_hitting_tm']['queryResults']['totalSize'] == '1':
                    ops = parsed_json['sport_hitting_tm']['queryResults']['row']['ops']
                    hr = parsed_json['sport_hitting_tm']['queryResults']['row']['hr']
                    slg = parsed_json['sport_hitting_tm']['queryResults']['row']['slg']
                    obp = parsed_json['sport_hitting_tm']['queryResults']['row']['obp']
                    rbi = parsed_json['sport_hitting_tm']['queryResults']['row']['rbi']
                    ab = parsed_json['sport_hitting_tm']['queryResults']['row']['ab']
                    np = parsed_json['sport_hitting_tm']['queryResults']['row']['np']

                elif parsed_json['sport_hitting_tm']['queryResults']['totalSize'] == '0':
                    ops = 0
                    hr = 0
                    slg = 0
                    obp = 0
                    rbi = 0
                    ab = 0
                    np = 0

                else:
                    ops = parsed_json['sport_hitting_tm']['queryResults']['row'][0]['ops']
                    hr = parsed_json['sport_hitting_tm']['queryResults']['row'][0]['hr']
                    slg = parsed_json['sport_hitting_tm']['queryResults']['row'][0]['slg']
                    obp = parsed_json['sport_hitting_tm']['queryResults']['row'][0]['obp']
                    rbi = parsed_json['sport_hitting_tm']['queryResults']['row'][0]['rbi']
                    ab = parsed_json['sport_hitting_tm']['queryResults']['row'][0]['ab']
                    np = parsed_json['sport_hitting_tm']['queryResults']['row'][0]['np']

                stats = [ops, hr, slg, obp, rbi, ab, np]
                stats_list.append(stats)


#print(player_info_list)
#print(stats_list)

player_df = pd.DataFrame(player_info_list)
stats_df = pd.DataFrame(stats_list)

#print(player_df)
#print(stats_df)

df = pd.concat([player_df.reset_index(drop=True), stats_df.reset_index(drop=True)], axis=1)
print(df)

df.to_csv("player_stats.csv")


