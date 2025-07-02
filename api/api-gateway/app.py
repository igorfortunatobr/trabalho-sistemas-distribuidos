from flask import Flask, request, jsonify
import requests
import io

app = Flask(__name__)

# --- Configuração para garantir UTF-8 e evitar escapadas Unicode ---
app.config['JSON_AS_ASCII'] = False
app.config['JSON_MIMETYPE'] = 'application/json; charset=utf-8'
# --- Fim da Configuração ---

IMAGE_CLASSIFIER_URL = "http://image-classifier:5000/classify"
TEXT_GENERATOR_URL = "http://text-generator:5001/get_discard_instructions"

@app.route('/process_trash_image', methods=['POST'])
def process_trash_image():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo 'file' na requisição."}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado."}), 400
    
    if file:
        try:
            files = {'file': (file.filename, file.read(), file.content_type)}
            
            classifier_response = requests.post(IMAGE_CLASSIFIER_URL, files=files)
            classifier_response.raise_for_status()
            classifier_result = classifier_response.json()

            if "predicted_class" not in classifier_result:
                return jsonify({"error": "Resposta inesperada do classificador de imagens."}), 500

            material_type = classifier_result["predicted_class"]
            
            text_generator_payload = {"material_type": material_type}
            
            text_generator_response = requests.post(TEXT_GENERATOR_URL, json=text_generator_payload)
            text_generator_response.raise_for_status()
            text_generator_result = text_generator_response.json()

            # Sua linha de código permanece a mesma aqui
            final_response = {
                "image_classification": material_type,
                "discard_instructions": text_generator_result.get("instructions", "Não foi possível obter instruções de descarte."),
                "discard_tips": text_generator_result.get("tips", "")
            }
            
            # O jsonify agora usará as configurações que definimos para UTF-8
            return jsonify(final_response), 200
            
        except requests.exceptions.ConnectionError as e:
            return jsonify({"error": f"Erro de conexão com um dos serviços internos: {e}"}), 503
        except requests.exceptions.HTTPError as e:
            return jsonify({"error": f"Erro HTTP ao chamar serviço interno: {e}. Resposta: {e.response.text}"}), e.response.status_code
        except Exception as e:
            return jsonify({"error": f"Erro inesperado no processamento: {str(e)}"}), 500
    
    return jsonify({"error": "Ocorreu um erro desconhecido."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)