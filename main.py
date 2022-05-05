import datetime

from utils.utils import get_api_football, draw_pretty_json, get_data_x_page, get_api_key


def collect_api_data():

    key = get_api_key()
    qs_liga = {"league": "140", "season": "2021", "page": 30}
    url_stats_liga = "https://api-football-v1.p.rapidapi.com/v3/players"

    json_response_stats_league = get_api_football(url_stats_liga, qs_liga, key)
    parsed_stats_league = draw_pretty_json(json_response_stats_league)

    total_pages = parsed_stats_league['paging']['total']

    df_liga = get_data_x_page(1, 4, url_stats_liga, key)

    datetime_now = datetime.datetime.now().strftime("%Y-%m-%d%H:%M:%S")

    df_liga.to_csv('data/data_liga_' + datetime_now + '.csv', index=False, header=True)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    collect_api_data()

