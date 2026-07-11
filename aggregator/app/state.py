workers = {}

current_round = 1

global_model = None

worker_updates = []
aggregation_status = "Waiting"
average_worker_accuracy = 0.0
last_aggregation_time = None
latest_submitted_updates = []
