FROM python:3.10-slim

RUN apt-get update && apt-get install -y gcc

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libomp-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./api /app/api
COPY ./src /app/src
COPY ./models_llm /app/models_llm
COPY ./db /app/db
COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
