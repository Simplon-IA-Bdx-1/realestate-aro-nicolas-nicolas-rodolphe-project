from PyInquirer import prompt


class Cli:
    def prompt(self):
        questions = [
            {
                'type': 'list',
                'name': 'type',
                'message': 'Quel est le type de bien sur \
                            lequel lancer une prédiction?',
                'choices': [
                    'maison',
                    'appartement'
                ]
            },
            {
                'type': 'input',
                'name': 'rooms',
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
