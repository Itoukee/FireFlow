FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    build-essential \
    libchm-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

COPY . .


ENTRYPOINT ["./entrypoint.sh"]
