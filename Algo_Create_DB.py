import sqlite3
import config

connection = sqlite3.connect(config.DB_FILE)
    
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock (
        id INTEGER PRIMARY KEY, 
        symbol TEXT NOT NULL UNIQUE, 
        name TEXT NOT NULL,
        exchange TEXT NOT NULL
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_price (
        id INTEGER PRIMARY KEY, 
        stock_id INTEGER,
        datetime NOT NULL,
        open NOT NULL, 
        high NOT NULL, 
        low NOT NULL, 
        close NOT NULL, 
        volume NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES stock (id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS strategy (
        id INTEGER PRIMARY KEY,
        name NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_strategy (
        stock_id INTEGER NOT NULL,
        strategy_id INTEGER NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES stock (id),
        FOREIGN KEY (strategy_id) REFERENCES strategy (id)
    )
""")

cursor.execute("""
    CREATE TABLE mention (
    stock_id INTEGER, 
        dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
        message TEXT NOT NULL,
        source TEXT NOT NULL,
        url TEXT NOT NULL,
        PRIMARY KEY (stock_id, dt),
        CONSTRAINT fk_mention_stock FOREIGN KEY (stock_id) REFERENCES stock (id)

    )
    
""")

cursor.execute("""
        SELECT symbol, message, url, dt
        FROM mention JOIN stock ON stock.id = mention.stock_id
""")

cursor.execute("""
    CREATE INDEX ON mention (stock_id, dt DESC)
""")
cursor.execute("""
    SELECT create_hypertable('mention', 'dt')
""")

strategies = ['opening_range_breakout', 'Risk_Ranges']

for strategy in strategies:
    cursor.execute("""
    INSERT INTO strategy (name) VALUES (?)
""", (strategy,))

connection.commit()