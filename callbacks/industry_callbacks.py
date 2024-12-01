from dash import Input, Output
import plotly.graph_objects as go
from src.graphics import hotel_reservation_evolution, lead_time_distribution
from plotly.subplots import make_subplots


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
    
def register_lead_time_callbacks(app, df):
    @app.callback(
        Output('lead-time-distribution', 'figure'),
        Input('show-cancellations', 'value')
    )

    def update_lead_time_cancellation(show_cancellations):
        # Create the base filtered dataframe
        filtered_df = df.copy()  # Ensure we start with the full dataset

        # Create the plot with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add histograms for City Hotel and Resort Hotel
        for hotel_type, color in zip(['City Hotel', 'Resort Hotel'], ['blue', 'orange']):
            hotel_data = filtered_df[filtered_df['hotel'] == hotel_type]
            histogram = go.Histogram(
                x=hotel_data['lead_time'],
                nbinsx=50,
                name=f'Lead Time ({hotel_type})',
                marker_color=color,
                opacity=0.7
            )
            fig.add_trace(histogram, secondary_y=False)

        # Conditionally add the cancellation line
        if show_cancellations and 'show_cancelations' in show_cancellations:
            cancellations_per_lead_time = (
                filtered_df[filtered_df['is_canceled'] == 1]
                .groupby('lead_time')
                .size()
                .reset_index(name='cancellations')
            )
            line = go.Scatter(
                x=cancellations_per_lead_time['lead_time'],
                y=cancellations_per_lead_time['cancellations'],
                mode='lines+markers',
                name='Total Cancellations',
                line=dict(color='grey', width=2, dash='dot')  # Grey dotted line
            )
            fig.add_trace(line, secondary_y=True)


        # Update layout
        fig.update_layout(
            barmode = "overlay",
            title="Lead Time Distribution with Optional Cancellation Line",
            xaxis_title="Lead Time (Days)",
            yaxis=dict(title="Count (Reservations)"),
            yaxis2=dict(title="Total Cancellations", overlaying="y", side="right"),
            legend=dict(title="Metrics"),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )

        return fig