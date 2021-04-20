import sqlite3
import pandas as pd


connection = sqlite3.connect(config.DB_FILE)

df = pd.read_sql_query("SELECT * FROM mention", connection)

df.to_csv('Mention.csv')


##M