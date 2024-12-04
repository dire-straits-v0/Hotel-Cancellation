import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report
from sklearn.preprocessing import StandardScaler
import pickle
import graphics

file = "C:\\Users\\arias\\OneDrive - Universidad Pontificia Comillas\\AÑO 5\\Visualización\\Hotel Cancellation\\data\\clean_hotel_bookings.csv" 

df = pd.read_csv(file)
    
X = df.drop(columns=['is_canceled'])
y = df['is_canceled']

X = pd.get_dummies(X)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42, stratify=y)

model = LogisticRegression(max_iter=500, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]
metrics = {
    "accuracy": accuracy_score(y_test, y_pred),
    "precision": precision_score(y_test, y_pred),
    "recall": recall_score(y_test, y_pred),
    "classification_report": classification_report(y_test, y_pred)
}
feature_importances = dict(zip(X.columns, abs(model.coef_[0])))

with open("model.pkl", "wb") as f:
    pickle.dump(
        {
            "model": model,
            "metrics": metrics,
            "feature_importances": feature_importances,
        },
        f,
    )

with open("feature_importances.pkl", "wb") as f:
    pickle.dump(feature_importances, f)

feature_importance_graph = graphics.plot_feature_importances(feature_importances)
feature_importance_graph.write_html("feature_importance_graph.html")

