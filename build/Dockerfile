FROM ubuntu:latest

ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update && \ 
    apt install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install streamlit pandasai SQLAlchemy psycopg2-binary pygwalker


    