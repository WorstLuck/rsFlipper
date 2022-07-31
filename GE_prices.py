#!/usr/bin/env python
# coding: utf-8

# In[1]:

from modules.get_item import get_item,objects,dfxp

import pandas as pd
import requests
import matplotlib.pyplot as plt
from dash.exceptions import PreventUpdate
from app import app, server
from modules.debugger import show_callbacks

from datetime import datetime
import dash_auth
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_table
import dash_daq as daq
from dash_table.Format import Format
import plotly.express as px

import plotly.graph_objects as go

pd.options.plotting.backend = "plotly"

server = server

name = "Super Saradomin brew flask (6)"
# group = "Airut bones"

group = name

custom_groups =[{'label': i, 'value': i} for i in objects]


app.layout = dbc.Container([
            dbc.Row([
                dbc.Col([
                        dcc.Dropdown(id='Select item',value=name, options=custom_groups)])
                    ]),
            dbc.Row([
                dbc.Col([dcc.Graph(id = 'plot',figure = {'layout': {
                'title': 'Item','autosize':True}})
                        ],width = 12)
                    ])
                            ],fluid=True)
       
@app.callback(Output('plot','figure'),
              Input('Select item','value'))
def getGraph(name):
    group = name
    item = name

    instance = get_item(name,graph='True')
    instance_price = instance.price(group,'day180')
    info = instance_price[1]

    price_frame = pd.DataFrame(info[item + ' graph']['daily'],index=['price']).transpose().reset_index()
    price_frame['index'] = price_frame['index'].apply(lambda x: datetime.fromtimestamp(int(x)/1000).strftime('%Y-%m-%d'))
    price_frame.set_index('index',inplace=True)

    fig = go.Figure()
    fig.update_layout(
    autosize=False,
    width=1920,
    height=1080)
    prices = price_frame.reset_index().rename(columns={'index':'date'})
    windows = [3,7,15,30,45]
    for i in windows:
        prices['average{}'.format(i)] = prices.price.rolling(i).mean()
        fig.add_trace(go.Scatter(x=prices.date, y=prices['average{}'.format(i)],
                        mode='lines',
                        name='Running average over {} days'.format(i)))
    fig.add_trace(go.Scatter(x=prices.date, y=prices.price,
                        mode='lines',
                        name='Price of {}'.format(item)))
    for index,row in dfxp.iterrows():
        if row[0] in list(prices.date):
            fig.add_vrect(
                x0="{}".format(row[0]), x1="{}".format(row[1]),
                fillcolor="LightSalmon",
                layer="below"
            )
    prices.set_index('date',inplace=True)
    prices = prices.astype(object)

    fig.layout.autosize =  True
    # fig.show()
    if name:
        return fig
    else:
        raise PreventUpdate

if __name__ == '__main__':
    print(show_callbacks(app))
    app.run_server(debug=True, port=8037,dev_tools_hot_reload=True,dev_tools_prune_errors=True)

# fig = px.scatter(prices,title=item, template="simple_white",color='Colour')
# px.scatter(prices[['average','Colour']],title=item, template="simple_white",color='Colour')
# display(prices)


# In[ ]:




