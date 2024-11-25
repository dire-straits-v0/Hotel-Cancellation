from dash import Output, Input, html
from layouts.industry_info import industry_info_layout
from layouts.predict_cancellation import predict_cancellation_layout

def register_tabs_callback(app):
    @app.callback(
        [
            Output("industry-info-content", "style"),
            Output("predict-cancellation-content", "style"),
        ],
        Input("tabs", "value"),
    )
    def switch_tabs(tab_name):
        if tab_name == "industry-info":
            return {"display": "block"}, {"display": "none"}
        elif tab_name == "predict-cancellation":
            return {"display": "none"}, {"display": "block"}
        return {"display": "none"}, {"display": "none"}
