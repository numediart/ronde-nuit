'''Create a dataset for retraining purpose.
'''
import argparse

from src.dataset import create_dataset


def parse_args():
    '''Define an argument parser and returns the corresponding dictionary.

    Returns
    -------
    dict
        dictionary of input arguments
    '''
    parser = argparse.ArgumentParser(
        description='Creates a dataset for retraining based on folder of CSV files.')
    parser.add_argument('infolder', type=str,
                        help='path to folder containing annotated CSVs. CSVs should have a message and label column.')
    parser.add_argument('-o', '--outfolder', type=str,
                        default='data/sorted/',
                        help='path to folder that will contain the CSVs.')
    parser.add_argument('-r', '--ratio', type=float,
                        default=0.3,
                        help='percentage of data that will be used for testing.')
    parser.add_argument('-v', '--verbose', type=bool,
                        default=True,
                        help='option to show statistics on data when creating.')
    opt = parser.parse_args()

    return opt


if __name__ == '__main__':
    # Load parameters
    opt = parse_args()

    create_dataset(opt.infolder, opt.outfolder, opt.test_ratio, opt.verbose)
