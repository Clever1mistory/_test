FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq-dev

RUN pip install -r requirements.txt

COPY . .

WORKDIR /app/bookmark_service

CMD python manage.py makemigrations && python manage.py migrate && gunicorn --bind 0.0.0.0:8000 bookmark_service.wsgi:application
