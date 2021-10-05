import glob
import os
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def get_statistics(data):
    print(
        f"Positive ratio: {len(data.loc[data['label'] == 'positive']) / len(data)}")
    print(
        f"Neutral ratio: {len(data.loc[data['label'] == 'neutral']) / len(data)}")
    print(
        f"Negative ratio: {len(data.loc[data['label'] == 'negative']) / len(data)}")


def merge_information(path):
    lower = np.vectorize(str.lower)
    sequences = []
    labels = []
    for elem in glob.glob(os.path.join(path, '*.csv')):
        data = pd.read_csv(elem, delimiter=';')
        data = data.dropna()
        sequences += data['sequence'].to_list()
        labels += data['label'].to_list()

    df = pd.DataFrame()
    df.insert(0, 'label', lower(labels))
    df.insert(0, 'sequence', sequences)
    return df


def select_label_and_store(data: pd.DataFrame, label: str, location: str):
    label_data = data.loc[data['label'] == label]


def create_csv_splits(data, path, test_ratio=0.3):
    train, test = train_test_split(data, test_size=test_ratio)

    os.makedirs(path, exist_ok=True)
    train.to_csv(os.path.join(path, 'train.csv'), index=False)
    test.to_csv(os.path.join(path, 'test.csv'), index=False)


def sort_data(inpath, outpath):
    data = merge_information(inpath)
    create_csv_splits(data, outpath)


def create_splits(path):
    texts = []
    labels = []

    data = pd.read_csv(path)
    data.loc[data['label'] != 'neutral']
    texts = data['sequence'].to_list()
    labels = [0 if x == 'negative' else 1 for x in data['label'].to_list()]

    return texts, labels
