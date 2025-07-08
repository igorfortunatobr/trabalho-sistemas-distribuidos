from flask import Flask, request, jsonify
import json
from transformers import pipeline

app = Flask(__name__)

try:
    ai_agent = pipeline("text-generation", model="gpt2", max_new_tokens=100) # GPT2
    print("AI agent loaded successfully!")
except Exception as e:
    print(f"Erro ao carregar o agente de IA: {e}")
    ai_agent = None # Set to None if loading fails

@app.route('/get_discard_instructions', methods=['POST'])
def get_discard_instructions():
    data = request.get_json()
    if not data or 'material_type' not in data:
        return jsonify({"error": "Requisição inválida. Esperado JSON com 'material_type'."}), 400

    material_type = data['material_type'].lower() # Garante minúsculas

    if ai_agent is None:
        return jsonify({"error": "Agente de IA não está disponível."}), 500

    try:
        prompt = f"For a '{material_type}' material, provide detailed discard instructions and some helpful tips for proper disposal. Format your response as follows:\nInstructions: [instructions here]\nTips: [tips here]"

        generated_text = ai_agent(prompt)[0]['generated_text']
        
        instructions_start = generated_text.find("Instructions:")
        tips_start = generated_text.find("Tips:")

        instructions = "Instruções não encontradas."
        tips = "Dicas não encontradas."

        if instructions_start != -1 and tips_start != -1:
            instructions = generated_text[instructions_start + len("Instructions:"):tips_start].strip()
            tips = generated_text[tips_start + len("Tips:"):].strip()
        elif instructions_start != -1:
            instructions = generated_text[instructions_start + len("Instructions:"):].strip()
        elif tips_start != -1:
            tips = generated_text[tips_start + len("Tips:"):].strip()
        else:
            instructions = generated_text
            tips = "Consulte a geração da IA para obter dicas."

        instructions = instructions.replace(prompt, "").strip()
        tips = tips.replace(prompt, "").strip()

        return jsonify({
            "material_type": material_type,
            "instructions": instructions,
            "tips": tips
        }), 200

    except Exception as e:
        print(f"Erro ao gerar instruções com IA: {e}")
        return jsonify({"error": f"Erro interno ao processar a requisição com IA: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) # Porta diferente para este serviço