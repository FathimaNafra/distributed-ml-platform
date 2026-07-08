import requests

from app.config import AGGREGATOR_URL


def submit_model(worker_id, accuracy, weights):
    payload = {
        "worker_id": worker_id,
        "round_number": 1,
        "accuracy": accuracy,
        "loss": 0.0,
        "weights": weights
    }

    response = requests.post(
        f"{AGGREGATOR_URL}/submit-model",
        json=payload
    )

    return response.json()
