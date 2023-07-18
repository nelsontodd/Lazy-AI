#!/bin/bash
set -x
export PROJECT_DIR=`pwd` #$(cd "$(dirname "$0")"; pwd)
export ABS_SRC_DIR=`realpath "backend/"`
export OPENAI_API_KEY=""
export OPENAI_USER=""
export OPENAI_MODEL="gpt-4-0613"
export MATHPIX_API_KEY=""
export MATHPIX_APP_ID=""
export SQUARE_ACCESS_TOKEN=""
export PYTHONPATH=$PYTHONPATH:$ABS_SRC_DIR
export PUBLIC_URL="http://homeworkhero.io"
export DANGEROUSLY_DISABLE_HOST_CHECK=true


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
    #Standard practice is to symlink this version of tlmgr to /usr/bin/tlmgr but this fails
    #Some kind of path error. So we just pass in the absolute path to tlmgr
    sudo /usr/local/texlive/2023/bin/x86_64-linux/tlmgr init-usertree
    sudo /usr/local/texlive/2023/bin/x86_64-linux/tlmgr update --self
    sudo /usr/local/texlive/2023/bin/x86_64-linux/tlmgr install texliveonfly
    sudo /usr/local/texlive/2023/bin/x86_64-linux/tlmgr install xelatex
    sudo /usr/local/texlive/2023/bin/x86_64-linux/tlmgr install adjustbox
    sudo /usr/local/texlive/2023/bin/x86_64-linux/tlmgr install tcolorbox
    sudo /usr/local/texlive/2023/bin/x86_64-linux/tlmgr install collectbox
    sudo /usr/local/texlive/2023/bin/x86_64-linux/tlmgr install ucs
    sudo /usr/local/texlive/2023/bin/x86_64-linux/tlmgr install environ
    sudo /usr/local/texlive/2023/bin/x86_64-linux/tlmgr install trimspaces
    sudo /usr/local/texlive/2023/bin/x86_64-linux/tlmgr install titling
    sudo /usr/local/texlive/2023/bin/x86_64-linux/tlmgr install enumitem
    sudo /usr/local/texlive/2023/bin/x86_64-linux/tlmgr install rsfs
fi
echo "Installing Systemd Service Files; not starting them"
sudo cp backend/system_files/backend.service /etc/systemd/system/multi-user.target.wants/
sudo cp backend/system_files/backend.service /etc/systemd/system/
sudo cp backend/system_files/frontend.service /etc/systemd/system/multi-user.target.wants/
sudo cp backend/system_files/frontend.service /etc/systemd/system/
sudo systemctl daemon-reload
set +x
