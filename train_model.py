import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
from database import load_data
import config

def train_model():
    data = load_data()
    if not data:
        print("No data to train.")
        return
    
    X, y = [], []
    for record in data:
        for date, daily_data in record["Time Series (Daily)"].items():
            X.append([float(daily_data["1. open"])])
            y.append(float(daily_data["4. close"]))

    # Entrenamos el modelo con los datos históricos
    model = LinearRegression().fit(X, y)
    joblib.dump(model, config.MODEL_PATH)
    print("Model trained and saved.")

if __name__ == "__main__":
    train_model()
