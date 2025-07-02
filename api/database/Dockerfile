FROM python:3.9-slim-buster

WORKDIR /app

# Instalar SQLite (já vem com Python, mas garantindo)
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

# Copiar script de inicialização do banco
COPY init_db.py .
COPY schema.sql .

# Criar diretório para o banco
RUN mkdir -p /app/data

# Expor porta (opcional, para debug)
EXPOSE 5002

# Comando para inicializar o banco
CMD ["python", "init_db.py"] 