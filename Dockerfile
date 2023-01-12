FROM python:3.11.1

COPY ./requirements.txt /app/
RUN pip install -U --no-cache-dir -r /app/requirements.txt

COPY ./alembic.ini /app/alembic.ini
COPY ./migrations /app/migrations/
COPY ./src /app/bot

WORKDIR /app

CMD ["python", "-m", "bot"]