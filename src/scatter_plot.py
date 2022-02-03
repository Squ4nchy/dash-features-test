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

from dash import dcc, html

scatter_plot = dcc.Graph(id='scatter-plot', style={'display': 'none'})
