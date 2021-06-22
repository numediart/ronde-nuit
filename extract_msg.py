'''Extract messages from WhatsApp archive.
'''
import argparse
import json

from src.whatsapp import convert_chat


def main():
    '''Main function used to parse command line arguments.
    '''
    parser = argparse.ArgumentParser(
        description='Parse WhatsApp chat and extract message into a JSON file.')
    parser.add_argument('path', type=str,
                        help='path to WhatsApp chat history file.')
    parser.add_argument('outfile', type=str,
                        help='JSON output file containing extracted messages.')
    parser.add_argument('-l', '--length', type=int, default=0,
                        help='number of messages to extract. 0 means all messages.')
    args = parser.parse_args()

    convert_chat(args.path, args.outfile, args.length)


if __name__ == '__main__':
    main()
