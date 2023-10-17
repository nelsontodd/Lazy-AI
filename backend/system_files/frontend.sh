#!/bin/bash
source env.sh
echo $ENVIRON
cd /home/ubuntu/Lazy-AI/client
# npm run build
# serve build/ > ../logs/frontend.log 2>&1
npm start > ../logs/frontend.log 2>&1
