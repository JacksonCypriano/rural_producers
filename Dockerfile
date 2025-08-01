FROM python:3.11-slim

RUN apt-get update && apt-get install -y build-essential libpq-dev postgresql-client

WORKDIR /app

COPY . .

RUN pip install poetry

ENV POETRY_VIRTUALENVS_CREATE=false

RUN poetry install --no-root

COPY wait-for-it.sh /wait-for-it.sh

RUN chmod +x wait-for-it.sh

RUN chmod +x /wait-for-it.sh

EXPOSE 8000

CMD ["/wait-for-it.sh", "db", "python", "manage.py", "runserver", "0.0.0.0:8000"]
