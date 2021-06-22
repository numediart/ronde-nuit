import csv
import json
import os


def csv2json(csvfile, jsonfile):
    data = []
    keys = []

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


def json2csv(jsonfile, csvfile):
    with open(jsonfile) as f:
        data = json.load(f)

    keys = []
    for elem in data:
        if len(keys) == 0:
            keys = [key for key in elem]

            with open(csvfile, 'w', newline='') as f:
                csvwriter = csv.writer(f, delimiter=',')
                csvwriter.writerow(keys)
        data = [elem[key] for key in keys]
        with open(csvfile, 'a', encoding="utf-8", newline='') as f:
            csvwriter = csv.writer(f, delimiter=',')
            csvwriter.writerow(data)


jsonfile = 'test.json'
csvfile = 'results/chaat_accueil.csv'
csv2json(csvfile, jsonfile)
