from dash import Dash, dcc, html, Input, Output
from src import graphics, model, etl
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import layouts from separate files
from callbacks.industry_callbacks import register_industry_callbacks
from callbacks.tabs_callback import register_tabs_callback
from layouts.industry_info import industry_info_layout
from layouts.predict_cancellation import predict_cancellation_layout

# Load your dataset
file = "C:\\Users\\arias\\OneDrive - Universidad Pontificia Comillas\\AÑO 5\\Visualización\\Hotel Cancellation\\data\\clean_hotel_bookings.csv" 

df = pd.read_csv(file)  # Adjust path as necessary

df["arrival_date"] = pd.to_datetime(df["arrival_date"], errors="coerce")
df["arrival_month"] = df["arrival_date"].dt.to_period("M")
unique_months = sorted(df["arrival_month"].unique())
reverse_month_mapping = {i: month for i, month in enumerate(unique_months)}
slider_marks = {
    i: month.strftime("%Y-%m") for i, month in enumerate(unique_months) if i % 6 == 0
}

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
                # Industry Information Content (static but dynamically displayed)
        html.Div(
            id="industry-info-content",
            style={"display": "block"},
            children=[
                html.P(
                    "Select Date Range",
                    style={"fontSize": "14px", "textAlign": "center"},
                ),
                dcc.RangeSlider(
                    id="month-range-slider",
                    min=0,
                    max=len(unique_months) - 1,
                    value=[0, len(unique_months) - 1],
                    marks=slider_marks,
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
                dcc.Graph(id="hotel-reservation-evolution"),
            ],
        ),
        # Predict Your Cancellation Content (hidden by default)
        html.Div(
            id="predict-cancellation-content",
            style={"display": "none"},
            children=[
                html.P("Predict Your Cancellation tab content."),
            ],
        ),
    ],
)

# Register callbacks
register_tabs_callback(app)
register_industry_callbacks(app, df, reverse_month_mapping)

if __name__ == "__main__":
    app.run_server(debug=True)