from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/ola')
def ola_mundo():
    return jsonify({
        "ola": "mundo"
    })
