'''Parse and format WhatsApp chat history into a JSON file.
'''
from typing import Dict, List

import argparse
import json
import os


def read_chat(path: str,
              length: int = 0) -> List[Dict[str, str]]:
    '''Parse WhatsApp chat history.

    Args
    ----
    path : str
        path to WhatsApp chat history file
    length : optional, int
        number of messages to extract. If 0, extract all messages.
        Default is 0

    Returns
    -------
    list of dictionary
        list of messages structured as dictionary.
        See parse_line function for further information on dictionary structure.
    '''
    result = []
    with open(path, 'r', encoding='utf8') as f:
        line = f.readline()
        data: Dict[str, str] = {}

        while line and length:
            # New message line
            if line[0] == '[':

                data_line = parse_line(line)
                if not data:
                    data = data_line
                else:
                    if data['user'] == data_line['user']:
                        data['message'] += data_line['message']
                    else:
                        result.append(data)
                        data = data_line

            # Continuation line
            else:
                data['message'] += line

            line = f.readline()
            length -= 1

        if data:
            result.append(data)

    return result


def parse_line(line: str) -> Dict[str, str]:
    '''Parse a WhatsApp history chat line.

    Line structure is:
        [DD/MM/YYYY HH:MM:SS AP] <name>: <message>

    Args
    ----
    line : str
        line to parse

    Returns
    -------
    dictionary
        message structured as dictionary such as:
            'user' is the name of message sender
            'message' is the sent message
            'date' is day the message was sent
            'time' is the time the message was sent
    '''
    data = {}
    value = line.split(']')

    data['date'] = value[0][1:11]
    data['time'] = value[0][12:]

    if len(value) > 1:
        valvalue = value[1][1:].split(':')
        if len(valvalue) > 1:
            data['user'] = valvalue[0]
            data['message'] = valvalue[1][1:]
        else:
            data['user'] = ''
            data['message'] = valvalue[0]

    return data


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

    data = read_chat(args.path, args.length)

    with open(args.outfile, 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    length = 5000
    path = os.path.join('data', 'whatsapp_famille.txt')
    outfile = os.path.join('data', 'chat_5000.json')

    main()
