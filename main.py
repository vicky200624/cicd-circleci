from fastapi import FastAPI
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

app = FastAPI()

log_file_path = "/home/vicky/Music/system_logs.txt"

def detect_anomalies():

    # Read log file
    with open(log_file_path, "r") as file:
        logs = file.readlines()

    # Parse logs
    data = []
    for log in logs:
        parts = log.strip().split(" ", 3)

        if len(parts) < 4:
            continue

        timestamp = parts[0] + " " + parts[1]
        level = parts[2]
        message = parts[3]

        data.append([timestamp, level, message])

    df = pd.DataFrame(data, columns=["timestamp", "level", "message"])

    # Convert timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Log level mapping
    level_mapping = {
        "INFO": 1,
        "WARNING": 2,
        "ERROR": 3,
        "CRITICAL": 4
    }

    df["level_score"] = df["level"].map(level_mapping)

    # Message length feature
    df["message_length"] = df["message"].apply(len)

    # Isolation Forest Model
    model = IsolationForest(contamination=0.1, random_state=42)

    df["anomaly"] = model.fit_predict(
        df[["level_score", "message_length"]]
    )

    df["is_anomaly"] = df["anomaly"].apply(
        lambda x: "Anomaly" if x == -1 else "Normal"
    )

    anomalies = df[df["is_anomaly"] == "Anomaly"]

    return anomalies.to_dict(orient="records")


@app.get("/")
def home():
    return {"message": "AI Log Anomaly Detection API"}


@app.get("/detect")
def detect():
    anomalies = detect_anomalies()
    return {
        "total_anomalies": len(anomalies),
        "anomalies": anomalies
    }