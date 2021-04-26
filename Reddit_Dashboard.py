from psaw import PushshiftAPI
import config
import sqlite3
import datetime
import pandas as pd

connection = sqlite3.connect(config.DB_FILE)

connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
    SELECT id, symbol, name FROM stock
""")

rows = cursor.fetchall()

stocks = {}
for row in rows: 
    stocks['$' + row['symbol']] = row['id']

stocks


api = PushshiftAPI()

start_time = int(datetime.datetime(2021, 4, 24).timestamp())

submissions = api.search_submissions(after=start_time,
                                     subreddit='wallstreetbets',
                                     filter=['url','author', 'title', 'subreddit'])

### CREATE TABLE AND BAR CHART TO COUNT MENTIONS                                    
                                     
for submission in submissions:
    words = submission.title.split()
    cashtags = list(set(filter(lambda word: word.lower().startswith('$'), words)))

    if len(cashtags) > 0:
        print(cashtags)
        print(submission.title)

        for cashtag in cashtags:
            if cashtag in stocks:
                submitted_time = datetime.datetime.fromtimestamp(submission.created_utc).isoformat()

                try:
                    cursor.execute("""
                        INSERT INTO mention (dt, stock_id, message, source, url)
                        VALUES (?, ?, ?, 'wallstreetbets', ?)
                    """, (submitted_time, stocks[cashtag], submission.title, submission.url))
        
                    connection.commit()

                except Exception as e:
                    print(e)
                    connection.rollback()

cursor.execute("""
            INSERT INTO Reddit
	        SELECT count(*) as num_mentions, stock_id, symbol, message
	        FROM mention join stock on stock.id = mention.stock_id
	        group by stock_id, symbol
	        order by num_mentions DESC
""")