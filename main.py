from urllib.parse import urlparse
from dotenv import load_dotenv
import requests
import argparse
import os

def shorten_link(long_url, headers):
    url = 'https://api-ssl.bitly.com/v4/shorten'

    payload = {
        'long_url': long_url
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    return response.json()['id']

def count_clicks(bitlink, headers):
    parse_url = urlparse(bitlink)

    parse_bitlink = parse_url.netloc + parse_url.path

    url = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'.format(parse_bitlink)

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()['total_clicks']

def main():
    load_dotenv()
    token = os.getenv('BITLINK_TOKEN')

    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }

    parser = argparse.ArgumentParser(
        description='Описание что делает программа'
    )
    parser.add_argument('-l', '--link', help='Ссылка')
    user = parser.parse_args()

    try:
        try:
            clicks_count = count_clicks(user.link, headers)
            print('Количество переходов по ссылке битли: ', clicks_count)
        except requests.exceptions.HTTPError:
            bitlink = shorten_link(user.link, headers)
            print('Битлинк', bitlink)
    except requests.exceptions.HTTPError:
        print("ошибка")

if __name__ == '__main__':
    main()
