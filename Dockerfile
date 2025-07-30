FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r --no-cache-dir requirements.txt

COPY src/* /app

ENTRYPOINT ["python3", "/app/metrics.py"]