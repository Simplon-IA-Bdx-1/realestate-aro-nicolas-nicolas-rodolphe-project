from PyInquirer import prompt


class Cli:
    def prompt(self):
        questions = [
            {
                'type': 'list',
                'name': 'type_de_bien',
                'message': 'Quel est le type de bien sur \
                            lequel lancer une prédiction?',
                'choices': [
                    'maison',
                    'appartement'
                ]
            },
            {
                'type': 'input',
                'name': 'nb_de_pieces',
                'message': 'Quel est le nombre de pièces?'
            },
            {
                'type': 'input',
                'name': 'surface',
                'message': 'Quelle est sa surface en m²?'
            },
            {
                'type': 'input',
                'name': 'ville',
                'message': 'Dans quelle ville?'
            },
        ]

        return prompt(questions)
