FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY discard_rules.json .

EXPOSE 5001

CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]