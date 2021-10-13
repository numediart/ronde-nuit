'''File used to retrain a sentiment analysis model.
'''
import argparse

from src.retrain import retrain


def main():
    '''Main function used to parse command line arguments.
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
    args = parser.parse_args()

    retrain(args.folder, args.token, args.sentiment)


if __name__ == '__main__':
    main()
