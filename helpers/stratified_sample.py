import random
from collections import defaultdict
import math

def stratified_random_sample(data, num_groups=3, exercise_sample_size=10, submissions_per_exercise=5):
    """
    Stratified sampling ensuring diversity in exercises, uniform submissions per exercise, and stratification by `maxPoints`.

    Args:
    - data: The dataset to sample from, where each item has "task_id", "course_slug", and "maxPoints".
    - num_groups: Number of groups to divide the dataset into (e.g., thirds, fifths).
    - exercise_sample_size: Number of exercises to sample from each course.
    - submissions_per_exercise: Number of submissions to sample per exercise.

    Returns:
    - A dictionary containing stratified random samples for each course, formatted for evaluation.
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

        # Collect submissions from sampled exercises with uniform submissions
        sampled_exercises = []
        for exercise_id in sampled_exercise_ids:
            exercise_submissions = exercises[exercise_id]

            # Stratify by `maxPoints`
            sorted_data = sorted(exercise_submissions, key=lambda x: x["maxPoints"])

            # Split data into `num_groups`
            n = len(sorted_data)
            group_size = n // num_groups
            groups = [sorted_data[i * group_size: (i + 1) * group_size] for i in range(num_groups)]

            # Handle remaining data (if not perfectly divisible)
            if n % num_groups != 0:
                groups[-1].extend(sorted_data[num_groups * group_size:])

            # Randomly sample from each group to ensure uniform submissions
            exercise_samples = []
            for group in groups:
                exercise_samples.extend(random.sample(group, min(len(group), submissions_per_exercise // num_groups)))

            # Ensure exact number of submissions per exercise
            while len(exercise_samples) < submissions_per_exercise:
                exercise_samples.append(random.choice(sorted_data))

            sampled_exercises.extend(exercise_samples)

        # Transform data to the required format for evaluation
        formatted_data = []
        for item in sampled_exercises:
            formatted_data.append({
                "question": item.get("instruction", "No instruction provided"),  # Handle missing instructions
                "answer": item.get("content", "No answer provided"),  # Handle missing answers
                "modelSolution": item.get("solution", "No solution provided") if item.get(
                    "solution") is not None else "No solution provided",  # Handle missing solutions
                "rubrics": item.get("rubrics", []) if not isinstance(item.get("rubrics"), float) or not math.isnan(
                    item.get("rubrics", float('nan'))) else [],  # Handle missing rubrics
                "maxPoints": item.get("maxPoints", 0),  # Default to 0 if maxPoints is missing
                "minPoints": 0,  # Default minPoints
                "pointStep": 0.5,  # Default pointStep
                "human_points": item.get("points", 0),  # Default to 0 if points are missing
                "task_id": item.get("task_id", "Unknown task"),  # Default for missing task_id
                "evaluation_id": item.get("evaluation_id", "Unknown evaluation"),  # Default for missing evaluation_id
                "id_x": item.get("id_x", "Unknown submission"),  # Default for missing id_x
            })

        # Store the formatted data for this course
        sampled_data[course] = formatted_data

    return sampled_data
