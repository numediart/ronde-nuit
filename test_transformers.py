'''File used to test transformers library on different files.
'''
import argparse
import json
import os

from tqdm import tqdm
from transformers import (AutoTokenizer, TFAutoModelForSequenceClassification,
                          pipeline)


def run_model(srcfile: str,
              outfile: str,
              version: int = 0) -> None:
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

    # CamemBERT trained on Allocine
    if version == 0:
        tokenizer = AutoTokenizer.from_pretrained("tblard/tf-allocine")
        model = TFAutoModelForSequenceClassification.from_pretrained(
            "tblard/tf-allocine")

        nlp = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

    # Default settings
    elif version == 1:
        nlp = pipeline("sentiment-analysis")

    export = []
    for elem in tqdm(data):
        if 'message' in elem:
            result = nlp(elem['message'])[0]
            export .append({
                'message': elem['message'],
                'label': result['label'],
                'score': round(result['score'], 4)
            })

        with open(outfile, 'w') as f:
            json.dump(export, f, indent=4)


def main():
    '''Main function used to parse command line arguments.
    '''
    parser = argparse.ArgumentParser(
        description='Run sentiment analysis using transformers library.')
    parser.add_argument('srcfile', type=str,
                        help='input file to be analyzed.')
    parser.add_argument('outfile', type=str,
                        help='output file containing analysis results.')
    parser.add_argument('-v', '--version', type=int, default=0,
                        help='version of analyzer. 0 is CamemBERT, 1 is transformers\' default.')
    args = parser.parse_args()

    run_model(args.srcfile, args.outfile, args.version)


if __name__ == '__main__':
    main()
