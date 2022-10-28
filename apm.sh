APM_DIR=$(dirname -- ${BASH_SOURCE[0]})
source $APM_DIR/venv/bin/activate
python $APM_DIR/src/commands.py $@
