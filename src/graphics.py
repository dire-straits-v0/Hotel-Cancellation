import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def hotel_reservation_evolution(df):
    #HOTEL RESERVATION EVOLUTION THROUGHOUT THE MONTHS
    df['arrival_date'] = pd.to_datetime(df['arrival_date'], errors='coerce')

    # Convertimos nuestra variable arrival_date al primer día de cada mes
    df['arrival_month'] = df['arrival_date'].dt.to_period('M')

    # Agrupamos por mes y tipo de hotel
    monthly_reservations = df.groupby(['arrival_month', 'hotel']).size().reset_index(name='reservations')

    monthly_reservations['arrival_month'] = monthly_reservations['arrival_month'].dt.to_timestamp()


    fig = px.line(
        monthly_reservations,
        x='arrival_month',
        y='reservations',
        color='hotel',
        labels={'arrival_month': 'Date', 'reservations': 'Number of Reservations', 'hotel': 'Hotel Type'},
        title = "Monthly Evolution of Hotel Reservations"
        #color_discrete_map=custom_colors_left

    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background for the entire figure
        plot_bgcolor='rgba(0,0,0,0)',
        height = 400,
        width = 600,
        yaxis=dict(
            gridcolor='lightgrey',  # Y-axis gridline color
            zerolinecolor='green'   # Y-axis zero line color
        )
    )

    return fig