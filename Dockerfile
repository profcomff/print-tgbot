# Marakulin Andrey @annndruha
# 2021

# Base image
FROM python:3.10.0

# Create directoris inside container
ADD ./ /print-bot
WORKDIR /print-bot

# Install libs from requirements
RUN pip install --no-cache-dir -r requirements.txt

# Specify the port number the container should expose 
EXPOSE 42

# Run the file
CMD ["python", "-u", "./print-bot.py"]

##===== Example docker Ubuntu command:
# docker run -d --name print-bot -v /root/print-bot:/print-bot imageid
##==== Next, add auth.ini file to /root/print-bot
##==== and restart container
# docker stop print-bot
# docker start print-bot