import requests

BASEURL = 'https://altumbase.com/api'
TIMEOUT = 30

def __get_diamonds_received_page(page):
    url = f'{BASEURL}/diamonds_received_24h?ref=bcl&page_size=100&page={page}'
    response = requests.get(url, timeout=TIMEOUT)
    return response.json()

def __get_deso_locked_page(page):
    url = f'{BASEURL}/deso_locked_24h?ref=bcl&page_size=100&page={page}'
    response = requests.get(url, timeout=TIMEOUT)
    return response.json()


def get_diamonds_received():
    page = 0
    while True:
        page_data = __get_diamonds_received_page(page)
        if not page_data:
            break
        if page_data.get("data", []) == []:
            break
        for row in page_data["data"]:
            if "public_key" not in row:
                continue
            yield row["public_key"]
        page += 1

def get_deso_locked():
    page = 0
    while True:
        page_data = __get_deso_locked_page(page)
        if not page_data:
            break
        if page_data.get("data", []) == []:
            break
        for row in page_data["data"]:
            if "public_key" not in row:
                continue
            yield row["public_key"]
        page += 1
