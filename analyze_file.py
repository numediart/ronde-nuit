'''File used to test analysis sentiment in files.
'''
import argparse

from src.analysis import analyze_file


def parse_args():
    '''Define an argument parser and returns the corresponding dictionary.

    Returns
    -------
    dict
        dictionary of input arguments
    '''
    parser = argparse.ArgumentParser(
        description='Run sentiment analysis using transformers library.')
    parser.add_argument('srcfile', type=str,
                        help='input file to be analyzed.')
    parser.add_argument('-v', '--version', type=int,
                        default=0,
                        help='version of analyzer. 0 is CamemBERT, 1 is transformers\' default.')
    parser.add_argument('-t', '--threshold', type=float,
                        default=0.6666,
                        help='threshold for neutral label. Any score below the threshold (positive or negative) is considered neutral.')
    opt = parser.parse_args()

    return opt


if __name__ == '__main__':
    # Load parameters
    opt = parse_args()

    analyze_file(opt.srcfile, opt.version, opt.threshold)
