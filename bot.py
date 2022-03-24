import os

import dotenv
import requests


def send_message(text: str) -> None:
    dotenv.load_dotenv()

    requests.get(
        f'https://api.telegram.org/bot{os.environ["TOKEN"]}/sendMessage',
        params={'chat_id': os.environ['CHAT_ID'], 'text': text, 'parse_mode': 'HTML'}
    )   
