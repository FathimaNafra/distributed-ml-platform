import requests

from app.config import WORKER_ID
from app.config import AGGREGATOR_URL

def register_worker(worker_ip):

    payload = {
        "worker_id": WORKER_ID,
        "worker_ip": worker_ip
    }

    response = requests.post(
        f"{AGGREGATOR_URL}/register",
        json=payload
    )

    return response.json()
