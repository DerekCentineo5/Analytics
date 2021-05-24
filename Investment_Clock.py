import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

Data = pd.read_csv('Productivity Data.csv', index_col=0,parse_dates=True)
Data

fig = go.Figure(data=go.Scatter(x=Data['10YR_1st_Diff'], y=Data['Productivity(YoY)_1st_Diff'], text = Data.index, mode = 'markers',name="Investment Clock"))
fig.show()









fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Scatter(x=Data.index, y=Data['Productivity'], name="Productivity (RHS)", marker_color='green'), secondary_y=False)

fig1.add_trace(go.Scatter(x=Data.index, y=Data['Inflation'], name='Inflation (LHS)'), secondary_y=True)

fig1.update_xaxes(title_text='Date')
fig1.update_yaxes(title_text='Productivity', secondary_y=False)
fig1.update_yaxes(title_text='Inflation', secondary_y=True)

fig1.show()
