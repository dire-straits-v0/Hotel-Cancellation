from dash import Input, Output
from src.graphics import hotel_reservation_evolution

def register_industry_callbacks(app, df, reverse_month_mapping):
    @app.callback(
        Output("hotel-reservation-evolution", "figure"),
        Input("month-range-slider", "value"),
    )
    def update_hotel_reservation_evolution(date_range):
        start_index, end_index = map(int, sorted(date_range))

        # Map the indices to actual periods
        start_period = reverse_month_mapping[start_index]
        end_period = reverse_month_mapping[end_index]

        # Filter the dataframe
        filtered_df = df[
            (df["arrival_month"] >= start_period) & (df["arrival_month"] <= end_period)
        ]

        # Generate the graph
        return hotel_reservation_evolution(filtered_df)
