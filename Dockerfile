# Marakulin Andrey @annndruha
# 2023

FROM python:3.11.1
ENV APP_NAME=src
#ENV APP_MODULE=${APP_NAME}.routes.base:app

ADD ./ /app
WORKDIR /app

#COPY ./requirements.txt /app/
RUN pip install -U -r /app/requirements.txt

#COPY ./alembic.ini /alembic.ini
#COPY ./migrations /migrations/

#COPY ./${APP_NAME} /app/${APP_NAME}

CMD ["python", "-m", "src"]

# Base image
#FROM python:3.11.1
#
## Create directoris inside container
#ADD ./ /print-bot
#WORKDIR /print-bot
#
#
#COPY ./requirements.txt /app/
#RUN pip install --no-cache-dir -r requirements.txt
#COPY ./alembic.ini /alembic.ini
#COPY ./migrations /migrations/
#
## Install libs from requirements
#
#
## Specify the port number the container should expose
#EXPOSE 42
#
## Run the file
#CMD ["python", "-u", "./src/main.py"]

##===== Example docker Ubuntu command:
# docker run -d --name print-bot -v /root/print-bot:/print-bot imageid
##==== Next, add auth.ini file to /root/print-bot
##==== and restart container
# docker stop print-bot
# docker start print-bot

#FROM python:3.10
#WORKDIR /app
#
#COPY requirements.txt /app/
#RUN pip install --no-cache-dir -r /app/requirements.txt
#
#ADD bot /app/bot
#
#CMD [ "python3", "-m", "bot"]