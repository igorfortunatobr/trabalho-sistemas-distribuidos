#!/usr/bin/env python3
"""
Script para inicializar o banco de dados SQLite
"""

import sqlite3
import os
import time

def init_database():
    """Inicializa o banco de dados"""
    
    # Caminho para o arquivo do banco
    db_path = "/app/data/users.db"
    
    # Garantir que o diretório existe
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Conectar ao banco (cria se não existir)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Ler e executar o schema
        with open('/app/schema.sql', 'r') as f:
            schema = f.read()
        
        # Executar o schema
        cursor.executescript(schema)
        
        # Commit das mudanças
        conn.commit()
        
        print("✅ Banco de dados inicializado com sucesso!")
        print(f"📁 Localização: {db_path}")
        
        # Verificar usuários criados
        cursor.execute("SELECT username, full_name FROM users")
        users = cursor.fetchall()
        
        print(f"👥 Usuários cadastrados: {len(users)}")
        for username, full_name in users:
            print(f"   - {username} ({full_name})")
            
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🚀 Iniciando banco de dados...")
    init_database()
    
    # Manter o container rodando
    print("🔄 Container de banco de dados ativo...")
    while True:
        time.sleep(3600)  # Dormir por 1 hora 