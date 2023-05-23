set -x PROJECT_DIR (cd (dirname (status -f)); and pwd) #$(cd "$(dirname "$0")"; pwd)
set -x ABS_SRC_DIR (realpath "backend/")
set -x OPENAI_API_KEY ""
set -x OPENAI_USER  "Nelson Morrow"
set -x OPENAI_MODEL  "gpt-3.5-turbo"
set -x MATHPIX_API_KEY ""
set -x MATHPIX_APP_ID ""
set -gx PYTHONPATH "$PYTHONPATH:$ABS_SRC_DIR"
