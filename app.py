from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'analises.json')

def load_analyses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_analyses(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/salvar', methods=['POST'])
def salvar():
    dados = request.get_json()
    dados['id'] = datetime.now().strftime('%Y%m%d%H%M%S')
    dados['created_at'] = datetime.now().isoformat()

    analises = load_analyses()
    analises.append(dados)
    save_analyses(analises)

    return jsonify({'success': True, 'id': dados['id']})

@app.route('/api/analises', methods=['GET'])
def listar():
    return jsonify(load_analyses())

if __name__ == '__main__':
    app.run(debug=True, port=5002)
