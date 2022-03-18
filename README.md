# SophieBot
Python3.10 бот для проверки новых релизов криптомонет через GitHub

# Как начать
- Создать `.venv` виртуальное окружение через
  ```console
  python3 -m venv .venv
  ```
- Скачать необходимые зависимости через
  ```console
  pip install -r requirements.txt
  ```

- Создать `.env` файл с переменными окружения:
  - CMC_ID - ваш [CoinMarketCap](https://coinmarketcap.com) API ключ
  - TOKEN - токен бота Telegram
  - CHAT_ID - id канала в Telegram

# Алгоритм работы
1. Отправка SQL запроса в **mongo_bridge** для получения списка топовых монет вместе с их cmcId:
    ```sql
    select tc.currency, (select c."cmcId"  from site.currencies c  where c.ticker = tc.currency) from reports.top_15_currencies tc
    ```
2. Запрос на API сайта [CoinMarketCap](https://coinmarketcap.com) для получения ссылки на GitHub для каждой монеты
3. Запрос на API сайта [GitHub](https://github.com) для получения списка всех релизов для каждой монеты
4. Запрос к внутренней базе данных для получения последней актуальной версии каждой монеты
5. Сравнение полученной версии с нашей:
   - Если версии не совпадают, отправка сообщения в Telegram чат со всей необходимой информацией, обновление актуальной версии монеты во внутренней базе данных

# План действий:  
- [x] Составить алгоритм работы программы
- [x] Выбрать стек разработки
- [x] Прототипирование:
  - [x] Написать прототип получения всех релизов для конкретной монеты
  - [x] Написать прототип получения всех релизов для конкретного списка монет
  - [x] Написать механизм для обнаружения нового релиза
- [ ] Тесты:
  - [x] Тестовый деплой бота
  - [ ] Обработка ошибок, нестандартных случаев, чтобы программа не упала
- [ ] Релиз бота с фиксированным списком монет
- [ ] Получить доступ к базе данных mongo_bridge
- [ ] Синк списка топовых монет с БД