from dash import Output, Input, html
from layouts.industry_info import industry_info_layout
from layouts.predict_cancellation import predict_cancellation_layout

# Define the callback function for tabs
def register_callbacks(app):
    @app.callback(
        Output("tab-content", "children"),
        Input("tabs", "value"),
    )
    def update_tab_content(tab_name):
        if tab_name == "industry-info":
            return industry_info_layout
        elif tab_name == "predict-cancellation":
            return predict_cancellation_layout
        return html.Div("404: Tab not found")