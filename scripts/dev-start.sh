#!/bin/sh
#test script
echo "[DEV-SETUP]: Starting setup..."
export FLASK_APP=app.py
export FLASK_DEBUG=1
echo "[DEV-SETUP]: Environment variables created!"
sudo systemctl start mongod.service
echo "[DEV-SETUP]: MongoDB started!"
sudo systemctl status mongod
echo "[DEV-START]: Starting development server..."
python3.10 -m flask run --host 172.31.10.42

