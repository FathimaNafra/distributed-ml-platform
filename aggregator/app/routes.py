from fastapi import APIRouter
from app.models import WorkerRegistration, ModelUpdate
from app.state import workers, worker_updates
from app.aggregation import aggregate_models
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

    global_weights = aggregate_models(worker_updates)

    if global_weights is None:
        return {
            "message": "No worker updates available."
        }

    return {
        "message": "Global model created successfully.",
        "workers_used": len(worker_updates),
        "global_weights": global_weights
    }

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
