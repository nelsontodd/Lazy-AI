#!/bin/bash
source env.sh
cd /home/ubuntu/Lazy-AI/backend
make dev > ../logs/backend.log 2>&1
