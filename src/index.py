# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:nomarker
#     text_representation:
#       extension: .py
#       format_name: nomarker
#       format_version: '1.0'
#       jupytext_version: 1.13.6
#   kernelspec:
#     display_name: dash
#     language: python
#     name: dash
# ---

import json
from datetime import datetime

import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
from dash import callback_context
from dash.exceptions import PreventUpdate
import flask
from jupyter_dash import JupyterDash
import numpy as np
import pandas as pd
import plotly.express as px

from src.app import app
from src.layouts import layout
from src.scatter_plot import scatter_plot

navbar = dbc.Nav(class_name='nav-bar',
                 children=
                 [
                     html.Img(id='logo', src=app.get_asset_url('logo.png')),
                     dbc.Container(class_name='nav-items', children=
                     [
                         html.Title('Page Navigation', style={'margin-top': '10px'}),
                         dbc.Button(dbc.NavLink(
                             'Home', active='exact', href='/', id='nav-1',
                             external_link=True),
                                    class_name='nav-item', id='nav-item-1',
                                    href='/', external_link=True
                                   ),
                         dbc.Button(dbc.NavLink(
                             'Scatter Plot', active='exact', href='/scatter-plot',
                             id='nav-2', external_link=True),
                                    class_name='nav-item', id='nav-item-2',
                                    href='/scatter-plot', external_link=True
                                   ),
                         
                         html.Div(
                             children=
                             [
                                 html.Title('Section Navigation',
                                            style={'margin-top': '40px'}
                                           ),
                                 dbc.Button(dbc.NavLink(
                                     'User Input', active='exact',
                                     href='#section-1', id='nav-3',
                                     external_link=True),
                                            class_name='nav-item', id='nav-item-3',
                                            href='#section-1', external_link=True
                                           ),
                                 dbc.Button(dbc.NavLink(
                                     'Single Sentence Report', active='exact',
                                     href='#section-2', id='nav-4',
                                     external_link=True),
                                            class_name='nav-item', id='nav-item-4',
                                            href='#section-2', active='exact', external_link=True
                                           )
                             ],
                             id='section-nav'
                             )
                     ]
                                  )
                 ]
                )                       

app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        navbar,
        html.Div(layout, id='content-area', style={'display': 'none'}),
        html.Div(scatter_plot, id='graph-home', className='graph-area')
    ]
)


# Return seperate page to display the homepage or scatter plot
# if the URL changes and hide section nav on scatter plot page.
@app.callback(
    Output('content-area', 'children'),
    Output('content-area', 'style'),
    Output('section-nav', 'style'),
    Input('url', 'pathname'),
    State('scatter-plot', 'style')
)
def switch_pages(pathname, scatter):
    if pathname == '/scatter-plot':
        scatter_plot_page = html.Div(
            children=
            [
                html.H2('User Input: Scatter Plot'),
                scatter_plot
            ],
            id='graph-page', className='graph-area'
        )
        
        return scatter_plot_page, None, {'display': 'none'}
    
    elif pathname == '/':
        return layout, {'display': 'block'}, {'display': 'block'}


# Cycle through nav items and go to the correct navlink's href
# if the related button is clicked.
for i in [1,2,3,4]:
    @app.callback(
        Output(f'nav-{i}', 'n_clicks'),
        Input(f'nav-item-{i}', 'n_clicks')
    )
    def nav_button_clicked(click):
        return click


# When 'enter' is used on the user input,
# click the submit button.
@app.callback(
    Output('button', 'n_clicks'),
    Input('x-value', 'n_submit')
)
def click_submit(enter):
    return +1


# When user data is input store the new value and a random number
# in the browser cookies and return None to clear the input area.
@app.callback(
    Output('x-value', 'value'),
    Output('my-output', 'n_clicks'),
    Input('button', 'n_clicks'),
    State('x-value', 'value')
)    
def get_user_data(click, input_value):
    if input_value is None:
        raise PreventUpdate
    else:
        d = {}
        cookies = dict(flask.request.cookies)
        
        if len(cookies) != 0:
            data = json.loads(cookies['data_values'])
        else:
            data = cookies

        d[len(data)+1] = [np.random.randint(1, 1000), input_value + 5]
        
        data = data | d # Add the temporary dict to the cookies list.
        callback_context.response.set_cookie('data_values', json.dumps(data)) # Set cookie with the newest values included
        
        return None, +1


# Use the stored value to populate the sentence report.
# Only display the sentence when the first value is entered.
@app.callback(
    Output('y-value', 'children'),
    Output('y-value-report', 'style'),
    Input('my-output', 'n_clicks')
)
def display_y_value_sentence(click):
    cookies = dict(flask.request.cookies)
    
    if cookies == {}:
        raise PreventUpdate
    else:
        json_data = json.loads(cookies['data_values'])
        latest_value = json_data[str(len(json_data))]
        
        return f'{latest_value[1]}.', {'display': 'block'}


# Plot a scatter graph, with hover over functionality using stored data.
@app.callback(
    Output('scatter-plot', 'figure'),
    Output('scatter-plot', 'style'),
    Input('my-output', 'n_clicks')
)
def populate_scatter_graph(click):
    cookies = dict(flask.request.cookies)
    
    if cookies == {}:
        raise PreventUpdate
    else:
        data = cookies['data_values']
        json_data = json.loads(data)
        df = pd.DataFrame.from_dict(json_data,
                                    orient='index',
                                    columns=['random-int', 'y-value'])
        fig = px.scatter(
            df, 'random-int', 'y-value',
            hover_data=['y-value']
        )
        
        return fig, {'display': 'block'}
