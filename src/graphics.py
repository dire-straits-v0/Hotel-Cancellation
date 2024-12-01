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
        height = 500,
        width = 750,
        yaxis=dict(
            gridcolor='lightgrey',  # Y-axis gridline color
            zerolinecolor='green'   # Y-axis zero line color
        )
    )

    return fig

def year_reservations_cancellation(df):

    # Extract the year from arrival_date
    df['arrival_year'] = df['arrival_date'].dt.year

    # Map is_canceled to 'Canceled' or 'Not Canceled'
    df['cancellation_status'] = df['is_canceled'].replace({0: 'Not Canceled', 1: 'Canceled'})

    # Map hotel type to readable labels
    df['hotel'] = df['hotel'].replace({'City Hotel': 'City Hotel', 'Resort Hotel': 'Resort Hotel'})

    # Group by year, hotel type, and cancellation status
    yearly_reservations = df.groupby(['arrival_year', 'hotel', 'cancellation_status']).size().reset_index(name='reservations')
    # Create the bar chart
    fig = px.bar(
        yearly_reservations,
        x='arrival_year',
        y='reservations',
        color='cancellation_status',
        barmode='stack',
        facet_col='hotel',  # Separate charts for City Hotel and Resort Hotel
        labels={
            'arrival_year': 'Year',
            'reservations': 'Number of Reservations',
            'cancellation_status': 'Reservation Status',
            'hotel': 'Hotel Type'
        },
        title='Total Reservations per Year by Hotel Type, with Cancellation Status',
        category_orders={
            'cancellation_status': ["Not Canceled", "Canceled"],  # Set the stacking order
            'hotel': ["City Hotel", "Resort Hotel"]  # Order for hotel types
        }
        #color_discrete_map=custom_colors_right  # Uncomment to apply custom colors
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background for the entire figure
        plot_bgcolor='rgba(0,0,0,0)',
        height = 500,
        width = 750
    )

    return fig

def lead_time_distribution(df):
    # Calculate the total cancellations per lead time
    cancellations_per_lead_time = df[df['is_canceled'] == 1].groupby('lead_time').size().reset_index(name='cancellations')
    
    # Create the histogram with Plotly Express
    fig = px.histogram(df, x="lead_time", color="hotel", marginal="box", nbins=50,
                       title="Distribution of Lead Time by Hotel Type",
                       labels={"lead_time": "Lead Time (Days)", "hotel": "Hotel Type"})
    
    # Add the line trace for total cancellations
    fig.add_trace(
        go.Scatter(
            x=cancellations_per_lead_time['lead_time'],
            y=cancellations_per_lead_time['cancellations'],
            mode='lines+markers',
            name='Total Cancellations',
            line=dict(color='red', width=2, dash='dash')  # Customize the line style
        )
    )
    # Update the layout
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background for the entire figure
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(
            title="Count",
            gridcolor='lightgrey',  # Y-axis gridline color
            zerolinecolor='green'   # Y-axis zero line color
        ),
        xaxis=dict(title="Lead Time (Days)")
    )
    
    return fig