'''File used to run transformer's library on different files.
'''
import json
from typing import Tuple

from tqdm import tqdm
from transformers import (AutoTokenizer, TFAutoModelForSequenceClassification,
                          pipeline)


class SentimentAnalyzer():
    def __init__(self,
                 version: int = 0,
                 threshold: float = 0.6666):
        self.version = version
        self.threshold = threshold
        self.select_model()

    def select_model(self):
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
        if self.version == 0:
            tokenizer = AutoTokenizer.from_pretrained("tblard/tf-allocine")
            model = TFAutoModelForSequenceClassification.from_pretrained(
                "tblard/tf-allocine")

            self.name = 'camembert'
            self.nlp = pipeline('sentiment-analysis',
                                model=model, tokenizer=tokenizer)

        # Default settings
        elif self.version == 1:
            self.name = 'default'
            self.nlp = pipeline("sentiment-analysis")

    def analyze(self, msg: str) -> Tuple[float, str]:
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

        result = self.nlp(msg)[0]

        score = result['score']
        label = 'NEUTRAL' if score < self.threshold else result['label']

        return score, label.lower()


def analyze_file(srcfile: str,
                 version: int = 0,
                 threshold: float = 0.6666):
    '''Analyze a messages in a JSON file.

    Args
    ----
    srcfile : file
        path to the file to analyze
    version : int
        version
    '''
    analyzer = SentimentAnalyzer(version, threshold)

    with open(srcfile, 'r') as f:
        data = json.load(f)

    for elem in tqdm(data):
        if 'message' in elem and analyzer.name not in elem:
            score, label = analyzer.analyze(elem['message'])

            elem.update({
                analyzer.name: {
                    'label': label,
                    'score': score
                }
            })

            with open(srcfile, 'w') as f:
                json.dump(data, f, indent=4)


def get_tokens(sentence,
               model="tblard/tf-allocine"):
    '''
    '''
    tokenizer = AutoTokenizer.from_pretrained(model)
    encoded = tokenizer.encode(sentence)
    return [tokenizer.decode([elem]) for elem in encoded]
