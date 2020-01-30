from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route('/')
def index():
    user_agent = request.headers['user-agent']
    if 'python' in user_agent:
        return jsonify({'message': 'hello python'})
    if 'Mozilla' in user_agent:
        return jsonify({'message': 'Yo web, what\'s up?'})

if __name__ == "__main__":
    app.run()
