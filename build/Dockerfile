FROM ubuntu:latest

ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update && \ 
    apt install -y python3 python3-pip gettext && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install streamlit SQLAlchemy psycopg2-binary 


    