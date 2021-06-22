'''File used to run transformer's library on different files.
'''
import argparse
import json
import os

from tqdm import tqdm
from transformers import (AutoTokenizer, TFAutoModelForSequenceClassification,
                          pipeline)


def select_model(version: int):
    '''Returns a sentiment analysis model.

    Args
    ----
    version : int
        defines which model to use.
        0 means using CamemBERT model, 1 is the default pipeline for sentiment-analysis.

    Returns
    -------
    model
        the sentiment analysis pipeline
    str
        a related name for the model
    '''
    # CamemBERT trained on Allocine
    if version == 0:
        tokenizer = AutoTokenizer.from_pretrained("tblard/tf-allocine")
        model = TFAutoModelForSequenceClassification.from_pretrained(
            "tblard/tf-allocine")

        name = 'camembert'
        nlp = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

    # Default settings
    elif version == 1:
        name = 'default'
        nlp = pipeline("sentiment-analysis")

    return nlp, name


def run_model(srcfile: str,
              version: int = 0,
              threshold: float = 0.6666) -> None:
    '''Runs a sentiment-analysis pipeline on a json file.

    Args
    ----
    scrfile : str
        input file, containing sentences to be analyzed.
        File structure should ne a JSON with a list of dictionary with at least
        a 'message' key containing the message to be analyzed.

    outfile : str
        path to the file containing the outputs. File should be a JSON.

    version : optional, int
        defines which model to use.
        0 means using CamemBERT model, 1 is the default pipeline for sentiment-analysis.
        Defaults is 0.
    '''
    with open(srcfile, 'r') as f:
        data = json.load(f)

    nlp, name = select_model(version)

    for elem in tqdm(data):
        if 'message' in elem and name not in elem:
            result = nlp(elem['message'])[0]

            score = round(result['score'], 4)
            label = 'NEUTRAL' if score < threshold else result['label']

            elem.update({
                name: {
                    'label': label,
                    'score': score
                }
            })

            with open(srcfile, 'w') as f:
                json.dump(data, f, indent=4)
