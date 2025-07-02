-- Schema para tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserir alguns usuários de exemplo (opcional)
INSERT OR IGNORE INTO users (full_name, username, password) VALUES 
    ('Administrador', 'admin', '123456'),
    ('Usuário Teste', 'teste', 'teste123'); 