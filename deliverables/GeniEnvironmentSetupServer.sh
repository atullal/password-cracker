#!/bin/bash

sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.7 get-pip.py
export PATH=$PATH:/users/anishil/.local/bin
pip3.7 install virtualenv
sudo apt-get install python3.6-venv

python3.7 -m venv .venv
source .venv/bin/activate
pip3.7 install markupsafe==1.1.1 flask
pip3.7 install flask_cors
pip3.7 install websockets
pip3.7 install flask_sock
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok