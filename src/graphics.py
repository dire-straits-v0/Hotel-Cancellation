import pandas as pd
import dash_table
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

###########-------------------INDUSTRY TAB VISUALIZATIONS-------------------

def hotel_reservation_evolution(df):
    df['arrival_date'] = pd.to_datetime(df['arrival_date'], errors='coerce')

    df['arrival_month'] = df['arrival_date'].dt.to_period('M')

    monthly_reservations = df.groupby(['arrival_month', 'hotel']).size().reset_index(name='reservations')

    monthly_reservations['arrival_month'] = monthly_reservations['arrival_month'].dt.to_timestamp()

    fig = px.line(
        monthly_reservations,
        x='arrival_month',
        y='reservations',
        color='hotel',
        labels={'arrival_month': 'Date', 'reservations': 'Number of Reservations', 'hotel': 'Hotel Type'},
        title = "Monthly Evolution of Hotel Reservations"
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(
            gridcolor='lightgrey', 
            zerolinecolor='green'  
        )
    )

    return fig

def year_reservations_cancellation(df):

    custom_colors = {
        "Not Canceled": "#377eb8",  # Medium-dark blue (~level 20 in the heatmap legend)
        "Canceled": "#a6cee3",      # Light blue (~level 10 in the heatmap legend)
    }

   
    df['arrival_year'] = df['arrival_date'].dt.year

   
    df['cancellation_status'] = df['is_canceled'].replace({0: 'Not Canceled', 1: 'Canceled'})

    
    df['hotel'] = df['hotel'].replace({'City Hotel': 'City Hotel', 'Resort Hotel': 'Resort Hotel'})

    
    yearly_reservations = df.groupby(['arrival_year', 'hotel', 'cancellation_status']).size().reset_index(name='reservations')
    
    fig = px.bar(
        yearly_reservations,
        x='arrival_year',
        y='reservations',
        color='cancellation_status',
        barmode='stack',
        facet_col='hotel',  
        labels={
            'arrival_year': 'Year',
            'reservations': 'Number of Reservations',
            'cancellation_status': 'Reservation Status',
            'hotel': 'Hotel Type'
        },
        title='Cancellations per Year, per Hotel',
        category_orders={
            'cancellation_status': ["Not Canceled", "Canceled"],  
            'hotel': ["City Hotel", "Resort Hotel"]  
        },
        color_discrete_map=custom_colors
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  
        plot_bgcolor='rgba(0,0,0,0)',
    )

    return fig

def lead_time_distribution(df, show_cancellations=False):
    
    color_map = {
        "City Hotel": "#636EFA",
        "Resort Hotel": "#EF553B",     
    }
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    
    for hotel_type, color in zip(df['hotel'].unique(), [None, None]):
        hotel_data = df[df['hotel'] == hotel_type]
        histogram = go.Histogram(
            x=hotel_data['lead_time'],
            nbinsx=50,
            name=f'Lead Time ({hotel_type})',
            marker_color=color_map[hotel_type],
            opacity=0.7
        )
        fig.add_trace(histogram, secondary_y=False)
    
   
    if show_cancellations:
        cancellations_per_lead_time = (
            df[df['is_canceled'] == 1]
            .groupby('lead_time')
            .size()
            .reset_index(name='cancellations')
        )
        line = go.Scatter(
            x=cancellations_per_lead_time['lead_time'],
            y=cancellations_per_lead_time['cancellations'],
            mode='lines+markers',
            name='Total Cancellations',
            line=dict(color='grey', width=2, dash='dot')
        )
        fig.add_trace(line, secondary_y=True)
    
    
    fig.update_layout(
        barmode="overlay",
        title="Lead Time Distribution with Optional Cancellation Line",
        xaxis_title="Lead Time (Days)",
        yaxis=dict(title="Count (Reservations)"),
        yaxis2=dict(title="Total Cancellations", overlaying="y", side="right"),
        legend=dict(title="Metrics"),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    return fig

def lead_time_cancellation_scatter(df):
    lead_time_cancellation = df.groupby(['lead_time', 'hotel']).agg(
        cancellation_rate=('is_canceled', 'mean')
    ).reset_index()

    
    fig = px.scatter(
        lead_time_cancellation,
        x="lead_time",
        y="cancellation_rate",
        color="hotel",
        title="Cancellation Rate vs. Lead Time by Hotel Type",
        labels={
            "lead_time": "Lead Time (Days)",
            "cancellation_rate": "Cancellation Rate",
            "hotel": "Hotel Type"
        }
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(
            gridcolor='lightgrey',  
        )
    )

    
    fig.update_yaxes(tickformat=".0%")

   
    return fig

def lead_time_cancellation_heatmap(df):
    # Group by lead_time and calculate cancellation rate
    heatmap_data = df.groupby('lead_time')['is_canceled'].mean().reset_index()
    heatmap_data['cancellation_rate'] = heatmap_data['is_canceled'] * 100

    custom_colorscale = [
        [0.0, "lightgray"],  
        [0.15, "lightgray"],  
        [0.15, "blue"], 
        [1.0, "darkblue"],  
    ]

    
    fig = px.density_heatmap(
        heatmap_data,
        x='lead_time',
        y='cancellation_rate',
        color_continuous_scale='Blues',
        labels={
            'lead_time': 'Lead Time (Days)',
            'cancellation_rate': 'Cancellation Rate (%)',
        },
        title='Cancellation Rate by Lead Time'
    )

    return fig

def deposit_type_piechart(filtered_df):

    custom_colors = {
        "No Deposit": "#8c0650",   
        "Non Refund": "#c90672",       
        "Refundable": "#ff038e"       
    }
   
    deposit_type_counts = filtered_df['deposit_type'].value_counts().reset_index()
    deposit_type_counts.columns = ['deposit_type', 'count']

    fig = px.pie(
        deposit_type_counts,
        names='deposit_type',
        values='count',
        title='Distribution of Deposit Types',
        color_discrete_map=custom_colors
    )

    fig.update_traces(textinfo='percent+label')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    return fig

def deposit_type_barchart(filtered_df):
    custom_colors = {
        "Not Canceled": "#377eb8",  
        "Canceled": "#a6cee3",      
    }
    
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
        title='Reservations by Deposit Type and Cancellation Status',
        color_discrete_map=custom_colors
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(title='Percentage of Reservations (%)', tickformat=".1f"),
        xaxis=dict(title='Deposit Type'),
        legend_title_text='Reservation Status'
    )

    return fig

def reservation_flow_sankey(filtered_df):
   
    sankey_data = filtered_df.groupby(['deposit_type', 'is_canceled']).size().reset_index(name='count')

   
    total_count = sankey_data['count'].sum()
    sankey_data['percentage'] = (sankey_data['count'] / total_count) * 100

    
    sankey_data['is_canceled_label'] = sankey_data['is_canceled'].replace({
        0: "Not Canceled",
        1: "Canceled"
    })

  
    node_labels = ["No Deposit", "Non Refund", "Refundable", "Canceled", "Not Canceled"]

   
    custom_colors = {
        "Not Canceled": "#377eb8",  
        "Canceled": "#a6cee3"       
    }


    node_colors = [
        "#636EFA", 
        "#EF553B", 
        "#00CC96",
        custom_colors["Canceled"], 
        custom_colors["Not Canceled"]
    ]

    # Prepare source, target, and value data for Sankey links
    sources = [0, 1, 2, 0, 1, 2]  # Indices of source nodes
    targets = [3, 3, 3, 4, 4, 4]  # Indices of target nodes
    values = sankey_data['count'].tolist()
    percentages = sankey_data['percentage'].tolist()

    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=node_labels,
            color=node_colors  
        ),
        link=dict(
            source=sources,  # Source indices
            target=targets,  # Target indices
            value=values,  # Flow values
            color="rgba(150, 150, 150, 0.4)",  
            customdata=percentages, 
            hovertemplate=(
                "Source: %{source.label}<br>" +
                "Target: %{target.label}<br>" +
                "Count: %{value}<br>" +
                "Percentage: %{customdata:.2f}%<extra></extra>"
            )
        )
    )])


    fig.update_layout(
        title_text="Reservation Flow by Deposit Type and Cancellation Status (with Percentages)",
        font_size=12,
        paper_bgcolor='rgba(0,0,0,0)', 
    )

    return fig

###########-------------------PREDICTION TAB VISUALIZATIONS-------------------

def plot_feature_importances(feature_importances: dict, top_n: int = 10):
    """
    Generate an interactive graph of feature importances using Plotly Express.

    Parameters:
    - feature_importances (dict): Dictionary of feature names and their importances.
    - top_n (int): Number of top features to display.

    Returns:
    - fig (plotly.graph_objects.Figure): The Plotly figure object for feature importance graph.
    """
    importance_df = pd.DataFrame(list(feature_importances.items()), columns=["Feature", "Importance"])

    importance_df['BaseFeature'] = importance_df['Feature'].str.split('.').str[0]

    grouped_importances = (
        importance_df.groupby('BaseFeature')['Importance']
        .sum()
        .reset_index()
        .sort_values(by="Importance", ascending=False)  
    )

    top_features = grouped_importances.head(top_n)

    fig = px.bar(
        top_features,
        x="Importance",
        y="BaseFeature",
        orientation="h",
        labels={"Importance": "Importance", "BaseFeature": "Feature"},
        title=f"Top {top_n} Feature Importances",
        color="Importance",  
        color_continuous_scale="Blues"  
    )

 
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  
        plot_bgcolor='rgba(0,0,0,0)', 
        xaxis_title="Importance",
        yaxis_title="Feature",
        showlegend=False,
    )
    
    return fig


def prepare_metrics_table(metrics):
    return [{"Metric": metric_name, "Value": f"{metric_value:.2f}"}
            for metric_name, metric_value in metrics.items()
            if metric_name != "classification_report"]


def create_metrics_table(metrics):
    metrics_data = prepare_metrics_table(metrics)
    return dash_table.DataTable(
        data=metrics_data,
        columns=[
            {"name": "Metric", "id": "Metric"},
            {"name": "Value", "id": "Value"},
        ],
        style_table={"width": "50%", "margin": "0 auto", "padding": "10px"},
        style_header={
            "backgroundColor": "#f4f4f4",
            "fontWeight": "bold",
            "textAlign": "center",
        },
        style_cell={
            "textAlign": "center",
            "padding": "10px",
        },
        style_data={
            "backgroundColor": "#fafafa",
        },
    )