
FROM python:3-slim


WORKDIR /app
COPY requirements.txt /app/

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=AmlABFlow_api.settings

CMD ["gunicorn", "--bind", "127.0.0.1:8000", "AmlABFlow_api.wsgi:application"]