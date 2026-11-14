from flask import Flask, jsonify

app = Flask(__name__)

VIFURUSHI = [
    {"id": "saa1", "jina": "Saa 1", "bei": 500},
    {"id": "siku1", "jina": "Siku 1", "bei": 1500},
    {"id": "wiki1", "jina": "Wiki 1", "bei": 7000},
]

@app.route("/")
def nyumbani():
    return "Bill-Fi yangu inafanya kazi!"

@app.route("/vifurushi")
def vifurushi():
    return jsonify(VIFURUSHI)
