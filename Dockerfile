FROM python:3.11.1
ENV APP_NAME=src

COPY ./requirements.txt /app/
RUN pip install -U --no-cache-dir -r /app/requirements.txt

COPY ./alembic.ini /app/alembic.ini
COPY ./migrations /app/migrations/

COPY ./${APP_NAME} /app/${APP_NAME}

WORKDIR /app

CMD ["python", "-m", "${APP_NAME}"]