import dotenv
import json
import os
import re
import requests

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


def get_last_github_release(owner: str, name: str) -> tuple[str, str] | None:
    response = requests.get(f'https://api.github.com/repos/{owner}/{name}/releases')
    json_object = json.loads(response.content)

    if json_object.get('message'):
        print("API requests limit!")   # ToDo
    else:
        if (len(json_object)):
            return (json_object[0]['tag_name'], json_object[0]['published_at'])


def main():
    f = open('currencies.json')
    a = json.load(f)
    f.close()

    for pair in a:
        curr, cmc = pair['currency'], pair['cmcId']
        print(curr)

        if (repository := get_github_repo(cmc)):
            if (release := get_last_github_release(repository[0], repository[1])):
                print(release)
        
        print()

if __name__ == '__main__':
    main()
