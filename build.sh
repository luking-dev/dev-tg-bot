#!/usr/bin/env bash
sudo apt-get install libportaudio2 -y
sudo apt-get install libasound-dev -y
pip install --upgrade pip setuptools wheel
pip install p5py
pip install PEP517
pip install pylibdmtx
pip install pylibdmtx[scripts]
apt install build-essential portaudio19-dev
pip install -r requirements.txt