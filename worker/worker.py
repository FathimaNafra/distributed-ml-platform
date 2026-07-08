import socket

from app.data_loader import load_dataset
from app.register import register_worker

hostname = socket.gethostname()

worker_ip = socket.gethostbyname(hostname)

print("Loading dataset...")

dataset = load_dataset()

print("Registering Worker...")

response = register_worker(worker_ip)

print(response)

print("Worker Ready")
