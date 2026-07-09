from fastapi import APIRouter
from app.models import WorkerRegistration, ModelUpdate
from app.state import (
    workers,
    worker_updates,
    current_round,
    aggregation_status,
    average_worker_accuracy,
    last_aggregation_time
)
from app.aggregation import aggregate_models
from app.storage import save_global_model, save_training_history
from datetime import datetime
router = APIRouter()


@router.get("/")
def home():
    return {
        "service": "Aggregator",
        "status": "Running"
    }


@router.post("/register")
def register_worker(worker: WorkerRegistration):
    workers[worker.worker_id] = {
        "ip": worker.worker_ip,
        "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Online"
    }

    return {
        "message": "Worker Registered",
        "workers": len(workers)
    }
@router.get("/workers")
def get_workers():
    return workers


@router.post("/submit-model")
def submit_model(update: ModelUpdate):

    worker_updates.append(update.model_dump())

    return {
        "message": "Model received successfully",
        "received_updates": len(worker_updates)
    }


@router.get("/updates")
def get_updates():
    return worker_updates


@router.post("/aggregate")
def aggregate():

    global current_round
    global aggregation_status
    global average_worker_accuracy
    global last_aggregation_time

    global_weights = aggregate_models(worker_updates)

    if global_weights is None:
        return {
            "message": "No worker updates available."
        }

    save_global_model(global_weights)

    average_worker_accuracy = sum(
        worker["accuracy"] for worker in worker_updates
    ) / len(worker_updates)

    save_training_history(
        round_number=current_round,
        worker_updates=worker_updates
    )

    aggregation_status = "Completed"

    from datetime import datetime
    last_aggregation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    response = {
        "message": "Global model created successfully.",
        "round": current_round,
        "workers_used": len(worker_updates),
        "average_worker_accuracy": round(average_worker_accuracy, 4),
        "global_weights": global_weights
    }

    worker_updates.clear()

    current_round += 1

    return response


@router.get("/status")
def get_status():

    return {
        "current_round": current_round,
        "registered_workers": len(workers),
        "registered_worker_ids": list(workers.keys()),
        "pending_updates": len(worker_updates),
        "aggregation_status": aggregation_status,
        "average_worker_accuracy": round(average_worker_accuracy, 4),
        "last_aggregation_time": last_aggregation_time
    }
@router.get("/api-info")
def api_info():
    return {
        "service": "Distributed ML Aggregator",
        "version": "1.0",
        "endpoints": {
            "register": "/register",
            "submit_model": "/submit-model",
            "aggregate": "/aggregate",
            "status": "/status"
        }
    }
@router.get("/worker-locations")
def worker_locations():
    return workers
