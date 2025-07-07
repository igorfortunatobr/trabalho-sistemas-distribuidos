from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import io
import jwt
import os
from functools import wraps

app = Flask(__name__)
CORS(app)

# --- Configuração para garantir UTF-8 e evitar escapadas Unicode ---
app.config['JSON_AS_ASCII'] = False
app.config['JSON_MIMETYPE'] = 'application/json; charset=utf-8'
# --- Fim da Configuração ---

# Configuração JWT
app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'CHAVE_SECRETA123')
app.config['JWT_ALGORITHM'] = 'HS256'

IMAGE_CLASSIFIER_URL = "http://image-classifier:5000/classify"
TEXT_GENERATOR_URL = "http://text-generator:5001/get_discard_instructions"
DATABASE_SERVICE_URL = "http://database-service:5002"

def verify_token(token):
    """Verifica se um token JWT é válido"""
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=[app.config['JWT_ALGORITHM']])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator para proteger rotas que requerem autenticação"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Verificar se o token está no header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Token invalido'}), 401
        
        if not token:
            return jsonify({'error': 'Token nao fornecido'}), 401
        
        # Verificar se o token é válido
        payload = verify_token(token)
        if not payload:
            return jsonify({'error': 'Token invalido ou expirado'}), 401
        
        # Adicionar dados do usuário à requisição
        request.user = payload
        return f(*args, **kwargs)
    
    return decorated

@app.route('/', methods=['GET'])
def home():
    return "Sistema de Classificação e Descarte de Residuos - API em funcionamento!"

def generate_token(user_data):
    """Gera um token JWT para o usuário"""
    import datetime
    payload = {
        'user_id': user_data['id'],
        'username': user_data['username'],
        'full_name': user_data['full_name'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm=app.config['JWT_ALGORITHM'])

@app.route('/login', methods=['POST'])
def login():
    """Endpoint de login que gera token JWT"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados de login não fornecidos"}), 400
        
        username = data.get('username') or data.get('user')
        password = data.get('password') or data.get('pass')
        
        if not username or not password:
            return jsonify({"error": "Usuário e senha são obrigatórios"}), 400
        
        # Verificar credenciais no serviço de banco de dados
        login_data = {
            "username": username,
            "password": password
        }
        
        response = requests.post(f"{DATABASE_SERVICE_URL}/users/login", json=login_data)
        
        if response.status_code == 200:
            db_response = response.json()
            user_data = db_response.get("user", {})
            
            # Gerar token JWT
            token = generate_token(user_data)
            
            return jsonify({
                "success": True,
                "message": "Login realizado com sucesso",
                "token": token,
                "user": user_data,
                "expires_in": 24 * 3600  # segundos
            }), 200
        else:
            db_response = response.json()
            return jsonify({
                "success": False,
                "error": db_response.get("error", "Erro no login")
            }), response.status_code
            
    except requests.exceptions.ConnectionError:
        return jsonify({
            "success": False,
            "error": "Serviço de banco de dados indisponível"
        }), 503
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro interno do servidor: {str(e)}"
        }), 500

@app.route('/register', methods=['POST'])
def register():
    """Endpoint de registro - apenas cria o usuário, sem gerar token"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados de cadastro não fornecidos"}), 400
        
        full_name = data.get('full_name')
        username = data.get('username')
        password = data.get('password')
        
        if not all([full_name, username, password]):
            return jsonify({"error": "Nome completo, usuário e senha são obrigatórios"}), 400
        
        # Criar usuário no serviço de banco de dados
        register_data = {
            "full_name": full_name,
            "username": username,
            "password": password
        }
        
        response = requests.post(f"{DATABASE_SERVICE_URL}/users", json=register_data)
        
        if response.status_code == 201:
            db_response = response.json()
            return jsonify({
                "success": True,
                "message": "Usuário cadastrado com sucesso. Faça login para acessar o sistema.",
                "user_id": db_response.get("user_id")
            }), 201
        else:
            db_response = response.json()
            return jsonify({
                "success": False,
                "error": db_response.get("error", "Erro no cadastro")
            }), response.status_code
            
    except requests.exceptions.ConnectionError:
        return jsonify({
            "success": False,
            "error": "Serviço de banco de dados indisponível"
        }), 503
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro interno do servidor: {str(e)}"
        }), 500

@app.route('/process_trash_image', methods=['POST'])
@token_required
def process_trash_image():
    """Endpoint protegido que requer autenticação JWT"""
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

            # Adicionar informações do usuário autenticado à resposta
            final_response = {
                "image_classification": material_type,
                "discard_instructions": text_generator_result.get("instructions", "Não foi possível obter instruções de descarte."),
                "discard_tips": text_generator_result.get("tips", ""),
                "user": {
                    "user_id": request.user['user_id'],
                    "username": request.user['username'],
                    "full_name": request.user['full_name']
                }
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

@app.route('/me', methods=['GET'])
@token_required
def get_current_user():
    """Endpoint para obter informações do usuário atual"""
    try:
        return jsonify({
            "success": True,
            "user": {
                "user_id": request.user['user_id'],
                "username": request.user['username'],
                "full_name": request.user['full_name']
            }
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro ao obter dados do usuário: {str(e)}"
        }), 500

@app.route('/verify-token', methods=['POST'])
def verify_token_endpoint():
    """Endpoint para verificar se um token é válido"""
    try:
        data = request.get_json()
        
        if not data or 'token' not in data:
            return jsonify({"error": "Token não fornecido"}), 400
        
        token = data['token']
        payload = verify_token(token)
        
        if payload:
            return jsonify({
                "valid": True,
                "user": {
                    "user_id": payload['user_id'],
                    "username": payload['username'],
                    "full_name": payload['full_name']
                }
            }), 200
        else:
            return jsonify({
                "valid": False,
                "error": "Token inválido ou expirado"
            }), 401
            
    except Exception as e:
        return jsonify({
            "valid": False,
            "error": f"Erro ao verificar token: {str(e)}"
        }), 500

@app.route('/refresh-token', methods=['POST'])
@token_required
def refresh_token():
    """Endpoint para renovar um token JWT"""
    try:
        # O decorator token_required já validou o token e adicionou request.user
        user_data = {
            'id': request.user['user_id'],
            'username': request.user['username'],
            'full_name': request.user['full_name']
        }
        
        # Gerar novo token
        import datetime
        payload = {
            'user_id': user_data['id'],
            'username': user_data['username'],
            'full_name': user_data['full_name'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            'iat': datetime.datetime.utcnow()
        }
        new_token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm=app.config['JWT_ALGORITHM'])
        
        return jsonify({
            "success": True,
            "token": new_token,
            "user": user_data,
            "expires_in": 24 * 3600
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro ao renovar token: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)