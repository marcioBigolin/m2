#!/bin/sh

if [ "$(docker ps -a | grep mda)" ]; then
    echo "Container exists"
    docker start mda
else
    echo "Container does not exist! Creating ..."
    docker run -itd --network mdinet --name mda -v $PWD:/app -p 8501:8501 gtechedu/streamlit  streamlit run src/Home.py 
fi