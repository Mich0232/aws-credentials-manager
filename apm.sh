#!/bin/bash

APM_DIR=$(dirname -- ${BASH_SOURCE[0]})

initialize() {
  mkdir ~/.apm && touch ~/.apm/store
}

if [[ ! -e "$HOME/.apm" ]]; then
  echo "Initializing workdir"
  initialize
fi

python $APM_DIR/apm.py $@
