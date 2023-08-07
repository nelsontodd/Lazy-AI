#!/bin/bash
source env.sh
cd /home/ubuntu/Lazy-AI/backend
#make dev > ../logs/backend.log 2>&1
gunicorn app:app --bind 127.0.0.1:5000 --workers 4 --timeout 400 > ../logs/backend.log 2>&1
