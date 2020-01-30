import requests
from Cli.cli import Cli


def sanitize_data(data):
    for key in data.keys():
        data[key] = data[key].strip()

    data['type_de_bien'] = data['type_de_bien'].lower()
    data['ville'] = data['ville'].upper()

    return data


cli = Cli()

data = sanitize_data(cli.prompt())

r = requests.post('http://127.0.0.1:5000/', json=data)

print(r.text)
