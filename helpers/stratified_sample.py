import random
from collections import defaultdict

def stratified_random_sample(data, sample_size=1000, num_groups=3, exercise_sample_size=10):
    """
    Stratified sampling ensuring diversity in exercises and stratification by `maxPoints`.

    Args:
    - data: The dataset to sample from, where each item has "task_id", "course_slug", and "maxPoints".
    - sample_size: Total number of samples to return (combined across all courses).
    - num_groups: Number of groups to divide the dataset into (e.g., thirds, fifths).
    - exercise_sample_size: Number of exercises to sample from each course.

    Returns:
    - A dictionary containing stratified random samples for each course.
    """
    # Separate data by course_slug
    courses = defaultdict(list)
    for item in data:
        courses[item["course_slug"]].append(item)

    sampled_data = {}

    for course, course_data in courses.items():
        # Group data by task_id within the course
        exercises = defaultdict(list)
        for item in course_data:
            exercises[item["task_id"]].append(item)

        # Randomly sample a subset of exercises
        exercise_ids = list(exercises.keys())
        sampled_exercise_ids = random.sample(exercise_ids, min(len(exercise_ids), exercise_sample_size))

        # Collect submissions from sampled exercises
        sampled_exercises = []
        for exercise_id in sampled_exercise_ids:
            sampled_exercises.extend(exercises[exercise_id])

        # Stratify by `maxPoints`
        sorted_data = sorted(sampled_exercises, key=lambda x: x["maxPoints"])

        # Split data into `num_groups`
        n = len(sorted_data)
        group_size = n // num_groups
        groups = [sorted_data[i * group_size: (i + 1) * group_size] for i in range(num_groups)]

        # Handle remaining data (if not perfectly divisible)
        if n % num_groups != 0:
            groups[-1].extend(sorted_data[num_groups * group_size:])

        # Calculate the sample size for each group
        sample_per_group = sample_size // (len(courses) * num_groups)

        # Randomly sample from each group
        samples = []
        for group in groups:
            samples.extend(random.sample(group, min(len(group), sample_per_group)))

        # If total samples are less than required for this course, fill the rest randomly
        while len(samples) < sample_size // len(courses):
            samples.append(random.choice(sorted_data))

        # Store the sampled data for this course
        sampled_data[course] = samples

    return sampled_data
