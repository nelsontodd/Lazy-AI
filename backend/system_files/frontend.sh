#!/bin/bash
source env.sh
cd /home/ubuntu/Lazy-AI/client
npm start > ../logs/frontend.log 2>&1
