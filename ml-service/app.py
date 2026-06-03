from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import os

from route_service import find_trains_between

app = FastAPI(
    title="RailGuard ML Service",
    description="Indian Railway delay prediction service",
    version="1.0.0"
)

MODEL_PATH = "model.pkl"
ENCODER_PATH = "encoders.pkl"

if not os.path.exists(MODEL_PATH):
    raise Exception("model.pkl not found. First run: python train_model.py")

if not os.path.exists(ENCODER_PATH):
    raise Exception("encoders.pkl not found. First run: python train_model.py")

model = joblib.load(MODEL_PATH)
encoders = joblib.load(ENCODER_PATH)


class PredictionRequest(BaseModel):
    distance: float
    weather: str
    dayOfWeek: str
    timeOfDay: str
    trainType: str
    routeCongestion: str


class SearchRequest(BaseModel):
    source: str
    destination: str
    weather: str
    dayOfWeek: str
    timeOfDay: str
    routeCongestion: str


def safe_encode(column, value):
    encoder = encoders[column]
    value = str(value)

    if value in encoder.classes_:
        return encoder.transform([value])[0]

    return 0


def get_train_type(train_number):
    train_number = str(train_number)

    if train_number.startswith("12") or train_number.startswith("22"):
        return "Superfast"

    if train_number.startswith("0"):
        return "Express"

    return "Passenger"


def calculate_delay_probability(expected_delay):
    probability = expected_delay * 2

    if probability < 5:
        probability = 5

    if probability > 95:
        probability = 95

    return round(probability, 2)


def calculate_delay_score(delay):
    if delay <= 100:
        return 1
    elif delay <= 200:
        return 2
    elif delay <= 300:
        return 3
    elif delay <= 400:
        return 4
    elif delay <= 500:
        return 5
    elif delay <= 600:
        return 6
    elif delay <= 700:
        return 7
    elif delay <= 800:
        return 8
    elif delay <= 900:
        return 9
    else:
        return 10


def predict_one_train(
    distance,
    weather,
    day_of_week,
    time_of_day,
    train_type,
    route_congestion
):
    input_data = {
        "Distance Between Stations (km)": distance,
        "Weather Conditions": safe_encode("Weather Conditions", weather),
        "Day of the Week": safe_encode("Day of the Week", day_of_week),
        "Time of Day": safe_encode("Time of Day", time_of_day),
        "Train Type": safe_encode("Train Type", train_type),
        "Route Congestion": safe_encode("Route Congestion", route_congestion)
    }

    input_df = pd.DataFrame([input_data])

    expected_delay = float(model.predict(input_df)[0])

    probability = calculate_delay_probability(expected_delay)

    score = calculate_delay_score(expected_delay)

    return expected_delay, probability, score


@app.get("/")
def home():
    return {
        "message": "RailGuard ML Service is running"
    }


@app.post("/predict")
def predict_delay(request: PredictionRequest):
    expected_delay, probability, score = predict_one_train(
        request.distance,
        request.weather,
        request.dayOfWeek,
        request.timeOfDay,
        request.trainType,
        request.routeCongestion
    )

    return {
        "expectedDelay": round(expected_delay, 2),
        "delayProbability": probability,
        "delayScore": score
    }


@app.post("/search-trains")
def search_trains(request: SearchRequest):
    trains = find_trains_between(
        request.source,
        request.destination
    )

    results = []

    for train in trains:
        train_type = get_train_type(train["trainNumber"])

        expected_delay, probability, score = predict_one_train(
            train["distance"],
            request.weather,
            request.dayOfWeek,
            request.timeOfDay,
            train_type,
            request.routeCongestion
        )

        results.append({
            "trainNumber": train["trainNumber"],
            "trainName": train["trainName"],
            "route": train["route"],
            "sourceStation": train["sourceStation"],
            "destinationStation": train["destinationStation"],
            "departureTime": train["departureTime"],
            "arrivalTime": train["arrivalTime"],
            "distance": train["distance"],
            "trainType": train_type,
            "expectedDelay": round(expected_delay, 2),
            "delayProbability": probability,
            "delayScore": score
        })

    results.sort(
        key=lambda x: x["delayScore"],
        reverse=True
    )

    return {
        "source": request.source,
        "destination": request.destination,
        "totalTrains": len(results),
        "trains": results
    }