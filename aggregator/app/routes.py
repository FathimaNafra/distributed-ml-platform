from fastapi import APIRouter
from app.models import WorkerRegistration, ModelUpdate
from app.state import workers, worker_updates,current_round
from app.aggregation import aggregate_models
from app.storage import save_global_model, save_training_history

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
        "ip": worker.worker_ip
    }

    return {
        "message": "Worker Registered",
        "workers": len(workers)
    }

@router.get("/workers")
def get_workers():
    return workers
@router.post("/aggregate")
def aggregate():

    global current_round

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
