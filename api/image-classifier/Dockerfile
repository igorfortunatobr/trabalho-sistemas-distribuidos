# Use uma imagem base do Python
FROM python:3.9-slim-buster

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o arquivo da aplicação Flask
COPY app.py .

# Expõe a porta que a aplicação Flask vai usar (padrão é 5000)
EXPOSE 5000

# Comando para rodar a aplicação quando o container iniciar
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
