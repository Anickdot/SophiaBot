import requests


def send_message(token: str, chat_id: str, text: str) -> None:
    requests.get(
        f'https://api.telegram.org/bot{token}/sendMessage',
        params={'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
    )
