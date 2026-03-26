from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE    = os.path.join(os.path.dirname(__file__), 'data', 'analises.json')
PRODUTO_FILE = os.path.join(os.path.dirname(__file__), 'data', 'produtos.json')

def _load(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def _save(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ── Módulo 1 ──────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/salvar', methods=['POST'])
def salvar():
    dados = request.get_json()
    dados['id'] = datetime.now().strftime('%Y%m%d%H%M%S')
    dados['created_at'] = datetime.now().isoformat()
    analises = _load(DATA_FILE)
    analises.append(dados)
    _save(DATA_FILE, analises)
    return jsonify({'success': True, 'id': dados['id']})

@app.route('/api/analises', methods=['GET'])
def listar():
    return jsonify(_load(DATA_FILE))

# ── Módulo 3 ──────────────────────────────────────────────
VIAB_FILE = os.path.join(os.path.dirname(__file__), 'data', 'viabilidades.json')

@app.route('/viabilidade')
def viabilidade():
    return render_template('viabilidade.html')

@app.route('/api/viabilidade/salvar', methods=['POST'])
def salvar_viabilidade():
    dados = request.get_json()
    dados['id'] = datetime.now().strftime('%Y%m%d%H%M%S')
    dados['created_at'] = datetime.now().isoformat()
    lista = _load(VIAB_FILE)
    lista.append(dados)
    _save(VIAB_FILE, lista)
    return jsonify({'success': True, 'id': dados['id']})

@app.route('/api/viabilidade/lista', methods=['GET'])
def listar_viabilidades():
    return jsonify(_load(VIAB_FILE))

# ── Módulo 2 ──────────────────────────────────────────────
@app.route('/produto')
def produto():
    return render_template('produto.html')

@app.route('/api/produto/salvar', methods=['POST'])
def salvar_produto():
    dados = request.get_json()
    dados['id'] = datetime.now().strftime('%Y%m%d%H%M%S')
    dados['created_at'] = datetime.now().isoformat()
    produtos = _load(PRODUTO_FILE)
    produtos.append(dados)
    _save(PRODUTO_FILE, produtos)
    return jsonify({'success': True, 'id': dados['id']})

@app.route('/api/produto/lista', methods=['GET'])
def listar_produtos():
    return jsonify(_load(PRODUTO_FILE))

if __name__ == '__main__':
    app.run(debug=True, port=5002)
