#!/bin/sh

#docker run -it -v $PWD:/app  streamlit run src/Home.py

#versão local
docker run -it -v $PWD:/app  gtechedu/streamlit  streamlit run src/Home.py