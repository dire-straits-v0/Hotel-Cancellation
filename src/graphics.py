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


def deposit_type_piechart(filtered_df):
    deposit_type_counts = filtered_df['deposit_type'].value_counts().reset_index()
    deposit_type_counts.columns = ['deposit_type', 'count']

    fig = px.pie(
        deposit_type_counts,
        names='deposit_type',
        values='count',
        title='Distribution of Deposit Types',
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    return fig

def deposit_type_barchart(filtered_df):
    filtered_df['cancellation_status'] = filtered_df['is_canceled'].replace({0: 'Not Canceled', 1: 'Canceled'})

    cancellations_by_deposit = filtered_df.groupby(['deposit_type', 'cancellation_status']).size().reset_index(name='count')
    total_by_deposit = cancellations_by_deposit.groupby('deposit_type')['count'].transform('sum')
    cancellations_by_deposit['percentage'] = (cancellations_by_deposit['count'] / total_by_deposit) * 100

    fig = px.bar(
        cancellations_by_deposit,
        x='deposit_type',
        y='percentage',
        color='cancellation_status',
        barmode='stack',
        labels={
            'deposit_type': 'Deposit Type',
            'percentage': 'Percentage of Reservations',
            'cancellation_status': 'Reservation Status',
        },
        category_orders={
            'cancellation_status': ["Not Canceled", "Canceled"]
        },
        title='Reservations by Deposit Type and Cancellation Status'
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(title='Percentage of Reservations (%)', tickformat=".1f"),
        xaxis=dict(title='Deposit Type'),
        legend_title_text='Reservation Status'
    )

    return fig


def lead_time_cancellation_heatmap(df):
    # Group by lead_time and calculate cancellation rate
    heatmap_data = df.groupby('lead_time')['is_canceled'].mean().reset_index()
    heatmap_data['cancellation_rate'] = heatmap_data['is_canceled'] * 100

    # Create heatmap
    fig = px.density_heatmap(
        heatmap_data,
        x='lead_time',
        y='cancellation_rate',
        color_continuous_scale='RdBu',
        labels={
            'lead_time': 'Lead Time (Days)',
            'cancellation_rate': 'Cancellation Rate (%)',
        },
        title='Cancellation Rate by Lead Time'
    )

    return fig

def reservation_flow_sankey(filtered_df):
    sankey_data = filtered_df.groupby(['deposit_type', 'is_canceled']).size().reset_index(name='count')

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=["No Deposit", "Non Refund", "Refundable", "Canceled", "Not Canceled"]
        ),
        link=dict(
            source=[0, 1, 2, 0, 1, 2],
            target=[3, 3, 3, 4, 4, 4],
            value=sankey_data['count'].tolist(),
        )
    )])

    fig.update_layout(title_text="Reservation Flow by Deposit Type and Cancellation Status")
    return fig

def reservation_flow_sankey_with_percentages(df):
    # Group data for Sankey diagram
    sankey_data = df.groupby(['deposit_type', 'is_canceled']).size().reset_index(name='count')

    # Calculate percentages for each link
    total_count = sankey_data['count'].sum()
    sankey_data['percentage'] = (sankey_data['count'] / total_count) * 100

    # Prepare node and link data
    deposit_types = sankey_data['deposit_type'].unique()
    node_labels = list(deposit_types) + ["Canceled", "Not Canceled"]
    deposit_indices = {name: idx for idx, name in enumerate(deposit_types)}
    cancel_indices = {"Canceled": len(deposit_types), "Not Canceled": len(deposit_types) + 1}

    # Create source and target mappings
    sankey_data['source'] = sankey_data['deposit_type'].map(deposit_indices)
    sankey_data['target'] = sankey_data['is_canceled'].map(lambda x: cancel_indices["Canceled"] if x == 1 else cancel_indices["Not Canceled"])

    # Add percentage to hover text
    sankey_data['hover_text'] = sankey_data.apply(
        lambda row: f"{row['count']} ({row['percentage']:.1f}%)",
        axis=1
    )

    # Create the Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=node_labels,
        ),
        link=dict(
            source=sankey_data['source'],
            target=sankey_data['target'],
            value=sankey_data['count'],
            customdata=sankey_data['hover_text'],  # Pass the hover text
            hovertemplate='%{customdata}<extra></extra>',  # Display hover text
        )
    )])

    # Update layout
    fig.update_layout(
        title_text="Reservation Flow by Deposit Type and Cancellation Status (with Percentages)",
        font_size=10
    )

    return fig

