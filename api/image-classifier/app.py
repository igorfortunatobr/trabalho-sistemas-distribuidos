import torch
from PIL import Image
from transformers import AutoModelForImageClassification, AutoImageProcessor
from flask import Flask, request, jsonify
import io

app = Flask(__name__)

# --- Carregando o Modelo e Processador (feito uma vez ao iniciar a aplicação) ---
# O modelo será carregado na memória do container Docker
print("Carregando modelo e processador do Hugging Face...")
model_name = "tribber93/my-trash-classification"
model = AutoModelForImageClassification.from_pretrained(model_name)
processor = AutoImageProcessor.from_pretrained(model_name)
print("Modelo e processador carregados com sucesso!")

# --- Endpoint da API para Classificação ---
@app.route('/classify', methods=['POST'])
def classify_image():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo 'file' na requisição."}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado."}), 400
    
    if file:
        try:
            # Ler a imagem do fluxo de bytes
            image_bytes = file.read()
            image = Image.open(io.BytesIO(image_bytes))
            
            # Processar a imagem e fazer a inferência
            inputs = processor(image, return_tensors="pt")
            outputs = model(**inputs)
            predictions = torch.argmax(outputs.logits, dim=-1)
            
            # Obter o nome da classe predita
            predicted_class = model.config.id2label[predictions.item()]
            
            return jsonify({"predicted_class": predicted_class}), 200
        except Exception as e:
            return jsonify({"error": f"Erro ao processar a imagem ou fazer inferência: {str(e)}"}), 500
    
    return jsonify({"error": "Ocorreu um erro desconhecido."}), 500

# --- Rodar o Servidor Flask ---
if __name__ == '__main__':
    # '0.0.0.0' torna o servidor acessível de fora do container
    app.run(host='0.0.0.0', port=5000)
