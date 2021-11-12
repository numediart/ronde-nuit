import glob
import os

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def print_ratio(data: pd.DataFrame,
                label: str) -> None:
    '''Print ratio of a given label

    Args
    ----
    data : pd.DataFrame
        DataFrame where labels come from
    label : str
        label to get ratio of. Can either be 'positive', 'negative' or 'neutral'
    '''
    print(
        f"{label} ratio: {len(data.loc[data['label'] == label.lower()]) / len(data)}")


def get_statistics(data: pd.DataFrame,
                   neutral=True) -> None:
    '''Print statistics of each label in the dataset.

    Args
    ----
    data : pd.DataFrame
        DataFrame where labels come from

    '''
    if not neutral:
        data = data.loc[data['label'] != 'neutral']
    print_ratio(data, "Positive")

    if neutral:
        print_ratio(data, "Neutral")
    print_ratio(data, "Negative")


def merge_information(path: str) -> pd.DataFrame:
    '''Merge information from csv in the same folder.

    Args
    ----
    path : str
        path to the folder containing all the csv 

    Returns
    -------
    pd.DataFrame
        DataFrame containing the messages and their label from each CSV
    '''
    # Define lower fonction for an array
    lower = np.vectorize(str.lower)

    # Init columns
    sequences = []
    labels = []

    # CSVs are delimited with semicolumns (;)
    # CSVs should have message and label columns
    for elem in glob.glob(os.path.join(path, '*.csv')):
        data = pd.read_csv(elem, delimiter=';')
        data = data.dropna()  # Skipped annotation are converted to NaN
        sequences += data['message'].to_list()
        labels += data['label'].to_list()

    # Create the dataframe
    df = pd.DataFrame()
    df.insert(0, 'label', lower(labels))
    df.insert(0, 'sequence', sequences)
    return df


def create_csv_splits(data: pd.DataFrame,
                      path: str,
                      test_ratio: float = 0.3) -> None:
    '''Create CSV files for training and testing.

    Args
    ----
    data : pd.DataFrame
        DataFrame containing all the annotated data.
    path : str
        path to the folder that will contain train.csv and test.csv
    test_ratio : float, optional
        percentage of data that will be used for testing.
        Default is 0.3.
    '''
    train, test = train_test_split(data, test_size=test_ratio)

    os.makedirs(path, exist_ok=True)
    train.to_csv(os.path.join(path, 'train.csv'), index=False)
    test.to_csv(os.path.join(path, 'test.csv'), index=False)


def create_dataset(infolder: str,
                   outfolder: str,
                   test_ratio: float = 0.3,
                   verbose: bool = True) -> None:
    '''Creates a dataset of retraining based on annotated CSVs.

    Args
    ----
    infolder : str
        folder containing all annotated CSVs
    outfolder : str
        folder that will contain CSVs for training (train.csv and test.csv)
    test_ratio : float, optional
        percentage of data that will be used for testing.
        Default is 0.3.
    verbose : bool, optional
        Weither to show additional information while running.
        Default is True.
    '''
    data = merge_information(infolder)
    if verbose:
        get_statistics(data)

    create_csv_splits(data, outfolder, test_ratio)


def get_split(path):
    '''Get a split from a CSV file.

    Args
    ----
    path : str
        path to the CSV file

    Returns
    -------
    tuple of pd.DataFrame
        text and label of the split
    '''
    texts = []
    labels = []

    data = pd.read_csv(path)
    data.loc[data['label'] != 'neutral']
    texts = data['sequence'].to_list()
    labels = [0 if x == 'negative' else 1 for x in data['label'].to_list()]

    return texts, labels
