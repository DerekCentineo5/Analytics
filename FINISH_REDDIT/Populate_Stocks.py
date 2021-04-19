from Database import config
import alpaca_trade_api as alpaca
import psycopg2
import datetime
import psycopg2.extras
import asyncpg
import config
import pandas as pd
from psaw import PushshiftAPI

Tickers = pd.read_csv('stock.csv')
Tickers

api = PushshiftAPI()

start_time = int(datetime.datetime(2021, 1, 30).timestamp())

submissions = api.search_submissions(after=start_time,
                                     subreddit='wallstreetbets',
                                     filter=['url','author', 'title', 'subreddit'])
                                     
Data = pd.DataFrame(columns=['Date','Cashtags','Title'])

for submission in submissions:
    words = submission.title.split()
    cashtags = list(set(filter(lambda word: word.lower().startswith('$'), words)))
    timestamp = datetime.datetime.fromtimestamp(submission.created_utc).isoformat()

    Data = Data.append({'Date': submission}, ignore_index=True)

    if len(cashtags) > 0:
        print(cashtags)
        print(submission.title)
        print(timestamp)
        print(Data)    

#Data = Data.append({'Date': timestamp,'Cashtags':cashtags,'Title':submission.title}, ignore_index=True)



