import datetime

from utils.utils import get_data_x_page, get_api_key, API_FOOTBALL_PLAYERS_ENDPOINT, \
    get_total_pages


def collect_api_data():

    # Get API Key
    key = get_api_key()
    # Get total pages
    total_pages = get_total_pages()
    # Get Liga dataset
    df_liga = get_data_x_page(1, total_pages, API_FOOTBALL_PLAYERS_ENDPOINT, key)
    # Get date now
    datetime_now = datetime.datetime.now().strftime("%Y-%m-%d%H:%M:%S")
    # Save La Liga dataset in csv format
    df_liga.to_csv('data/data_liga_' + datetime_now + '.csv', index=False, header=True)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    collect_api_data()

