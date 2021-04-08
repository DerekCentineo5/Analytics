import datetime as dt
import pandas as pd
import time
import praw
import squarify
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from nltk.sentiment.vader import SentimentIntensityAnalyzer

api = PushshiftAPI()

start_time = int(dt.datetime(2021, 4, 1).timestamp())

submissions = api.search_submissions(after=start_time,
                                    subreddit='wallstreetbets',
                                    filter=['url','author','title','subreddit'])

for submission in submissions:
    print(submission.created_utc)
    print(submission.title)
    print(submission.url)

