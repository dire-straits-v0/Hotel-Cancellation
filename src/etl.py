import pandas as pd
import pickle

def load_data():
    file = "data/clean_hotel_bookings.csv" 
    df = pd.read_csv(file)

    df["arrival_date"] = pd.to_datetime(df["arrival_date"], errors="coerce")
    df["arrival_month"] = df["arrival_date"].dt.to_period("M")

    return df

def load_model_data():
    
    with open("src/feature_importances.pkl", "rb") as f:
        feature_importances = pickle.load(f)

    with open("src/model.pkl", "rb") as f:
        model_data = pickle.load(f)

    with open("src/form_model.pkl", "rb") as f:
        form_model_data = pickle.load(f)

    return feature_importances, model_data, form_model_data