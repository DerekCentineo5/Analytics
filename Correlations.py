import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from Jim_Dash import RiskRange
import alpaca_trade_api  as tradeapi


api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)

Global_Indices = ['^GSPC', '^IXIC', '^RUT', '^GSPTSE', '^BVSP','^STOXX50E', '^GDAXI','^N225','^HSI','^AXJO']
US_Sectors = ['XLK','XLP','XLY','XRT','XLI','XLV','IBB','XLB','XLE','XLF','XLC','XLU']
Macrowise = ['ADI', 'ASML', 'TSM', 'ERIC','NOK','EA','ILMN','INTC','MCHP','COST','MELI','SLV', 'QGEN','EWT','SWKS', 'TXN', 'MSFT', 'CCJ', 'GLD', 'XBI', 'PYPL', 'SQ']
Crypto = ['BTC-USD', 'ETH-USD', 'DOT1-USD', 'LINK-USD', 'KSM-USD', 'XRP-USD', 'ATOM1-USD', 'ADA-USD']
Country_ETF = ['SPY','EWC', 'EWW','EWZ', 'ECH', 'EWI','DAX','EWN', 'EWU', 'GREK','TUR','EZA','RSX','INDA','FXI','EWJ','EWY','EWM','EWT','EWA']

def get_bars(symbol, Start, End):
     data = yf.download(symbol, start=Start, end=End)
     RR = RiskRange(Price_Data=data, window=10, length=63, volume_weighted=True, vol_window=10)
     RR_Spread = pd.DataFrame((RR['Bottom RR'] - RR['Trend']), columns=['RR_Spread'])
     RR_Spread = RR_Spread.dropna()
     return RR_Spread
    
get_bars("AAPL", '2020-01-02', '2021-04-19')

def correlation(equity_list):  
    
    df = pd. DataFrame()
    equity_columns = []
    
    # Get symbol history
    for symbol in equity_list:   
        try:
            symbol_df = get_bars(symbol, '2018-01-02', '2021-04-18')
            df = pd.concat([df, symbol_df], axis=1)
            equity_columns.append(symbol)
        except:
            print('Exception with {}'.format(symbol))
            
    df.columns = equity_columns
    
    # Get correlation and sort by sum
    sum_corr = df.corr().sum().sort_values(ascending=True).index.values
    
    return df[sum_corr].corr()

correlation(Macrowise)

plt.figure(figsize=(13, 8))
sns.heatmap(correlation(Macrowise), annot=True)

