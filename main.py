import datetime

from utils.utils import get_championship_data, get_api_key, API_FOOTBALL_PLAYERS_ENDPOINT, \
    get_total_pages


def get_api_data():

    # Get API Key
    key = get_api_key()
    # Get championship dataset
    df_championship = get_championship_data(1, get_total_pages(), API_FOOTBALL_PLAYERS_ENDPOINT, key)
    # Get date now
    datetime_now = datetime.datetime.now().strftime("%Y-%m-%d%H:%M:%S")
    # Save championship dataset in csv format
    df_championship.to_csv('data/df_championship_' + datetime_now + '.csv', index=False, header=True)


# The main one.
if __name__ == '__main__':
    get_api_data()

