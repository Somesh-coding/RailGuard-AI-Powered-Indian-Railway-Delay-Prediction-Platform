import json
import os
import re

DATA_FILES = [
    "data/EXP-TRAINS.json",
    "data/PASS-TRAINS.json",
    "data/SF-TRAINS.json"
]


def load_all_trains():
    trains = []

    for file_path in DATA_FILES:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

                if isinstance(data, list):
                    trains.extend(data)

    return trains


def clean_station_code(station_name):
    station_name = station_name.strip().upper()

    if "-" in station_name:
        return station_name.split("-")[-1].strip()

    return station_name


def extract_distance(distance_text):
    if not distance_text:
        return 0

    match = re.search(r"\d+", str(distance_text))

    if match:
        return int(match.group())

    return 0


def find_trains_between(source, destination):
    source = source.upper().strip()
    destination = destination.upper().strip()

    all_trains = load_all_trains()
    matched_trains = []

    for train in all_trains:
        route = train.get("trainRoute", [])

        source_index = -1
        destination_index = -1
        source_station = None
        destination_station = None

        for i, stop in enumerate(route):
            station_code = clean_station_code(stop.get("stationName", ""))

            if station_code == source:
                source_index = i
                source_station = stop

            if station_code == destination:
                destination_index = i
                destination_station = stop

        if source_index != -1 and destination_index != -1 and source_index < destination_index:
            source_distance = extract_distance(source_station.get("distance", "0 kms"))
            destination_distance = extract_distance(destination_station.get("distance", "0 kms"))

            journey_distance = destination_distance - source_distance

            matched_trains.append({
                "trainNumber": train.get("trainNumber"),
                "trainName": train.get("trainName"),
                "route": train.get("route"),
                "runningDays": train.get("runningDays"),
                "sourceStation": source_station.get("stationName"),
                "destinationStation": destination_station.get("stationName"),
                "departureTime": source_station.get("departs"),
                "arrivalTime": destination_station.get("arrives"),
                "distance": journey_distance
            })

    return matched_trains