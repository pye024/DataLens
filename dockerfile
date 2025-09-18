FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libfreetype6 \
    libpng16-16 \
    libopenblas0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501 


CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

