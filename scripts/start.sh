#!/bin/sh
echo "[SETUP]: Starting setup..."
export FLASK_APP=app.py
export FLASK_DEBUG=0
echo "[SETUP]: Environment variables created!"
sudo systemctl start mongod.service
echo "[SETUP]: MongoDB started!"
sudo systemctl status mongod
echo "[SETUP]: Starting server..."
python3.10 app.py

