import concurrent.futures
import random


from helpers.get_metrics import get_average_accuracy

# Careful not to use too many threads due to rate limiting
def parallel_evaluate(data, func, num_threads=4, batch_size=100, solution=False, cot=False, voting = 1):
    """
    Parallelizes the evaluation process using threads.
    Args:
    - data: List of data to evaluate.
    - func: The function to evaluate on each batch of data.
    - num_threads: Number of threads to use.
    - batch_size: Number of items per batch.

    Returns:
    - Combined statistics across all threads.
    """
    random.shuffle(data)  # Shuffle the data to get a random subset
    data_batches = [data[i:i + batch_size] for i in range(0, len(data), batch_size)]

    combined_tracker = []
    combined_logs = []

    def wrapper(batch):
        """
        Wrapper to pass additional arguments to func.
        """
        return func(batch, solution, cot, voting)

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = list(executor.map(wrapper, data_batches))

    # Aggregate results
    for res_tracker, _, res_logs in results:
        combined_tracker.extend(res_tracker)  # Ensure stat_tracker is a list
        combined_logs.extend(res_logs)

    # Calculate average accuracy from individual tracker items
    average_accuracy, cleaned_tracker = get_average_accuracy(combined_tracker)

    return cleaned_tracker, average_accuracy, combined_logs
