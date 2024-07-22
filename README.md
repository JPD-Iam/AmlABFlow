# AmlABFlow
1. Project Overview

Description: A web application that integrates Django for the backend, MLflow for model management, and Docker for containerization.
Technologies Used: Django, MLflow, Docker.
Purpose: To manage and serve machine learning models, providing APIs for model registration and predictions.
2. Docker Setup

Dockerfile for Django:

```
# Dockerfile for Django
FROM python:3-slim

WORKDIR /app
COPY . /app/

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=AmlABFlow_api.settings

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "AmlABFlow_api.wsgi:application"]
```

3. Running the Application

Build and Start Containers:
```
docker-compose build
docker-compose up

```
Stopping Containers:
```
docker-compose down
```

Accessing Services
Django: http://localhost:8000
MLflow: http://localhost:5000
Prometheus: http://localhost:9090
Grafana: http://localhost:3000

4. Endpoints

Django Endpoints
/api/register_model/ - Register a new model
/api/predict/ - Make predictions with a model


5. Troubleshooting

Common Issues
Connection Issues: Ensure all services are running and check Docker logs for errors.
Bad Request Error: Verify the API request format and required fields.
Internal Server Error: Check Django and MLflow logs for detailed error messages.

Future Enhancements
Plan to add more plugins or features.
