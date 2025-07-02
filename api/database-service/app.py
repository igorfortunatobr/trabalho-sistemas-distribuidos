from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
import hashlib

app = Flask(__name__)
CORS(app)

# Configuração do banco
DB_PATH = "/app/data/users.db"

def get_db_connection():
    """Cria conexão com o banco de dados"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    """Cria hash da senha (simples para demo)"""
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/', methods=['GET'])
def home():
    return "Serviço de Banco de Dados - Sistema de Usuários"

@app.route('/users', methods=['GET'])
def get_users():
    """Lista todos os usuários (sem senhas)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, full_name, username, created_at FROM users")
        users = cursor.fetchall()
        
        user_list = []
        for user in users:
            user_list.append({
                'id': user['id'],
                'full_name': user['full_name'],
                'username': user['username'],
                'created_at': user['created_at']
            })
        
        conn.close()
        return jsonify({'users': user_list}), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar usuários: {str(e)}'}), 500

@app.route('/users', methods=['POST'])
def create_user():
    """Cria um novo usuário"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        full_name = data.get('full_name')
        username = data.get('username')
        password = data.get('password')
        
        if not all([full_name, username, password]):
            return jsonify({'error': 'Nome completo, usuário e senha são obrigatórios'}), 400
        
        # Verificar se usuário já existe
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Usuário já existe'}), 409
        
        # Criar hash da senha
        hashed_password = hash_password(password)
        
        # Inserir novo usuário
        cursor.execute(
            "INSERT INTO users (full_name, username, password) VALUES (?, ?, ?)",
            (full_name, username, hashed_password)
        )
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Usuário criado com sucesso',
            'user_id': user_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Erro ao criar usuário: {str(e)}'}), 500

@app.route('/users/login', methods=['POST'])
def login_user():
    """Autentica um usuário"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados de login não fornecidos'}), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Usuário e senha são obrigatórios'}), 400
        
        # Buscar usuário
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, full_name, username, password FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Verificar senha
        hashed_password = hash_password(password)
        if user['password'] != hashed_password:
            return jsonify({'error': 'Senha incorreta'}), 401
        
        return jsonify({
            'success': True,
            'message': 'Login realizado com sucesso',
            'user': {
                'id': user['id'],
                'full_name': user['full_name'],
                'username': user['username']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro no login: {str(e)}'}), 500

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Remove um usuário"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar se usuário existe
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Remover usuário
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Usuário removido com sucesso'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao remover usuário: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True) 