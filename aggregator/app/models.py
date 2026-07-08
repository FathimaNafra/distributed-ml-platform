from pydantic import BaseModel

class WorkerRegistration(BaseModel):
    worker_id: str
    worker_ip: str

class ModelUpdate(BaseModel):
    worker_id: str
    round_number: int
    accuracy: float
    loss: float
    weights: list
