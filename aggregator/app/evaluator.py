import pandas as pd
import joblib
from sklearn.metrics import accuracy_score

def evaluate_global_model():
    model = joblib.load("models/global_model.pkl")

    df = pd.read_csv("datasets/test.csv")

    X = df.drop("TenYearCHD", axis=1)
    y = df["TenYearCHD"]

    predictions = model.predict(X)

    accuracy = accuracy_score(y, predictions)

    return round(accuracy, 4)
