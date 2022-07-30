import time
import os
import datetime
import pandas as pd
import requests
import json as json

# Endpoints
API_FOOTBALL_PLAYERS_ENDPOINT = "https://api-football-v1.p.rapidapi.com/v3/players"

# Championship Codes
SPANISH_LEAGUE = "140"
SPANISH_LEAGUE_2 = "141"
PREMIER_LEAGUE = "39"
BUNDESLIGA = "78"
EREDIVISE_LEAGUE = "88"
# DENMARK_LEAGUE = "120"
TURKEY_LEAGUE = "203"
MAJOR_LEAGUE = "253"
INDIA_LEAGUE = "323"
# CAMEROON_LEAGUE = "411"

# Season year
SEASON = "2021"

# Http Codes
TOO_MANY_REQUESTS = 429

# Initial Page
FIRST = 1


def get_api_keys_file(path):
    with open(path) as f:
        return json.load(f)


def get_api_key():
    keys = get_api_keys_file('/home/jordilucas/.secret/api_football.json')
    return keys['api_football_key']


def save_df_to_csv(df):
    path = "data"
    datetime_now = datetime.datetime.now().strftime("%Y-%m-%d%H:%M:%S")
    if not os.path.exists(path):
        os.makedirs(path)
    df.to_csv(path+'/df_championship_' + datetime_now + '.csv', index=False, header=True)


def get_total_pages():
    querystring_ = {"league": PREMIER_LEAGUE, "season": SEASON, "page": 30}
    json_response_stats_league = get_api_football(API_FOOTBALL_PLAYERS_ENDPOINT, querystring_, get_api_key())
    parsed_stats_league = draw_pretty_json(json_response_stats_league)

    return parsed_stats_league['paging']['total']


def get_api_football(url, querystring, key, method="GET"):
    url = url
    headers = {
        'x-rapidapi-key': key,
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
    }
    response = requests.request(method, url, headers=headers, params=querystring)
    json_response = response.text
    print(response.status_code, '::', response.url)
    print(response.headers)

    if response.status_code == TOO_MANY_REQUESTS:
        print(response.text)
        # time.sleep(61)

    return json_response


def draw_pretty_json(json_resp):
    parsed = json.loads(json_resp)
    print(json.dumps(parsed, indent=4, sort_keys=True))
    return parsed


def get_championship_data(initial, page_num, url, key):
    request_x_minute = 30
    df = pd.DataFrame()
    for page_ in range(initial, page_num + 1):
        qs = {"league": PREMIER_LEAGUE, "season": SEASON, "page": page_}
        json_response = get_api_football(url, qs, key)
        parsed = json.loads(json_response)
        api_data = get_data(parsed)
        df = df.append(api_data)

        # You have to control time between requests in the BASIC Plan.
        if page_ == request_x_minute - 2:
            time.sleep(121)

    return df


def clean_weight_height(df):
    df['Weight_kg'] = (df['Weight'].str.extract('^([0-9]{2,3})')).astype(float)
    df['Height_cm'] = (df['Height'].str.extract('^([0-9]{3})')).astype(float)

    df.drop(['Weight', 'Height'], axis=1, inplace=True)

    return df


# Loop all passes accuracy api page team
def get_data(parsed):
    # General
    id_list = []
    team_list = []
    name_list = []
    position_list = []
    age_list = []
    height_list = []
    weight_list = []
    nationality_list = []
    injured_list = []
    photo_list = []
    logo_team_list = []
    rating_list = []
    captain_list = []

    # Passes
    passes_acc_list = []
    passes_total_list = []
    passes_key_list = []

    # Shots
    shots_on_list = []
    shots_total_list = []

    # Fouls
    fouls_drawn_list = []
    fouls_comm_list = []

    # Dribbles
    dribbles_attempts = []
    dribbles_past = []
    dribbles_success = []

    # Games
    games_app_list = []
    games_minutes_list = []
    games_rating_list = []

    # Goals
    goals_total_list = []
    goals_assist_list = []
    goals_conc_list = []
    goals_saved_list = []

    # Tackles
    tackles_blocks_list = []
    tackles_inter_list = []
    tackles_total_list = []

    # Duels
    duels_won_list = []
    duels_total_list = []

    # Cards
    yellow_card_list = []
    red_card_list = []
    yellowred_card_list = []

    # print("Longitud parsed[response]: {}".format(len(parsed['response'])))
    # print("parsed_stats_league[results]: {}".format(parsed['results']))
    for i in range(0, parsed['results']):
        # Mains
        response = parsed['response'][i]
        stats = response['statistics'][0]

        # General
        id_player = response['player']['id']
        team = stats['team']['name']
        logo_team = stats['team']['logo']
        name = response['player']['name']
        age = response['player']['age']
        height = response['player']['height']
        weight = response['player']['weight']
        nationality = response['player']['nationality']
        injured = response['player']['injured']
        photo = response['player']['photo']

        # Appends
        position_list.append(stats['games']['position'])
        rating_list.append(stats['games']['rating'])
        captain_list.append(stats['games']['captain'])
        age_list.append(age)
        height_list.append(height)
        weight_list.append(weight)
        nationality_list.append(nationality)
        injured_list.append(injured)
        photo_list.append(photo)
        id_list.append(id_player)
        team_list.append(team)
        name_list.append(name)
        logo_team_list.append(logo_team)

        # Cards
        yellow_card_list.append(stats['cards']['yellow'])
        red_card_list.append(stats['cards']['red'])
        yellowred_card_list.append(stats['cards']['yellowred'])

        # Passes
        passes_acc_list.append(stats['passes']['accuracy'])
        passes_total_list.append(stats['passes']['total'])
        passes_key_list.append(stats['passes']['key'])

        # Shots
        shots_on_list.append(stats['shots']['on'])
        shots_total_list.append(stats['shots']['total'])

        # Fouls
        fouls_drawn_list.append(stats['fouls']['drawn'])
        fouls_comm_list.append(stats['fouls']['committed'])

        # Dribbles
        dribbles_attempts.append(stats['dribbles']['attempts'])
        dribbles_past.append(stats['dribbles']['past'])
        dribbles_success.append(stats['dribbles']['success'])

        # Games
        games_app_list.append(stats['games']['appearences'])
        games_minutes_list.append(stats['games']['minutes'])
        games_rating_list.append(stats['games']['rating'])

        # Goals
        goals_total_list.append(stats['goals']['total'])
        goals_assist_list.append(stats['goals']['assists'])
        goals_conc_list.append(stats['goals']['conceded'])
        goals_saved_list.append(stats['goals']['saves'])

        # Tackles
        tackles_blocks_list.append(stats['tackles']['blocks'])
        tackles_inter_list.append(stats['tackles']['interceptions'])
        tackles_total_list.append(stats['tackles']['total'])

        # Duels
        duels_total_list.append(stats['duels']['total'])
        duels_won_list.append(stats['duels']['won'])

    api_data = pd.DataFrame({"Id": id_list, "Name": name_list,
                             "Age": age_list,
                             "Height": height_list,
                             "Weight": weight_list,
                             "Nationality": nationality_list,
                             "Injured": injured_list,
                             "Team": team_list,
                             "Position": position_list,
                             "Games": games_app_list,
                             "Minutes": games_minutes_list,
                             "Accuracy_Passes": passes_acc_list,
                             "Key_Passes": passes_key_list,
                             "Total_Passes": passes_total_list,
                             "Shots_On": shots_on_list,
                             "Shots_Total": shots_total_list,
                             "Dribbles_Attempts": dribbles_attempts,
                             "Dribbles_Past": dribbles_past,
                             "Dribbles_Success": dribbles_success,
                             "Fouls_Drawn": fouls_drawn_list,
                             "Fouls_Committed": fouls_comm_list,
                             "Tackled_Block": tackles_blocks_list,
                             "Tackled_Intercept": tackles_inter_list,
                             "Tackled_Total": tackles_total_list,
                             "Duels_Won": duels_won_list,
                             "Duels_Total": duels_total_list,
                             "Goals_Assist": goals_assist_list,
                             "Goals_Total": goals_total_list,
                             "Goals_Conceded": goals_conc_list,
                             "Goals_Saves": goals_saved_list,
                             "Photo": photo_list,
                             "Logo_Team": logo_team_list,
                             "Rating": rating_list,
                             "Yellow_Cards": yellow_card_list,
                             "Red_Cards": red_card_list,
                             "Yellow_Red_Cards": yellowred_card_list,
                             "Captain": captain_list
                             })
    return api_data
