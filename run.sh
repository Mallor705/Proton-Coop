#!/bin/bash

cd "$(dirname "$0")"

# Compile GResource bundle
(cd src/gui/resources && glib-compile-resources --target=compiled.gresource resources.xml)

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate

pip install -r requirements.txt

python3 protoncoop.py "$@"
