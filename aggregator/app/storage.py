import json
import os


def save_global_model(global_weights):
    os.makedirs("models", exist_ok=True)

    with open("models/global_model.json", "w") as f:
        json.dump(global_weights, f, indent=4)


def save_training_history(round_number, worker_updates):
    os.makedirs("logs", exist_ok=True)

    history = {
        "round": round_number,
        "workers": worker_updates
    }

    with open("logs/training_history.json", "w") as f:
        json.dump(history, f, indent=4)
