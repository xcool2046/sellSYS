#!/bin/bash
set -e

echo ">>> Stopping old uvicorn process..."
pkill uvicorn || true
sleep 2

echo ">>> Backing up old backend..."
mv backend backend_old_$(date +%s)

echo ">>> Unpacking new backend code..."
tar -xzf backend.tar.gz

echo ">>> Entering backend directory..."
cd backend

echo ">>> Removing old database..."
rm -f sellsys.db

echo ">>> Creating Python virtual environment..."
python3 -m venv venv

echo ">>> Installing dependencies into venv..."
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

echo ">>> Starting new uvicorn process in the background..."
nohup ./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 &

echo ">>> Deployment script finished."