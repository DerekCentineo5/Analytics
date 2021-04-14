from Database import config
import alpaca_trade_api as alpaca
import psycopg2
import datetime
import psycopg2.extras
import asyncpg
import config
from psaw import PushshiftAPI

connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)

cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

api = alpaca.REST(config.API_KEY, config.API_SECRET, base_url=config.API_URL)

assets = api.list_assets()

for asset in assets:
    print(f"Inserting stock {asset.name}{asset.symbol}")
    cursor.execute("""
        INSERT INTO stock (name, symbol, exchange, is_etf)
        VALUES (%s, %s, %s, false)
    """, (asset.name, asset.symbol, asset.exchange))

connection.commit()

###########################################################

connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
cursor.execute("""
    SELECT * FROM stock
""")
rows = cursor.fetchall()

stocks = {}
for row in rows: 
    stocks['$' + row['symbol']] = row['id']


api = PushshiftAPI()

start_time = int(datetime.datetime(2021, 1, 30).timestamp())

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
            if cashtag in stocks:
                submitted_time = datetime.datetime.fromtimestamp(submission.created_utc).isoformat()

                try:
                    cursor.execute("""
                        INSERT INTO mention (dt, stock_id, message, source, url)
                        VALUES (%s, %s, %s, 'wallstreetbets', %s)
                    """, (submitted_time, stocks[cashtag], submission.title, submission.url))

                    connection.commit()
                except Exception as e:
                    print(e)
                    connection.rollback()



