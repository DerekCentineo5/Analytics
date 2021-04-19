from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import config
import sqlite3
from datetime import date

app = FastAPI()
templates = Jinja2Templates(directory='/Users/derekcentineo/Documents/GitHub/Analytics/Templates')

@app.get("/")
def index(request:Request):

    stock_filter = request.query_params.get('filter', False)

    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    if stock_filter == "new_intraday_highs":
        cursor.execute("""
        SELECT * from (
            SELECT symbol, name, stock_id, max(close), date
            from stock_price join stock on stock.id = stock_price.stock_id
            group by stock_id
            order by symbol  
        ) where date = ?
        """, (date.today().isoformat(),))    
    else:
        cursor.execute("""
        SELECT id, symbol, name FROM stock ORDER BY symbol
        """)    

    rows = cursor.fetchall()

    return templates.TemplateResponse("index.html", {"request": request, "stocks": rows})

@app.get("/stock/{symbol}")
def stock_detail(request:Request, symbol):
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, symbol, name FROM stock WHERE symbol = ?
    """, (symbol, ))    

    row = cursor.fetchone()

    cursor.execute("""
    SELECT * FROM stock_price WHERE stock_id = ? ORDER BY date DESC
    """, (row['id'], ))  

    prices = cursor.fetchall()

    return templates.TemplateResponse("stock_detail.html", {"request": request, "stock": row, "bars": prices})
