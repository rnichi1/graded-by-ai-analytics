import random


def stratified_random_sample(data, sample_size=1000, num_groups=3):
    """
    Stratified sampling based on the `points` field.
    Divides the dataset into `num_groups` groups and samples evenly from each.

    Args:
    - data: The dataset to sample from, where each item has a "maxPoints" field.
    - sample_size: Total number of samples to return.
    - num_groups: Number of groups to divide the dataset into (e.g., thirds, fifths).

    Returns:
    - A list containing the stratified random sample.
    """
    # Sort data by `points`
    sorted_data = sorted(data, key=lambda x: x["maxPoints"])

    # Split data into `num_groups`
    n = len(sorted_data)
    group_size = n // num_groups
    groups = [sorted_data[i * group_size: (i + 1) * group_size] for i in range(num_groups)]

    # Handle remaining data (if not perfectly divisible)
    if n % num_groups != 0:
        groups[-1].extend(sorted_data[num_groups * group_size:])

    # Calculate the sample size for each group
    sample_per_group = sample_size // num_groups

    # Randomly sample from each group
    samples = []
    for group in groups:
        samples.extend(random.sample(group, min(len(group), sample_per_group)))

    # If total samples are less than required, fill the rest randomly
    while len(samples) < sample_size:
        samples.append(random.choice(sorted_data))

    return samples
