import os

import dotenv
import telebot

def send_message(text: str) -> None:
    dotenv.load_dotenv()

    bot = telebot.TeleBot(os.environ['TOKEN'])

    bot.send_message(os.environ['CHAT_ID'], text, parse_mode='HTML')
