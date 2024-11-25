from dash import Dash, dcc, html, Input, Output
from src import graphics, model, etl
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import layouts from separate files
from layouts.industry_info import industry_info_layout
from layouts.predict_cancellation import predict_cancellation_layout
from callbacks.tabs_callback import register_callbacks


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
        ),
                # Tabs
        dcc.Tabs(
            id="tabs",
            value="industry-info",
            children=[
                dcc.Tab(label="Industry Information", value="industry-info"),
                dcc.Tab(label="Predict Your Cancellation", value="predict-cancellation"),
            ],
            style={
                "marginTop": "20px",
                "backgroundColor": "#f8f9fa",  # Match header background
            },
            parent_style={
                "display": "flex",  # Ensures tabs align properly
                "justifyContent": "center",  # Center tabs
            },
        ),
        # Content
        html.Div(id="tab-content", style={"padding": "20px"}),
    ],
)

register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)