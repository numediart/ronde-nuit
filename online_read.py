'''Connect to an IRC server to gather messages from one of its channel.
'''
import argparse

from src.connection import OnlineTxtParser


def parse_args():
    '''Define an argument parser and returns the corresponding dictionary.

    Returns
    -------
    dict
        dictionary of input arguments
    '''
    parser = argparse.ArgumentParser(
        description='Gather data (sentences) from an online txt file.')
    parser.add_argument('url', type=str,
                        help='IRC server to connect to.')
    parser.add_argument('-f', '--file', type=str,
                        default='output.json',
                        help='path to JSON file to store sentences in.')
    opt = parser.parse_args()

    return opt


if __name__ == '__main__':
    # Load parameters
    opt = parse_args()

    parser = OnlineTxtParser(opt.url, opt.file)
    parser.get_online_file()
