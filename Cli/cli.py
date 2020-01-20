from PyInquirer import prompt


class Cli:
    def prompt(self):
        questions = [
            {
                'type': 'list',
                'name': 'type',
                'message': 'Quel est le type de bien sur lequel lancer une prédiction?',
                'choices': [
                    'maison',
                    'appartement'
                ]
            },
            {
                'type': 'input',
                'name': 'surface',
                'message': 'Quelle est sa surface en m²?'
            },
            {
                'type': 'input',
                'name': 'year-build',
                'message': 'Quelle est l\'anée de construction?'
            },
            {
                'type': 'input',
                'name': 'rooms',
                'message': 'Quel est le nombre de chambres?'
            },
            {
                'type': 'list',
                'name': 'basement',
                'message': 'Y a-t-il une cave?',
                'choices': [
                    'oui',
                    'non'
                ]
            },
            {
                'type': 'input',
                'name': 'parking',
                'message': 'Combien de places de parking sont disponibles?'
            },
        ]

        return prompt(questions)


cli = Cli()
print(cli.prompt())

