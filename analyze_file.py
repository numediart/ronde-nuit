'''File used to test analysis sentiment in files.
'''
import argparse

from src.analysis import run_model


def main():
    '''Main function used to parse command line arguments.
    '''
    parser = argparse.ArgumentParser(
        description='Run sentiment analysis using transformers library.')
    parser.add_argument('srcfile', type=str,
                        help='input file to be analyzed.')
    parser.add_argument('-v', '--version', type=int, default=0,
                        help='version of analyzer. 0 is CamemBERT, 1 is transformers\' default.')
    parser.add_argument('-t', '--threshold', type=float, default=0.6666,
                        help='threshold for neutral label. Any score below the threshold (positive or negative) is considered neutral.')
    args = parser.parse_args()

    run_model(args.srcfile, args.version, args.threshold)


if __name__ == '__main__':
    main()
