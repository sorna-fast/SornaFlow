FROM python:3.12-slim-bullseye


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    libjpeg-dev \
    zlib1g-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


RUN mkdir -p /app/SornaFlow/media

WORKDIR /app/SornaFlow

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]