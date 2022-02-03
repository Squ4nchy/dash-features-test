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

from dash import html, dcc

layout = html.Div(
    children=html.Div(className='main', id='content', 
                      children=
                      [
                          html.Div(className='main', id='section-1',
                                   children=
                                   [
                                       html.H4(children='User Input'),
                                       dcc.Input(id='x-value',
                                                 type='number',
                                                 placeholder='Enter your value',
                                                 min=0, max=1000, n_submit=0, n_submit_timestamp=0
                                                ),
                                       html.Button(children='Submit Value',
                                                   id='button',
                                                   n_clicks=0, n_clicks_timestamp=0),
                                       
                                       html.Br(),html.Br(),
                                       
                                       html.Div(id='my-output', hidden=True)
                                   ]
                                  ),
                          
                          html.Div(className='main', id='section-2',
                                   children=[
                                       html.P(id='y-value-report', style={'display': 'none'},
                                              children=[
                                                  'The all-important value driving our business decisions is ',
                                                  html.Span(id='y-value', className='value')
                                              ]
                                             )
                                   ]
                                  )
                      ]
                     )
)
