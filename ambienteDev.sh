#!/bin/sh

docker run -it -v $PWD:/app gtechedu/streamlit streamlit run src/app.py
