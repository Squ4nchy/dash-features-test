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

# If running from Jupyter Lab/Notebook use this package.
from jupyter_dash import JupyterDash

# If not running from Jupyter Lab/Notebook use dash.Dash().
# from dash import Dash

app = JupyterDash(__name__)
