'''Parse and format WhatsApp chat history into a JSON file.
'''
import csv
import json
import re
from typing import Dict, List

import ftfy


# -------- #
# WhatsApp #
# -------- #
def parse_whatsapp_line(line: str) -> Dict[str, str]:
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


def read_whatsapp_chat(path: str,
                       length: int = -1) -> List[Dict[str, str]]:
    '''Parse WhatsApp chat history.

    Args
    ----
    path : str
        path to WhatsApp chat history file
    length : optional, int
        number of messages to extract. If -1, extract all messages.
        Default is -1.

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

                data_line = parse_whatsapp_line(line)
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


def convert_whatsapp_chat(srcfile: str,
                          outfile: str,
                          length: int = -1) -> None:
    '''Converts txt archive file to JSON file.

    Args
    ----
    srcfile : str
        path to WhatsApp chat history file
    outfile : str
        JSON file to extract messages to
    length : optional, int
        number of messages to extract. If -1, extract all messages.
        Default is -1.
    '''
    data = read_whatsapp_chat(srcfile, length)

    with open(outfile, 'w') as f:
        json.dump(data, f, indent=4)


# --------- #
# Text file #
# --------- #
def read_txt_file(path: str,
                  length: int = -1) -> List[Dict[str, str]]:
    '''Parse txt file.

    Args
    ----
    path : str
        path to txt file
    length : optional, int
        number of messages to extract. If -1, extract all messages.
        Default is -1.

    Returns
    -------
    list of dictionary
        list of messages structured as dictionary.
    '''
    result = []
    msgs = []
    with open(path, 'r', encoding='utf8') as f:
        line = f.readline()

        while line and length:
            if line and line not in msgs:
                result.append({'message': line})
                msgs.append(line)
                length -= 1

            line = f.readline()

    return result


def convert_txt_file(scrfile: str,
                     outfile: str,
                     length: int = -1) -> None:
    '''Convert txt file to JSON file.

    Each line of the txt line is a new sentence.

    Args
    ----
    srcfile : str
        path to txt file
    outfile : str
        JSON file to extract sentences to
    length : optional, int
        number of messages to extract. If -1, extract all messages.
        Default is -1.
    '''
    data = read_txt_file(scrfile, length)

    with open(outfile, 'w') as f:
        json.dump(data, f, indent=4)


def remove_irc_formatting(msg: str) -> str:
    '''Removes the tags for IRC formatting characters.

    Based on https://gist.github.com/ion1/2791653
    '''
    regex = re.compile(
        "\x1f|\x02|\x12|\x0f|\x16|\x03(?:\d{1,2}(?:,\d{1,2})?)?", re.UNICODE)
    msg = regex.sub("", msg)
    msg.replace('\\\\', '\\')
    return msg


def json2csv(jsonfile: str,
             csvfile: str,
             threshold: int = 3) -> None:
    '''Converts JSON file to CSV file.

    It is assumed that JSON file list dictionary keys are:
        * message: the message analyzed
        * <name>: the name of a model
            * label: the label of the message
            * score: the confidence score

    Args
    ----
    jsonfile : str
        input JSON file

    csvfile : str
        output CSV file

    threshold : optional, int
        minimum (exclusive) length of a message (in number of characters).
        Default is 3.
    '''
    with open(jsonfile, encoding='utf-8') as f:
        jsondata = json.load(f)

    header = ['channel', 'message']
    names = list(jsondata[0].keys())
    for x in header:
        if x in names:
            names.remove(x)

    for name in names:
        header.append('{} label'.format(name))
        header.append('{} score'.format(name))

    with open(csvfile, 'w', encoding='utf-8', newline='') as f:
        csvwriter = csv.writer(f, delimiter=',')
        csvwriter.writerow(header)

    for elem in jsondata:
        msg = remove_irc_formatting(elem['message'])
        msg = ftfy.ftfy(msg)
        if len(msg) > threshold:
            # data = [elem['channel'], msg]
            data = [msg]

            for name in names:
                data.append(elem[name]['label'])
                data.append(elem[name]['score'])

            with open(csvfile, 'a', encoding="utf-8", newline='') as f:
                csvwriter = csv.writer(f, delimiter=',')
                csvwriter.writerow(data)
