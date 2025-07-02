from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Carrega as regras de descarte uma vez ao iniciar a aplicação
DISCARD_RULES = {}
try:
    with open('discard_rules.json', 'r', encoding='utf-8') as f:
        DISCARD_RULES = json.load(f)
    print("Regras de descarte carregadas com sucesso!")
except FileNotFoundError:
    print("Erro: 'discard_rules.json' não encontrado. As instruções não estarão disponíveis.")
except Exception as e:
    print(f"Erro ao carregar 'discard_rules.json': {e}")

@app.route('/get_discard_instructions', methods=['POST'])
def get_discard_instructions():
    data = request.get_json()
    if not data or 'material_type' not in data:
        return jsonify({"error": "Requisição inválida. Esperado JSON com 'material_type'."}), 400

    material_type = data['material_type'].lower() # Garante minúsculas

    # Tenta encontrar as instruções para o tipo de material
    instructions_data = DISCARD_RULES.get(material_type, DISCARD_RULES.get("unknown"))

    if instructions_data:
        return jsonify({
            "material_type": material_type,
            "instructions": instructions_data["instructions"],
            "tips": instructions_data["tips"]
        }), 200
    else:
        # Caso "unknown" não esteja no JSON, ou algum erro inesperado
        return jsonify({"error": "Instruções não encontradas para o tipo de material especificado."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) # Porta diferente para este serviço