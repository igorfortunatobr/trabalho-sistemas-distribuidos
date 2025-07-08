from flask import Flask, request, jsonify
import json
from transformers import pipeline, set_seed
from googletrans import Translator

app = Flask(__name__)

set_seed(42)

translator = Translator()

try:
    ai_agent = pipeline("text-generation", model="gpt2", max_new_tokens=200)
    print("Agente de IA carregado com sucesso!")
except Exception as e:
    print(f"Erro ao carregar o agente de IA: {e}")
    ai_agent = None

@app.route('/get_discard_instructions', methods=['POST'])
def get_discard_instructions():
    data = request.get_json()
    if not data or 'material_type' not in data:
        return jsonify({"error": "Requisição inválida. Esperado JSON com 'material_type'."}), 400

    material_type = data['material_type'].lower()

    if ai_agent is None:
        return jsonify({"error": "Agente de IA não está disponível."}), 500

    try:
        prompt = f"For a '{material_type}' material, provide detailed discard instructions and some helpful tips for proper disposal. Format your response as follows:\nInstructions: [instructions here]\nTips: [tips here]"

        result = ai_agent(prompt)
        generated_text_english = result[0]['generated_text']

        if generated_text_english.startswith(prompt):
            generated_text_english = generated_text_english[len(prompt):].strip()

        translated_text_portuguese = translator.translate(generated_text_english, dest='pt').text
        print(f"Texto original (EN):\n{generated_text_english}")
        print(f"Texto traduzido (PT):\n{translated_text_portuguese}")


        instructions = "Não foi possível encontrar instruções de descarte claras."
        tips = "Não foi possível encontrar dicas úteis claras."

        instructions_tag = "Instruções:" 
        tips_tag = "Dicas:" 
        translated_instructions_tag_pt = "Instruções:"
        translated_tips_tag_pt = "Dicas:"


        idx_instructions = translated_text_portuguese.find(translated_instructions_tag_pt)
        idx_tips = translated_text_portuguese.find(translated_tips_tag_pt)

        if idx_instructions != -1:
            if idx_tips != -1 and idx_tips > idx_instructions:
                instructions = translated_text_portuguese[idx_instructions + len(translated_instructions_tag_pt):idx_tips].strip()
                tips = translated_text_portuguese[idx_tips + len(translated_tips_tag_pt):].strip()
            else:
                instructions = translated_text_portuguese[idx_instructions + len(translated_instructions_tag_pt):].strip()
        elif idx_tips != -1:
            tips = translated_text_portuguese[idx_tips + len(translated_tips_tag_pt):].strip()
        
        if instructions == "Não foi possível encontrar instruções de descarte claras." and \
           tips == "Não foi possível encontrar dicas úteis claras.":
            instructions = translated_text_portuguese # Retorna o texto inteiro nas instruções
            tips = "A IA gerou um texto que foi traduzido, mas não consegui separar instruções e dicas."


        return jsonify({
            "material_type": material_type,
            "instructions": instructions,
            "tips": tips
        }), 200

    except Exception as e:
        print(f"Erro ao gerar ou traduzir instruções: {e}")
        return jsonify({"error": f"Erro interno ao processar a requisição: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) # Porta diferente para este serviço