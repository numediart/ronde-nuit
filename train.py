'''File used to test analysis sentiment in files.
'''
import argparse

from src.retrain import retrain


def main():
    '''Main function used to parse command line arguments.
    '''
    parser = argparse.ArgumentParser(
        description='Retrain a model.')
    parser.add_argument('-f', '--folder', type=str,
                        default='data/sorted/',
                        help='path to folder containing data.')
    parser.add_argument('-m', '--model', type=str,
                        default='distilbert-base-uncased',
                        help='base model to retrain from.')
    args = parser.parse_args()

    retrain(args.model, args.folder)


if __name__ == '__main__':
    main()
