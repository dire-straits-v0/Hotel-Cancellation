from dash import Dash, dcc, html, Input, Output
from src import graphics, etl
import dash_bootstrap_components as dbc
import pickle
import plotly.io as pio

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import layouts from separate files
from callbacks.industry_callbacks import register_industry_callbacks, register_lead_time_callbacks, register_deposit_type_callbacks
from callbacks.prediction_callbacks import register_prediction_callbacks
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


# Load pre-trained model and feature importances
with open("src/feature_importances.pkl", "rb") as f:
    feature_importances = pickle.load(f)

with open("src/model.pkl", "rb") as f:
    model_data = pickle.load(f)

with open("src/form_model.pkl", "rb") as f:
    form_model_data = pickle.load(f)

# Load the saved graph
feature_importance_graph = graphics.plot_feature_importances(feature_importances)
model = model_data["model"]
metrics = model_data["metrics"]

form_model = form_model_data["model"]
feature_names = form_model_data["feature_names"]

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
                html.H3(
                    "Industry Overview",
                    style={"textAlign": "center", "marginBottom": "20px", "color": "#333", "marginTop": "20px"},
                ),
                html.P(
                    "Evolution of the industry's reservations throughout the years.",
                    style={"textAlign": "center", "marginBottom": "20px", "color": "#333"},
                ),
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
                    ],
                ),
                        # Right Container (Graph 2)
                html.Div(
                        style = {
                            "display": "flex",  # Use flexbox layout
                            "justifyContent": "space-between",  # Ensure equal spacing between graphs
                            "padding": "20px",
                        },  # Add padding around the container},
                        children = [
                            dcc.Graph(
                                id="hotel-reservation-evolution",
                                style={"width": "55%"}
                            ),
                            dcc.Graph(
                                id = "year-reservations-cancellation",
                                figure = graphics.year_reservations_cancellation(df),
                                style={"width": "55%"}
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
                        "display": "flex",  # Flexbox layout
                        "flexDirection": "column",  # Stack vertically
                        "alignItems": "right",  # Center-align content horizontally
                        "width": "100%",  # Full width
                        "marginTop":"40px"
                    },
                    children = [
                        html.H3(
                            "Lead Time",
                            style={"textAlign": "center", "marginBottom": "20px", "color": "#333"},
                        ),
                        html.P(
                            "What effect does lead time have on cancellations?",
                            style={"textAlign": "center", "marginBottom": "20px", "color": "#333"},
                        ),
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
                                        {'label': 'Show Total Cancellations', 'value': 'show_cancelations'}
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
                        html.Div(
                            style = {
                                "display": "flex",  # Use flexbox layout
                                "justifyContent": "space-between",  # Ensure equal spacing between graphs
                                "padding": "20px",
                              },  # Add padding around the container},
                            children = [
                                dcc.Graph(
                                    id="lead-time-cancellation-scatter",
                                    figure=graphics.lead_time_cancellation_scatter(df),  # Call the scatter plot function
                                    style={"width": "55%"}
                            ),
                                dcc.Graph(
                                    id = "lead-time-cancellation-heatmap",
                                    figure = graphics.lead_time_cancellation_heatmap(df),
                                    style={"width": "45%"}
                                ),
                            ],
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
                            "Deposit Types",
                            style={"textAlign": "center", "marginBottom": "20px", "color": "#333"},
                        ),
                        html.P(
                            "Filter by hotel type.",
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
                            style={"marginBottom": "20px", "textAlign": "center", "padding": "10px"},
                            inputStyle={"marginRight": "10px", "marginLeft": "10px"}  # Add space around each radio button
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
                html.H3(
                    "Cancellation Predictor - Overview",
                    style={"textAlign": "center", "marginBottom": "20px", "color": "#333", "marginTop": "20px"},
                ),
                html.Div(
                    style = {
                        "padding": "20px",
                    },
                    children = [
                        graphics.create_metrics_table(metrics), 
                        dcc.Graph(
                            id="feature-importance-graph",
                            figure=feature_importance_graph),
                    ],
                ),
                html.Div(
                    children = [
                        html.H3("Predict Cancellation", style={"textAlign": "center"}),

                        # Input form
                        html.Div(
                            style={"width": "50%", "margin": "0 auto", "padding": "20px"},
                            children=[
                                dbc.Row(
                                    [
                                        dbc.Col(dbc.Label("Requested Parking Spaces"), width=4),
                                        dbc.Col(dbc.Input(id="input-parking", type="number", value=1), width=8),
                                    ],
                                    className="mb-3",
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(dbc.Label("Customer's Previous Cancellations"), width=4),
                                        dbc.Col(dbc.Input(id="input-previous-cancellations", type="number", value=0), width=8),
                                    ],
                                    className="mb-3",
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(dbc.Label("Deposit Type"), width=4),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="input-deposit-type",
                                                options=[
                                                    {"label": "No Deposit", "value": "deposit_type_No Deposit"},
                                                    {"label": "Non Refund", "value": "deposit_type_Non Refund"},
                                                    {"label": "Refundable", "value": "deposit_type_Refundable"},
                                                ],
                                                value="deposit_type_No Deposit",  # Default selection
                                            ),
                                            width=8,
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(dbc.Label("Average Daily Rate (ADR)"), width=4),
                                        dbc.Col(dbc.Input(id="input-adr", type="number", value=100), width=8),
                                    ],
                                    className="mb-3",
                                ),
                                html.Br(),
                                    dbc.Row(
                                        dbc.Col(
                                            dbc.Button(
                                                "Predict Cancellation", 
                                                id="predict-button", 
                                                color="primary",
                                                style={"width": "100%"}  # Make the button span the full width
                                            ),
                                            width=12,
                                        ),
                                        className="mb-3",
                                    ),
                            ],
                        ),

                        # Output section
                        html.Div(
                            id="prediction-output",
                            style={"textAlign": "center", "padding": "20px", "fontSize": "20px"},
                        ),
                    ],
                ),
            ],
        ),
    ],
)

# Register callbacks
register_tabs_callback(app)
register_industry_callbacks(app, df, reverse_month_mapping)
register_lead_time_callbacks(app,df)
register_deposit_type_callbacks(app,df)
register_prediction_callbacks(app, form_model, feature_names)

if __name__ == "__main__":
    app.run_server(debug=True)