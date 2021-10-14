'''File used to retrain a sentiment analysis model.
'''
import argparse

from src.retrain import retrain


def parse_args():
    '''Define an argument parser and returns the corresponding dictionary.

    Returns
    -------
    dict
        dictionary of input arguments
    '''
    parser = argparse.ArgumentParser(
        description='Retrain a model.')
    parser.add_argument('folder', type=str,
                        help='path to folder containing data.')
    parser.add_argument('-t', '--token', type=str,
                        default='camembert-base',
                        help='model for tokenisation.')
    parser.add_argument('-s', '--sentiment', type=str,
                        default='tblard/tf-allocine',
                        help='sentiment analysis model to retrain from.')
    opt = parser.parse_args()

    return opt


if __name__ == '__main__':
    # Load parameters
    opt = parse_args()

    retrain(opt.folder, opt.token, opt.sentiment)
