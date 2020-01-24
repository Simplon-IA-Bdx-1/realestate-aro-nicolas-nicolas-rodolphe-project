from flask import Flask, jsonify, request
from Cli.cli import Cli


data = {'type': '   MaIsoN', 'rooms': '    4',
         'surface': '120', 'ville': 'bordeaux'}


def sanitize_data(data):
    for key in data.keys():
        data[key] = data[key].strip()

    data['type'] = data['type'].lower()
    data['ville'] = data['ville'].upper()

    return data


cli = Cli()

app = Flask(__name__)


@app.route('/')
def index():
    data = sanitize_data(cli.prompt())
    return f'data to predict on: {data}'


if __name__ == "__main__":
    app.run()
