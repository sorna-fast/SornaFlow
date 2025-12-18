FROM python:3.12-bullseye

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libmariadb-dev \
    mariadb-client \
    libjpeg-dev \
    zlib1g-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

WORKDIR /app/SornaFlow

RUN mkdir -p /app/SornaFlow/media

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
