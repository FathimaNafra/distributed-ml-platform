from fastapi import APIRouter
from app.models import WorkerRegistration
from app.state import workers

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
