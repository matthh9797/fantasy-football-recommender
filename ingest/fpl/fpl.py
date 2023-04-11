import requests


def get_fantasy_api_data(prefix: str) -> dict:
    """
    get data from Fantasy Footbal API
    @param prefix to append to api url
    @return json containing api output
    """
    url = f"https://fantasy.premierleague.com/api/{prefix}/"
    r = requests.get(url)
    if r.status_code == 404:
        print(f"Invalid api url provided: {url}")
        return 404
    else:
        return r.json()
