'''Converts JSON to CSV file.
'''
import argparse

from src.utils import json2csv


def main():
    '''Main function used to parse command line arguments.
    '''
    parser = argparse.ArgumentParser(
        description='Converts a JSON file into a CSV file.')
    parser.add_argument('path', type=str,
                        help='path to JSON file.')
    parser.add_argument('-c', '--csv', type=str, default='output.csv',
                        help='CSV output file to have conversion.')
    parser.add_argument('-m', '--models', type=str,
                        default=['default', 'camembert'], nargs='+',
                        help='list of models result present in the JSON file.')
    args = parser.parse_args()

    json2csv(args.path, args.csv, args.models)


if __name__ == '__main__':
    main()
