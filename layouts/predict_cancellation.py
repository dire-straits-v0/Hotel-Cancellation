from dash import html

predict_cancellation_layout = html.Div(
    children=[
        html.H3("Predict Your Cancellation", className="text-center mt-4"),
        html.P("This section will include a machine learning model and visualizations."),
    ]
)
