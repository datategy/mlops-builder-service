FROM python:3.13-slim

# Install dependencies
COPY requirements-loading.txt requirements-loading.txt
COPY requirements-webserver.txt requirements-webserver.txt
COPY papai/regression-classification-clustering/requirements.txt requirements.txt

# For numpy 1.26 (it does not seem to be required for numpy 2.x)
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y g++

RUN pip install --no-cache-dir -r requirements-loading.txt -r requirements-webserver.txt -r requirements.txt

COPY papai/regression-classification-clustering /app
ENV MODEL_PATH=/app/model_info.joblib

EXPOSE 8000

ENTRYPOINT [ "python",  "/app/main.py"]
