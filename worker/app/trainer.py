import os
import joblib
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def train_local_model(dataset_path, worker_id):
    """
    Train a Logistic Regression model
    using a worker's local dataset.
    """

    # Load dataset
    df = pd.read_csv(dataset_path)

    # Split features and target
    X = df.drop("TenYearCHD", axis=1)
    y = df["TenYearCHD"]

    # Create train and validation sets
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # Create Logistic Regression model
    model = LogisticRegression(
        max_iter=1000
    )

    # Train the model
    model.fit(X_train, y_train)

    # Predict on validation data
    predictions = model.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, predictions)

    # Create models folder if needed
    os.makedirs("models", exist_ok=True)

    # Save trained model
    model_path = f"models/{worker_id}_model.pkl"

    joblib.dump(model, model_path)

    return {
        "accuracy": accuracy,
        "model_path": model_path,
        "weights": model.coef_.tolist(),
        "bias": model.intercept_.tolist()
    }
