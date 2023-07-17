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

# Installing pandoc
pandoc --version
if [ $? = 0 ]; then
  echo "Environment setup complete";
else
  brew install pandoc
  brew tap homebrew/cask
  brew install --cask basictex
  eval "$(/usr/libexec/path_helper)"
  # Update $PATH to include `/usr/local/texlive/2022basic/bin/universal-darwin`
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
set +x
# conda activate AIProject
