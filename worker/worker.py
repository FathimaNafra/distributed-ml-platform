import socket

from app.config import WORKER_ID, DATASET_PATH
from app.data_loader import load_dataset
from app.register import register_worker
from app.trainer import train_local_model

hostname = socket.gethostname()
worker_ip = socket.gethostbyname(hostname)

print("=" * 50)
print(f"Starting {WORKER_ID}")
print("=" * 50)

print("\nLoading dataset...")
load_dataset()

print("\nRegistering worker...")
response = register_worker(worker_ip)
print(response)

print("\nTraining local model...")
result = train_local_model(DATASET_PATH, WORKER_ID)

print("\nTraining completed!")
print(f"Accuracy : {result['accuracy']:.4f}")
print(f"Model saved at : {result['model_path']}")

print("\nWorker Ready!")
