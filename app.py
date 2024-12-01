from dash import Dash, dcc, html, Input, Output
from src import graphics, model, etl
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import layouts from separate files
from callbacks.industry_callbacks import register_industry_callbacks, register_lead_time_callbacks, register_deposit_type_callbacks
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


#df = df.dropna()

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
            style={
                "display": "flex",  # Horizontal layout
                "width": "100%",  # Ensure full width of the screen
            },
            children=[
                # Left Container
                html.Div(
                    style={
                        "width": "48%",
                        "display": "inline-block",
                        "verticalAlign": "top",
                        "padding": "10px"
                    },
                    children=[
                        html.Div(
                            style={"marginBottom": "20px"},
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
                            ],
                        ),
                        dcc.Graph(
                            id="hotel-reservation-evolution",
                            style={"height": "400px"},
                        ),
                    ],
                ),
                        # Right Container (Graph 2)
                html.Div(
                    style={
                        "width": "48%", "display": "inline-block", "verticalAlign": "top"
                    },
                    children=[
                        dcc.Graph(
                            id="year-reservations-cancellation",
                            figure=graphics.year_reservations_cancellation(df),  # Generate graph
                            style={"height": "400px", "width": "100%"},  # Adjust graph size
                        ),
                    ],
                ),
                html.Div(
                    style={
                        "display": "flex",  # Flexbox layout
                        "flexDirection": "column",  # Stack vertically
                        "alignItems": "right",  # Center-align content horizontally
                        "width": "100%",  # Full width
                        "marginTop":"40px"
                    },
                    children = [
                        html.Div(
                            style = {"marginTop":"40px", 
                                     "textAlign": "right",
                                    "backgroundColor": "rgba(240, 240, 240, 0.8)",  # Optional light background
                                    "borderRadius": "5px", 
                                     },
                            children = [
                                dcc.Checklist(
                                    id='show-cancellations',
                                    options=[
                                        {'label': 'Show Cancellations', 'value': 'show_cancelations'}
                                    ],
                                    value=[],  # Default is unchecked
                                    style={"display": "inline-block", "fontSize": "16px", "padding": "5px", "textAlign": "right"}  # Visible and styled
                                ),
                            ],
                        ),
                        dcc.Graph(
                            id='lead-time-distribution',
                            style = {"height": "400px", "width": "100%"}
                        ),
                    ],
                ),
                html.Hr(
                    style={
                        "border": "1px solid gray",  # Thin gray line
                        "width": "95%",  # Slightly narrower than full width
                        "margin": "20px auto",  # Center the line with some spacing
                    }
                ),
                html.Div(
                    style={
                        "padding": "20px",
                    },
                    children=[
                        html.H3(
                            "Filter by Hotel Type",
                            style={"textAlign": "center", "marginBottom": "20px", "color": "#333"},
                            
                        ),
                        dcc.RadioItems(
                            id="hotel-type-filter",
                            options=[
                                {"label": "City Hotel", "value": "City Hotel"},
                                {"label": "Resort Hotel", "value": "Resort Hotel"},
                                {"label": "Both", "value": "Both"},
                            ],
                            value="Both",  # Default value
                            inline=True,  # Display horizontally
                            style={"marginBottom": "20px", "textAlign": "center"},
                        ),
                        html.Div(
                            style={
                                "display": "flex",  # Use flexbox layout
                                "justifyContent": "space-between",  # Ensure equal spacing between graphs
                                "padding": "20px",  # Add padding around the container
                            },
                            
                            children=[
                                # Pie Chart
                                dcc.Graph(
                                    id="deposit-type-pie-chart",
                                    style={"width": "45%"}  # Adjust width to fit side by side
                                ),
                                # Bar Chart
                                dcc.Graph(
                                    id="deposit-type-bar-chart",
                                    style={"width": "45%"}  # Adjust width to fit side by side
                                ),
                            ],
                        ),
                        html.Div(
                            style={
                                "display": "flex",
                                "flexDirection": "column",
                                "alignItems": "center",
                                "padding": "20px",
                            },
                            children=[
                                dcc.Graph(
                                    id="reservation-flow-sankey",
                                    style={"width": "80%", "height": "500px"}  # Adjust graph size
                                ),
                            ],
                        ),
                    ],
                ),
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
register_lead_time_callbacks(app,df)
register_deposit_type_callbacks(app,df)

if __name__ == "__main__":
    app.run_server(debug=True)