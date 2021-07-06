'''Utility functions for diverse features.
'''
from typing import List

import csv
import json


def csv2json(csvfile: str,
             jsonfile: str):
    '''
    '''
    data = []
    keys: List[str] = []

    with open(csvfile, 'r', encoding="utf-8") as f:
        csv_reader = csv.reader(f, delimiter=',')
        for row in csv_reader:
            if len(keys) == 0:
                keys = [key for key in row]
            else:
                curdata = {}
                for key, value in zip(keys, row):
                    curdata[key] = value
                data.append(curdata)

    with open(jsonfile, 'w') as f:
        json.dump(data, f)


def json2csv(jsonfile: str,
             csvfile: str,
             names: List[str]):
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
    names : list of str
        list of model results in the JSON
    '''
    with open(jsonfile) as f:
        jsondata = json.load(f)

    header = ['message']
    for name in names:
        header.append('{} label'.format(name))
        header.append('{} score'.format(name))

    with open(csvfile, 'w', newline='') as f:
        csvwriter = csv.writer(f, delimiter=',')
        csvwriter.writerow(header)

    for elem in jsondata:
        data = [elem['message']]
        for name in names:
            data.append(elem[name]['label'])
            data.append(elem[name]['score'])
        with open(csvfile, 'a', encoding="utf-8", newline='') as f:

            csvwriter = csv.writer(f, delimiter=',')
            csvwriter.writerow(data)
