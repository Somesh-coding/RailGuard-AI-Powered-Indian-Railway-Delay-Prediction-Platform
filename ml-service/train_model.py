import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error

DATA_PATH = "data/train delay data.csv"

df = pd.read_csv(DATA_PATH)

df = df.fillna("Unknown")

required_columns = [
    "Distance Between Stations (km)",
    "Weather Conditions",
    "Day of the Week",
    "Time of Day",
    "Train Type",
    "Historical Delay (min)",
    "Route Congestion"
]

for col in required_columns:
    if col not in df.columns:
        raise Exception(f"Missing column: {col}")

feature_cols = [
    "Distance Between Stations (km)",
    "Weather Conditions",
    "Day of the Week",
    "Time of Day",
    "Train Type",
    "Route Congestion"
]

target_col = "Historical Delay (min)"

encoders = {}

categorical_cols = [
    "Weather Conditions",
    "Day of the Week",
    "Time of Day",
    "Train Type",
    "Route Congestion"
]

for col in categorical_cols:
    encoder = LabelEncoder()
    df[col] = encoder.fit_transform(df[col].astype(str))
    encoders[col] = encoder

df["Distance Between Stations (km)"] = pd.to_numeric(
    df["Distance Between Stations (km)"],
    errors="coerce"
)

df[target_col] = pd.to_numeric(
    df[target_col],
    errors="coerce"
)

df = df.dropna()

X = df[feature_cols]
y = df[target_col]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)

print("Model trained successfully")
print("Mean Absolute Error:", mae)

joblib.dump(model, "model.pkl")
joblib.dump(encoders, "encoders.pkl")

print("model.pkl saved")
print("encoders.pkl saved")