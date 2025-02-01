# Graded By AI - Experiment and Analysis

## Pre-requisites
- Graded by AI service running at `localhost:4000`
- Python 3.8 or higher

## Installation

1. Clone this repository:

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Project structure

### Data Preparation
The data was read and prepared for the experiment in the file `get_data_stat_mat.ipynb`. The process involved loading
the data from a postgres database dump, cleaning the data, and saving it in a format that can be used for the experiment.

The Banking data was already in CSV format so no pre-processing was needed.

### Experiment
The experiment steps can be found in `experiment.ipynb`. This notebook contains:
- Data sampling and preprocessing
- Model evaluation
- Results aggregation and saving

### Analysis of Results
The analysis of the results can be found in `statistics.ipynb`. This includes:
- Statistical analysis of model performance
- Visualization of results
- Comparative analysis

## Usage

1. Start the Graded by AI service

2. Launch Jupyter Notebook:
   ```bash
   jupyter notebook
   ```

3. Set up data and database:
   - Ensure the data files are available in the `data_banking` directory:
     ```
     data_banking/
     ├── exam_data.csv      # Exam questions and rubrics
     ├── grading.csv        # Student grades per question
     ├── point_adjustments.csv  # Manual grade adjustments
     ├── responses.csv      # Student responses
     ```
   - Configure PostgreSQL database with the following details:
     ```
     Database Name: access
     Host: localhost
     Port: 5432
     User: postgres
     Password: postgres
     ```

4. Open and run the notebooks in the following order:
   - `get_data_stat_mat.ipynb` - for data preparation
   - `experiment.ipynb` - to run the experiments
   - `statistics.ipynb` - to analyze results

## Files Description

- `get_data_stat_mat.ipynb`: Data preparation and cleaning notebook
- `experiment.ipynb`: Main experiment implementation
- `statistics.ipynb`: Statistical analysis and results visualization
- `requirements.txt`: List of Python dependencies