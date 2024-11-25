from dash import Dash, dcc, html, Input, Output
from src import graphics, model, etl
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Layout of the app
app.layout = html.Div(
    [
        # Header section
        html.Div(
            children=[
                html.H1(
                    "Hotel Cancellations",
                    style={
                        "textAlign": "center",  # Center the title
                        "margin": "0",  # Remove default margin
                        "padding": "20px",  # Add padding for spacing
                        "color": "#333",  # Slightly darker text for readability
                    },
                )
            ],
            style={
                "backgroundColor": "#E4E4E4",  # Light gray background
                "padding": "10px",  # Padding for the entire header
            },
        )
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)