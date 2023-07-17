#!/bin/bash
set -x
export PROJECT_DIR=`pwd` #$(cd "$(dirname "$0")"; pwd)
export ABS_SRC_DIR=`realpath "backend/"`
export OPENAI_API_KEY=""
export OPENAI_USER="Nelson Morrow"
export OPENAI_MODEL="gpt-3.5-turbo"
export MATHPIX_API_KEY=""
export MATHPIX_APP_ID=""
export SQUARE_ACCESS_TOKEN=""
if [ ! -d ".venv/bin" ]; then
  echo ".venv does not exist."
  virtualenv -p python3.10.6 .venv
  source .venv/bin/activate
  pip3 install -r requirements.txt
fi
source .venv/bin/activate
# Installing pandoc
pandoc --version
if [ $? = 0 ]; then
  echo "Environment setup complete";
else
    sudo apt install pandoc
    sudo apt install basictex texlive texlive-latex-extra texlive-lang-english
    eval "$(/usr/libexec/path_helper)"
    ## Update $PATH to include `/usr/local/texlive/2022basic/bin/universal-darwin`
    ## export PATH=/usr/local/texlive/2023/bin/x86_64-linux:$PATH
    sudo tlmgr init-usertree
    sudo tlmgr update --self
    sudo tlmgr install texliveonfly
    sudo tlmgr install xelatex
    sudo tlmgr install adjustbox
    sudo tlmgr install tcolorbox
    sudo tlmgr install collectbox
    sudo tlmgr install ucs
    sudo tlmgr install environ
    sudo tlmgr install trimspaces
    sudo tlmgr install titling
    sudo tlmgr install enumitem
    sudo tlmgr install rsfs
fi
echo "Installing Systemd Service Files; not starting them"
sudo cp backend/system_files/backend.service /etc/systemd/system/multi-user.target.wants/
sudo cp backend/system_files/backend.service /etc/systemd/system/
sudo cp backend/system_files/frontend.service /etc/systemd/system/multi-user.target.wants/
sudo cp backend/system_files/frontend.service /etc/systemd/system/
sudo systemctl daemon-reload
set +x
