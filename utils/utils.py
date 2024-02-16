import time
import os
import datetime
import pandas as pd
import requests
import json as json
import os

# Data Path
DATA_PATH = "data"

# Endpoints
API_FOOTBALL_PLAYERS_ENDPOINT = "https://api-football-v1.p.rapidapi.com/v3/players"

# Championship Codes
CHAMPIONSHIPS = {
    "SPANISH_LEAGUE": "140",
    "SPANISH_LEAGUE_2": "141",
    "PREMIER_LEAGUE": "39",
    "BUNDESLIGA": "78",
    "EREDIVISE_LEAGUE": "88",
    "TURKEY_LEAGUE": "203",
    "MAJOR_LEAGUE": "253",
    "INDIA_LEAGUE": "323"
}

# Set the championship
CHAMPIONSHIP = CHAMPIONSHIPS["SPANISH_LEAGUE"]

# Season year
SEASON_22 = "2022"
SEASON_23 = "2023"

# Http Codes
TOO_MANY_REQUESTS = 429

# Initial Page
FIRST = 1


def get_api_keys_file(path: str) -> dict:
    """
    Reads the API keys file located at the given path and returns the contents as a dictionary.

    Args:
        path (str): The path to the API keys file.

    Returns:
        dict: The contents of the API keys file as a dictionary.
    """
    with open(path) as f:
        return json.load(f)


def get_api_key() -> str:
    """
    Retrieves the API key from the API keys file.

    Returns:
        str: The API key.
    """
    keys = get_api_keys_file('/home/jordilucas/.secret/api_football.json')
    return keys['api_football_key']


def save_df_to_csv(df: pd.DataFrame) -> None:
    """
    Save a DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to be saved.

    Returns:
        None
    """
    datetime_now = datetime.datetime.now().strftime("%Y-%m-%d%H:%M:%S")
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
    df.to_csv(DATA_PATH+'/df_championship_' + CHAMPIONSHIP + '_' + datetime_now + '.csv', index=False, header=True)


def get_total_pages() -> int:
    """
    Retrieves the total number of pages for the league statistics.

    Returns:
        int: The total number of pages.
    """
    querystring_ = {"league": CHAMPIONSHIP, "season": SEASON_22, "page": 30}
    json_response_stats_league = get_api_football(API_FOOTBALL_PLAYERS_ENDPOINT, querystring_, get_api_key())
    parsed_stats_league = draw_pretty_json(json_response_stats_league)

    return parsed_stats_league['paging']['total']


def get_api_response(url: str, querystring: dict, key: str, method: str = "GET") -> requests.Response:
    """
    Sends a request to the specified URL with the given querystring and API key.

    Args:
        url (str): The URL to send the request to.
        querystring (dict): The query parameters to include in the request.
        key (str): The API key to authenticate the request.
        method (str, optional): The HTTP method to use for the request. Defaults to "GET".

    Returns:
        requests.Response: The response object containing the API response.

    """
    url = url
    headers = {
        'x-rapidapi-key': key,
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
    }
    response = requests.request(method, url, headers=headers, params=querystring)

    return response


def get_api_football(url: str, querystring: dict, key: str) -> str:
    """
    Sends a GET request to the specified URL with the given querystring and API key.
    Returns the JSON response as a string.

    :param url: The URL to send the request to.
    :param querystring: The query parameters to include in the request.
    :param key: The API key to authenticate the request.
    :return: The JSON response as a string.
    """
    response = get_api_response(url, querystring, key, method="GET")

    json_response = response.text
    print(response.status_code, '::', response.url)
    print(response.headers)

    if response.status_code == TOO_MANY_REQUESTS:
        print(response.text)

    return json_response


def draw_pretty_json(json_resp: str) -> dict:
    """
    Prints the JSON response in a pretty and indented format.

    Args:
        json_resp (str): The JSON response to be printed.

    Returns:
        dict: The parsed JSON response.

    """
    parsed = json.loads(json_resp)
    print(json.dumps(parsed, indent=4, sort_keys=True))
    return parsed


def get_championship_data(url: str, key: str, initial: int = FIRST) -> pd.DataFrame:
    """
    Retrieves championship data from an API.

    Args:
        url (str): The URL of the API.
        key (str): The API key.
        initial (int, optional): The initial page number. Defaults to FIRST.

    Returns:
        pd.DataFrame: The championship data as a pandas DataFrame.
    """
    request_x_minute = 30
    df = pd.DataFrame()
    for page_ in range(initial, get_total_pages()):
        qs = {"league": CHAMPIONSHIP, "season": SEASON_22, "page": page_}
        json_response = get_api_football(url, qs, key)
        parsed = json.loads(json_response)
        api_data = get_data(parsed)
        df = df.append(api_data)

        # You have to control time between requests in the BASIC Plan.
        if page_ == request_x_minute - 2:
            # Sleep the process to avoid TOO_MANY_REQUESTS
            time.sleep(121)

    return df


def clean_weight_height(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the weight and height columns of a DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the weight and height columns.

    Returns:
    pd.DataFrame: The DataFrame with the weight and height columns cleaned.
    """
    df['Weight_kg'] = (df['Weight'].str.extract('^([0-9]{2,3})')).astype(float)
    df['Height_cm'] = (df['Height'].str.extract('^([0-9]{3})')).astype(float)

    df.drop(['Weight', 'Height'], axis=1, inplace=True)

    return df



def get_data(parsed)-> pd.DataFrame:
    """
    Extracts data from the parsed JSON response and returns it as a pandas DataFrame.

    Args:
        parsed (dict): Parsed JSON response containing player statistics.

    Returns:
        pd.DataFrame: DataFrame containing the extracted player statistics.
    """
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
