#!/bin/sh

docker run -it -v $PWD/src:/app gtechedu/streamlit streamlit run app.py
