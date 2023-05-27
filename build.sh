#!/usr/bin/env bash
sudo apt-get install libportaudio2 -y
sudo apt-get install libasound-dev -y
pip install pylibdmtx
pip install pylibdmtx[scripts]
pip install -r requirements.txt