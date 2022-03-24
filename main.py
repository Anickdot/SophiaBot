import json
import os
import re

import dotenv
import requests

from bot import send_message
from database import update_local_data

dotenv.load_dotenv()


def get_github_repo(cmc_id: int) -> tuple[str, str] | None:
    response = requests.get(
        'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info',
        params={'id': cmc_id},
        headers={'X-CMC_PRO_API_KEY': os.environ['CMC_ID']}
    )
    json_object = json.loads(response.content)
    
    source_code = json_object['data'][str(cmc_id)]['urls']['source_code']
    if len(source_code):
        for scode in source_code:
            if (match := re.fullmatch('^https:\/\/github\.com\/(.+)\/(.+)$', scode)):
                return (match[1], match[2])
        print('No GitHub url ' + json_object['data'][str(cmc_id)]['symbol'])
    else:
        print('No source code ' + json_object['data'][str(cmc_id)]['symbol'])

def get_last_github_release(owner: str, name: str) -> str:
    response = requests.get(f'https://api.github.com/repos/{owner}/{name}/releases')
    json_object = json.loads(response.content)
    
    if not isinstance(json_object, list):
        raise ConnectionError

    if (len(json_object)):
        return json_object[0]['tag_name']
    return '0'

def main():
    with open('currencies.json', 'r') as file:
        currencies = json.load(file)

    result = ''
    for pair in currencies:
        curr, cmc = pair['currency'], pair['cmcId']
        if (repository := get_github_repo(cmc)):
            release = get_last_github_release(repository[0], repository[1])
            if update_local_data(curr, release):
                result += f'<a href="https://github.com/{repository[0]}/{repository[1]}/releases">{curr.upper()}</a>: {release}\n'
    
    if result:
        result = 'New Token Release:\n' + result
        send_message(result)


if __name__ == '__main__':
    main()
