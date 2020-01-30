from flask import Flask, jsonify, request


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
    return data


if __name__ == "__main__":
    app.run()
