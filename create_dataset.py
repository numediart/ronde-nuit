import json


def create_dummy_db(outputfile: str = 'data/dataset.json'):
    with open('data/chaat.json', 'r') as f:
        data = json.load(f)

    res = [{'text': elem['message'], 'label': elem['camembert']['label']}
           for elem in data]

    with open(outputfile, 'w') as f:
        json.dump(res, f, indent=4)
