from __future__ import division, print_function

import json
import warnings

import datasets
import ftfy
import torch
from torch.utils.data import Dataset

from .format import remove_irc_formatting

# Ignore warnings
warnings.filterwarnings("ignore")


labels = {
    'NEGATIVE': 0,
    'POSITIVE': 1,
    'NEUTRAL': 2
}

names = ['neg', 'pos']

DESCRIPTION = """\
Ronde de nuit Dataset.
Dataset developed during the Ronde de nuit project, for sentiment analysis on French language in a specific context.
"""


class RondeDataset(Dataset):
    def __init__(self,
                 filepath='data/dataset.json'):
        with open(filepath, 'r') as f:
            self.data = json.load(f)

    def __len__(self):
        return len(self.data)

    def __get_item__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        elem = self.data[idx]

        msg = elem["message"]
        msg = remove_irc_formatting(elem['message'])
        msg = ftfy.ftfy(msg)

        return {'text': msg, 'label': labels[elem["label"]]}

    def __str__(self):
        data = {
            'features': ['text', 'label'],
            'num_rows': self.__len__()
        }
        return f"Dataset({data})"


class RondeConfig(datasets.BuilderConfig):
    """BuilderConfig for Ronde de nuit dataset."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class RondeBuilder(datasets.DatasetBuilder):
    '''Dataset builder for Ronde de nuit project.
    '''

    BUILDER_CONFIGS = [
        RondeConfig(
            name="ronde-de-nuit",
            version=datasets.Version("1.0.0"),
            description="Ronde de nuit dataset.",
        ),
    ]

    def _info(self):
        '''Returns dataset general info.
        '''
        return datasets.DatasetInfo(
            description=DESCRIPTION,
            features=datasets.Features(
                {
                    "text": datasets.Value(dtype="string", id=None),
                    "label": datasets.ClassLabel(num_classes=2, names=names, names_file=None, id=None),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/numediart/ronde-nuit"
        )

    def _split_generator(self):
        pass

    def _generate_examples(self, filepath):
        """Generate Ronde de nuit examples."""
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                review = data["review"]
                label = "neg" if data["polarity"] == 0 else "pos"
                yield id_, {"review": review, "label": label}


def create_dataset(csvfile):
    dataset = datasets.load_dataset('csv', data_files=csvfile)
