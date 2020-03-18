import requests
from Cli.cli import Cli
from production_ia import Model
import locale

locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')
locale._override_localeconv = {'mon_thousands_sep': ' '}


def sanitize_data(data):
    for key in data.keys():
        data[key] = data[key].strip()

    data['type_de_bien'] = data['type_de_bien'].lower()
    data['ville'] = data['ville'].upper()

    return data


cli = Cli()
model = Model()

data = sanitize_data(cli.prompt())
prediction = (model.make_prediction(data))
fr_price = locale.format_string('%.2f', prediction, grouping=True, monetary= True)



print(f'Votre bien est estimé à : {fr_price}€')