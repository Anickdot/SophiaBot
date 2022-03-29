import os

import dotenv

from bot import (get_github, get_last_release, get_local_github, send_message,
                 update_local_db)
from database import Database

dotenv.load_dotenv()

def main():
    database = Database()
    
    result = ''

    database.cursor.execute('SELECT * FROM top_currencies;')
    for curr, cmc in database.cursor.fetchall():
        if (repository := get_github(cmc) or get_local_github(database, curr)):
            release = get_last_release(repository[0], repository[1])

            if update_local_db(database, curr, release):
                result += f'<a href="https://github.com/{repository[0]}/{repository[1]}/releases">{curr.upper()}</a>: {release}\n'
    
    if result:
        result = 'New Token Release:\n' + result
        send_message(os.environ["TOKEN"], os.environ['CHAT_ID'], result)


if __name__ == '__main__':
    main()
