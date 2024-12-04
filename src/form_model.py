import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report
from sklearn.preprocessing import StandardScaler
import pickle


file = "C:\\Users\\arias\\OneDrive - Universidad Pontificia Comillas\\AÑO 5\\Visualización\\Hotel Cancellation\\data\\clean_hotel_bookings.csv"
df = pd.read_csv(file)


selected_features = ["required_car_parking_spaces", "adr", "previous_cancellations", "deposit_type"]
X = df[selected_features]
y = df["is_canceled"]


X = pd.get_dummies(X) 

feature_names = X.columns.tolist()


scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42, stratify=y)


model = LogisticRegression(max_iter=500, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]


metrics = {
    "accuracy": accuracy_score(y_test, y_pred),
}

# Save the trained model
with open("form_model.pkl", "wb") as f:
    pickle.dump(
        {
            "model": model,
            "metrics": metrics,
            "feature_names": feature_names
        },
        f,
    )


print("Metrics:")
print(metrics)
print("\nFeature Names:")
print(feature_names)

