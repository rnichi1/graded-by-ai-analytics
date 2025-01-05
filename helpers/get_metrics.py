from typing import List
import numpy as np

def calculate_mean_absolute_error(llm_scores: List[float], human_scores: List[float]) -> float:
    """
    Calculate the Mean Absolute Error (MAE) between LLM scores and human scores.

    Parameters:
    - llm_scores (List[float]): Scores predicted by the LLM.
    - human_scores (List[float]): Scores given by humans.

    Returns:
    - float: The Mean Absolute Error.
    """
    llm_scores = np.array(llm_scores)
    human_scores = np.array(human_scores)
    return np.mean(np.abs(llm_scores - human_scores))

def calculate_mean_squared_error(llm_scores: List[float], human_scores: List[float]) -> float:
    """
    Calculate the Mean Squared Error (MSE) between LLM scores and human scores.

    Parameters:
    - llm_scores (List[float]): Scores predicted by the LLM.
    - human_scores (List[float]): Scores given by humans.

    Returns:
    - float: The Mean Squared Error.
    """
    llm_scores = np.array(llm_scores)
    human_scores = np.array(human_scores)
    return np.mean((llm_scores - human_scores) ** 2)

def calculate_root_mean_squared_error(llm_scores: List[float], human_scores: List[float]) -> float:
    """
    Calculate the Root Mean Squared Error (RMSE) between LLM scores and human scores.

    Parameters:
    - llm_scores (List[float]): Scores predicted by the LLM.
    - human_scores (List[float]): Scores given by humans.

    Returns:
    - float: The Root Mean Squared Error.
    """
    mse = calculate_mean_squared_error(llm_scores, human_scores)
    return np.sqrt(mse)

def calculate_pearson_correlation(llm_scores: List[float], human_scores: List[float]) -> float:
    """
    Calculate the Pearson correlation coefficient between LLM scores and human scores.

    Parameters:
    - llm_scores (List[float]): Scores predicted by the LLM.
    - human_scores (List[float]): Scores given by humans.

    Returns:
    - float: The Pearson correlation coefficient.
    """
    llm_scores = np.array(llm_scores)
    human_scores = np.array(human_scores)
    return np.corrcoef(llm_scores, human_scores)[0, 1]

def calculate_cohens_kappa(annotations_1: List[int], annotations_2: List[int]) -> float:
    """
    Calculate Cohen's Kappa for inter-rater agreement.

    Parameters:
    - annotations_1 (List[int]): First set of annotations (e.g., human scores).
    - annotations_2 (List[int]): Second set of annotations (e.g., LLM scores discretized).

    Returns:
    - float: Cohen's Kappa score.
    """
    from sklearn.metrics import cohen_kappa_score
    return cohen_kappa_score(annotations_1, annotations_2)

def calculate_fleiss_kappa(annotations: List[List[int]]) -> float:
    """
    Calculate Fleiss' Kappa for inter-rater agreement.

    Parameters:
    - annotations (List[List[int]]): A list of lists where each sublist contains annotations from multiple raters for a single item.

    Returns:
    - float: Fleiss' Kappa score.
    """
    from statsmodels.stats.inter_rater import fleiss_kappa
    import pandas as pd
    df = pd.DataFrame(annotations)
    return fleiss_kappa(df, method='fleiss')

def get_average_accuracy(tracker):
    cleaned_tracker = []
    accuracy_sum = 0
    for x in tracker:
        # check nan
        if x['accuracy'] == x['accuracy'] and x['accuracy'] >= 0:
            cleaned_tracker.append(x)
            accuracy_sum += x['accuracy']
        else:
            # Add 0 for wrong data to still count it in the average
            cleaned_tracker.append(0)
    average = accuracy_sum / len(cleaned_tracker)
    return average, cleaned_tracker

# scale proposed by Landis & Koch (1977)
def interpret_agreement_level(score: float) -> str:
    """
    Interpret the agreement level based on Landis & Koch (1977) scale.

    Parameters:
    - score (float): Agreement score (e.g., Kappa, AC1).

    Returns:
    - str: The interpreted agreement level.
    """
    if score < 0.0:
        return "Poor agreement"
    elif 0.0 <= score <= 0.20:
        return "Slight agreement"
    elif 0.21 <= score <= 0.40:
        return "Fair agreement"
    elif 0.41 <= score <= 0.60:
        return "Moderate agreement"
    elif 0.61 <= score <= 0.80:
        return "Substantial agreement"
    elif 0.81 <= score <= 1.00:
        return "Almost perfect agreement"
    else:
        return "Invalid score"

def calculate_gwets_ac1(annotations: List[List[int]]) -> float:
    """
    Calculate Gwet's AC1 for inter-rater reliability.

    Parameters:
    - annotations (List[List[int]]): A list of lists where each sublist contains annotations from multiple raters for a single item.

    Returns:
    - float: Gwet's AC1 score.
    """
    # Placeholder for Gwet's AC1 calculation, requires external library or custom implementation
    raise NotImplementedError("Gwet's AC1 calculation requires a specialized implementation or library.")

# Example usage
if __name__ == "__main__":
    llm_scores = [4.5, 3.0, 5.0, 2.5]
    human_scores = [4.0, 3.0, 4.5, 3.0]

    print("Mean Absolute Error:", calculate_mean_absolute_error(llm_scores, human_scores))
    print("Mean Squared Error:", calculate_mean_squared_error(llm_scores, human_scores))
    print("Root Mean Squared Error:", calculate_root_mean_squared_error(llm_scores, human_scores))
    print("Pearson Correlation:", calculate_pearson_correlation(llm_scores, human_scores))

    # Example for Cohen's Kappa
    annotations_1 = [1, 0, 1, 1]  # Human binary classifications
    annotations_2 = [1, 0, 1, 0]  # LLM binary classifications
    print("Cohen's Kappa:", calculate_cohens_kappa(annotations_1, annotations_2))

    # Example for Fleiss' Kappa
    annotations = [[1, 0, 1], [1, 1, 1], [0, 0, 1], [1, 0, 0]]  # Annotations from 3 raters for 4 items
    print("Fleiss' Kappa:", calculate_fleiss_kappa(annotations))
