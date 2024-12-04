from dash import Input, Output
import plotly.graph_objects as go
from src import graphics
from src.graphics import hotel_reservation_evolution, lead_time_distribution
from plotly.subplots import make_subplots


def register_industry_callbacks(app, df, reverse_month_mapping):
    @app.callback(
        Output("hotel-reservation-evolution", "figure"),
        Input("month-range-slider", "value"),
    )
    def update_hotel_reservation_evolution(date_range):
        start_index, end_index = map(int, sorted(date_range))

        start_period = reverse_month_mapping[start_index]
        end_period = reverse_month_mapping[end_index]

        filtered_df = df[
            (df["arrival_month"] >= start_period) & (df["arrival_month"] <= end_period)
        ]

        return hotel_reservation_evolution(filtered_df)
    
def register_lead_time_callbacks(app, df):
    @app.callback(
        Output('lead-time-distribution', 'figure'),
        Input('show-cancellations', 'value')
    )
    def update_lead_time_cancellation(show_cancellations):
        show_cancel = 'show_cancelations' in show_cancellations
        return lead_time_distribution(df, show_cancellations=show_cancel)

def register_deposit_type_callbacks(app,df):
    @app.callback(
        [
            Output("deposit-type-pie-chart", "figure"),
            Output("deposit-type-bar-chart", "figure"),
            Output("reservation-flow-sankey", "figure"),
        ],
        Input("hotel-type-filter", "value")
    )
    def update_graphs(hotel_type):
        if hotel_type == "City Hotel":
            filtered_df = df[df['hotel'] == "City Hotel"]
        elif hotel_type == "Resort Hotel":
            filtered_df = df[df['hotel'] == "Resort Hotel"]
        else:  # Both
            filtered_df = df

        pie_chart = graphics.deposit_type_piechart(filtered_df)
        bar_chart = graphics.deposit_type_barchart(filtered_df)
        sankey_chart = graphics.reservation_flow_sankey(filtered_df)

        return pie_chart, bar_chart, sankey_chart
