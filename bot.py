import json
import os
import re

import dotenv
import requests

from database import Database

dotenv.load_dotenv()

def send_message(token: str, chat_id: str, text: str) -> None:
    requests.get(
        f'https://api.telegram.org/bot{token}/sendMessage',
        params={'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
    )

def get_local_github(database: Database, ticker: str) -> tuple[str, str] | None:
    database.cursor.execute('SELECT * FROM github WHERE currency = %s;', (ticker, ))
    responce = database.cursor.fetchall()

    if len(responce):
        return (responce[0][1], responce[0][2])

def get_github(cmc_id: int) -> tuple[str, str] | None:
    response = requests.get(
        'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info',
        params={'id': cmc_id},
        headers={'X-CMC_PRO_API_KEY': os.environ['CMC_ID']}
    )
    json_object = json.loads(response.content)

    try:
        source_code = json_object['data'][str(cmc_id)]['urls']['source_code']
    except KeyError as e:
        send_message(os.environ['TOKEN'], os.environ['CHAT_ID'], f'Ошибка парсинга CMC ответа для ID={cmc_id}\n\n\n{e.with_traceback()}')
    else:
        if not len(source_code):
            return

        for scode in source_code:
            if (match := re.fullmatch('^https:\/\/github\.com\/(.+)\/(.+)$', scode)):
                return (match[1], match[2])

def get_last_release(owner: str, name: str) -> str:
    response = requests.get(f'https://api.github.com/repos/{owner}/{name}/releases')
    json_object = json.loads(response.content)
    
    if not isinstance(json_object, list):
        send_message(os.environ['TOKEN'], os.environ['ADMIN_ID'], 'Превышен лимит запросов на GitHub')
        raise ConnectionError

    if not len(json_object):
        return '0'
    
    return json_object[0]['tag_name']

def update_local_db(database: Database, currency: str, version: str) -> bool:
    database.cursor.execute('SELECT * from local_currencies WHERE currency = %s;', (currency, ))
    responce = database.cursor.fetchall()

    if not responce:
        database.cursor.execute('INSERT INTO local_currencies (currency, version) VALUES (%s, %s)', (currency, version))
        return False

    if responce[0][1] == version:
        return False
    
    database.cursor.execute('UPDATE local_currencies SET version = %s WHERE currency = %s', (version, currency))
    return True
