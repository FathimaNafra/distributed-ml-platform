import os
from dotenv import load_dotenv

load_dotenv()

WORKER_ID = os.getenv("WORKER_ID")
AGGREGATOR_URL = os.getenv("AGGREGATOR_URL")
DATASET_PATH = os.getenv("DATASET_PATH")
