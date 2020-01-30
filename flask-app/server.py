from flask import Flask, jsonify, request
from production_ia import Model


app = Flask(__name__)


@app.route('/')
def index():
    user_agent = request.headers['user-agent']
    if 'python' in user_agent:
        return jsonify({'message': 'hello python'})
    else:
        return jsonify({'message': 'Yo web, what\'s up?'})


@app.route('/', methods=['POST'])
def post_route():
    data = request.get_json(force=True)
    model = Model()
    prediction = model.make_prediction(data)
    return jsonify({"prediction": prediction[0]})


if __name__ == "__main__":
    app.run()
