import os
import pandas as pd


def save_evaluation_result_with_versioning(tracker, filename, folder):
    """
    Save the evaluation results from a list of dictionaries to a CSV file with versioned folder management inside the base folder.

    Args:
        tracker (list): A list of dictionaries containing evaluation data.
        filename (str): The name of the file to save the results to.
        folder (str): The base folder where the file should be saved.
    """

    # Ensure the base folder exists
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    # Create versioned subfolders inside the base folder
    version = 1
    versioned_folder = os.path.join(folder, str(version))
    while os.path.exists(versioned_folder):
        version += 1
        versioned_folder = os.path.join(folder, str(version))

    # Create the final versioned folder
    os.makedirs(versioned_folder, exist_ok=True)

    # Define the full path for the file
    full_path = os.path.join(versioned_folder, filename)

    # Convert the tracker list to a DataFrame
    df = pd.DataFrame(tracker)

    # Flatten 'evaluation_result'
    eval_df = df['evaluation_result'].apply(pd.Series)

    # Flatten 'submission' and drop specific columns
    submission_df = df['submission'].apply(pd.Series)
    submission_df = submission_df.drop(columns=['human_points', 'modelSolution', 'question', 'answer'], errors='ignore')

    # Concatenate the flattened DataFrames with the original, after dropping the nested columns
    df = pd.concat([df.drop(columns=['evaluation_result', 'submission']), eval_df, submission_df], axis=1)

    # Save the resulting DataFrame to the file
    df.to_csv(full_path, index=False)

    # Return the full path and versioned folder for verification
    return full_path, versioned_folder
