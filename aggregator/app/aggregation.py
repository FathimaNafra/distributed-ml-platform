import numpy as np


def aggregate_models(worker_updates):
    """
    Aggregate worker model weights using simple averaging.
    """

    if not worker_updates:
        return None

    all_weights = [update["weights"] for update in worker_updates]

    averaged_weights = np.mean(np.array(all_weights), axis=0)

    return averaged_weights.tolist()
