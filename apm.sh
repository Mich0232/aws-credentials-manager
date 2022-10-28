CLOUDER_DIR=$(dirname -- ${BASH_SOURCE[0]})
source $CLOUDER_DIR/venv/bin/activate
python $CLOUDER_DIR/src/commands.py $@
