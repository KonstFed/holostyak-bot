# syntax=docker/dockerfile:1
FROM postgres:latest
RUN apt update &&\
    apt install -y python3 &&\
    apt install -y python3-pip &&\
    pip3 install aiogram &&\
    pip3 install psycopg2-binary &&\
    apt install -y git
WORKDIR /home
RUN git clone https://github.com/KonstFed/holostyak-bot
WORKDIR /home/holostyak-bot
RUN git fetch &&\
    git switch docker
WORKDIR /home/holostyak-bot/configs
# RUN touch config.json &&\
#     echo '"db":{' > config.json &&\
#     echo '"dbname": "' >> config.json &&\
#     echo "$POSTGRES_DB" >> config.json &&\
#     echo '","user":' >> config.json &&\
#     echo "$POSTGRES_USER" >> config.json &&\
#     echo '","password":' >> config.json &&\
#     echo "$POSTGRES_PASSWORD" >> config.json &&\
#     echo '","host":"localhost"}, "bot": { "token": ' >> config.json &&\
COPY configs/config.json .
WORKDIR /home/holostyak-bot
# WORKDIR /home/holostyak-bot
# CMD ["python3","create_table.py","main.py"]