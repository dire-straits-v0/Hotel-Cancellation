import pandas as pd
from dash import Input, Output
import plotly.graph_objects as go
from src import graphics
from src.graphics import hotel_reservation_evolution, lead_time_distribution

def register_prediction_callbacks(app, model, feature_names):
    @app.callback(
        Output("prediction-output", "children"),
        Input("predict-button", "n_clicks"),
        [
            Input("input-parking", "value"),
            Input("input-adr", "value"),
            Input("input-previous-cancellations", "value"),
            Input("input-deposit-type", "value"),
        ],
    )
    def predict_cancellation(n_clicks, parking, adr, previous_cancellations, deposit_type):
        if n_clicks is None:
            return "Fill in the details and click Predict to see the result."

        # Create a DataFrame with the user inputs
        input_data = pd.DataFrame({
            "required_car_parking_spaces": [parking],
            "adr": [adr],
            "previous_cancellations": [previous_cancellations],
            "deposit_type": [deposit_type],
        })

        # Convert categorical variables to dummy variables
        input_data = pd.get_dummies(input_data, drop_first=True)

        # Add missing columns with default values of 0
        for col in feature_names:
            if col not in input_data.columns:
                input_data[col] = 0

        # Ensure the column order matches the model's expected input
        input_data = input_data[feature_names]

        # Predict using the trained model
        prediction = model.predict(input_data)[0]  # Get the prediction (binary: 0 or 1)
        probability = model.predict_proba(input_data)[0][1]  # Probability of cancellation

        # Generate the output message
        if prediction == 1:
            return f"Prediction: Cancellation Likely ({probability * 100:.2f}% chance)"
        else:
            return f"Prediction: No Cancellation ({(1 - probability) * 100:.2f}% chance)"
