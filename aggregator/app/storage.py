import json
import os


def save_global_model(global_weights):
    os.makedirs("models", exist_ok=True)

    with open("models/global_model.json", "w") as f:
        json.dump(global_weights, f, indent=4)


def save_training_history(round_number, worker_updates):
    os.makedirs("logs", exist_ok=True)

    history_file = "logs/training_history.json"

    history = []

    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            try:
                history = json.load(f)

                # Convert old dictionary format to list
                if isinstance(history, dict):
                    history = [history]

            except Exception:
                history = []

    average_accuracy = (
        sum(worker["accuracy"] for worker in worker_updates)
        / len(worker_updates)
    )

    history.append({
        "round": round_number,
        "average_accuracy": average_accuracy,
        "workers": worker_updates
    })

    with open(history_file, "w") as f:
        json.dump(history, f, indent=4)
