'''Converts JSON to CSV file.
'''
import argparse

from src.format import json2csv


def main():
    '''Main function used to parse command line arguments.
    '''
    parser = argparse.ArgumentParser(
        description='Converts a JSON file into a CSV file.')
    parser.add_argument('path', type=str,
                        help='path to JSON file.')
    parser.add_argument('-c', '--csv', type=str, default='output.csv',
                        help='CSV output file to have conversion.')
    args = parser.parse_args()

    json2csv(args.path, args.csv)


if __name__ == '__main__':
    main()
