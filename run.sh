#!/usr/bin/env bash

## starts up the langgraph agent
python3.11 -m venv env
source env/bin/activate
pip install -r requirements.txt
export COHERE_API_KEY=$(cat ./.secrets/cohere_key.txt)

python main.py resume.tex jd.txt