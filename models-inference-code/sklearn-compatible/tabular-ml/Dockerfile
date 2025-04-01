FROM python:3.13-slim

# Install dependencies
COPY requirements-loading.txt requirements-loading.txt
COPY requirements-webserver.txt requirements-webserver.txt
COPY sklearn-compatible/tabular-ml/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements-loading.txt -r requirements-webserver.txt -r requirements.txt

COPY sklearn-compatible/tabular-ml /app
ENV MODEL_PATH=/app/model.joblib

EXPOSE 8000

ENTRYPOINT [ "python",  "/app/main.py"]
