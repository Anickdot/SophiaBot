import os

import dotenv
from apscheduler.schedulers.blocking import BlockingScheduler

from bot import (get_github, get_last_release, get_local_github, send_message,
                 update_local_db)
from database import Database

dotenv.load_dotenv()

sched = BlockingScheduler(timezone='Europe/Moscow')

@sched.scheduled_job('cron', hour=13, minute=0)
def job():
    database = Database()

    news = []
    skipped = []

    database.cursor.execute('SELECT * FROM top_currencies;')
    for curr, cmc in database.cursor.fetchall():
        if (repository := get_github(cmc) or get_local_github(database, curr)):
            release = get_last_release(repository[0], repository[1])

            if update_local_db(database, curr, release):
                news.append(f'<a href="https://github.com/{repository[0]}/{repository[1]}/releases">{curr.upper()}</a>: {release}')
        else:
            skipped.append(curr)

    send_message(
        os.environ['TOKEN'], 
        os.environ['CHAT_ID'], 
        'Мониториг топ-30 монет\n' +
        f'<b>Не забудьте</b> вручную проверить следующие монеты: {" ".join(skipped)}\n\n' + 
        'Обновления монет:\n' +
        '\n'.join(news)
    )

    database.cursor.close()

sched.start()
