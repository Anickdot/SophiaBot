import dotenv
import json
import os
import re
import requests

dotenv.load_dotenv()


def get_github_owner_repo(cmc_id: int) -> tuple[str, str]:
    response = requests.get(
        'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info',
        params={'id': cmc_id},
        headers={'X-CMC_PRO_API_KEY': os.environ['CMC_ID']}
    )
    json_object = json.loads(response.content)
    github_url = json_object['data'][str(cmc_id)]['urls']['source_code'][0]
    match = re.search('^https:\/\/github\.com\/(.+)\/(.+)$', github_url)
    return (match[1], match[2])


def get_last_github_release(owner: str, repo: str) -> tuple[str, str]:
    response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/releases')
    json_object = json.loads(response.content)

    return (json_object[0]['tag_name'], json_object[0]['published_at'])


def main():
    owner, repo = get_github_owner_repo(1027)
    version, date = get_last_github_release(owner, repo)
    print(version, date)

if __name__ == '__main__':
    main()
