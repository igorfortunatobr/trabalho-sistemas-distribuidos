FROM python:3.9-slim-buster

WORKDIR /app

# Install system dependencies required for some AI libraries (like torch)
# You might need more depending on your specific AI model's dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# If your AI model is local and large, you might want to pre-download it here
# For Hugging Face models, `pipeline` will download it on first run,
# but it's better to manage it for production deployments.
# Example:
# ENV HF_HOME=/app/models
# RUN python -c "from transformers import pipeline; pipeline('text-generation', model='gpt2')"

COPY app.py .
# No need to copy discard_rules.json anymore

EXPOSE 5001

CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]