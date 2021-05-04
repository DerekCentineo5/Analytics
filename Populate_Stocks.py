import config
import alpaca_trade_api as alpaca
import datetime
import sqlite3
import config
import pandas as pd
from psaw import PushshiftAPI

connection = sqlite3.connect(config.DB_FILE)

connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
    SELECT * FROM stock
""")
rows = cursor.fetchall()

stocks = {}
for row in rows: 
    stocks['$' + row['symbol']] = row['id']

symbols = {}
for row in rows:
    symbols['$' + row['symbol']] = row['symbol']

api = PushshiftAPI()

start_time = int(datetime.datetime(2021, 4, 30).timestamp())

submissions = api.search_submissions(after=start_time,
                                     subreddit='wallstreetbets',
                                     filter=['url','author', 'title', 'subreddit'])
                                    
for submission in submissions:
    words = submission.title.split()
    cashtags = list(set(filter(lambda word: word.lower().startswith('$'), words)))

    if len(cashtags) > 0:
        print(cashtags)
        print(submission.title)

        for cashtag in cashtags:
            if cashtag in stocks and cashtag in symbols:
                submitted_time = datetime.datetime.fromtimestamp(submission.created_utc).isoformat()

                try:
                    cursor.execute("""
                        INSERT INTO mention (dt, stock_id, symbol, message, source, url)
                        VALUES (?, ?, ?, ?, 'wallstreetbets', ?)
                    """, (submitted_time, stocks[cashtag], symbols[cashtag], submission.title, submission.url))

                    connection.commit()

                except Exception as e:
                    print(e)
                    connection.rollback()


