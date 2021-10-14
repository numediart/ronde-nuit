'''Create a dataset for retraining purpose.
'''
import argparse

from src.dataset import create_splits


def parse_args():
    '''Define an argument parser and returns the corresponding dictionary.

    Returns
    -------
    dict
        dictionary of input arguments
    '''
    parser = argparse.ArgumentParser(
        description='Converts a JSON file into a CSV file.')
    parser.add_argument('path', type=str,
                        help='path to JSON file.')
    parser.add_argument('-c', '--csv', type=str,
                        default='output.csv',
                        help='CSV output file to have conversion.')
    opt = parser.parse_args()

    return opt


if __name__ == '__main__':
    # Load parameters
    opt = parse_args()
