#!/bin/bash

delimiters="------------------------------------------------------------"

echo $delimiters
echo "Starting build..."
echo $delimiters

# Get current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create virtualenv
if [ ! -d "$DIR/venv" ]; then
    python3 -m venv $DIR/venv
    echo $delimiters
    echo "Virtualenv created"
    echo $delimiters
fi

# Activate env
source $DIR/venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r $DIR/requirements.txt

# Install pyinstaller
pip install pyinstaller

# Run pyinstaller
pyinstaller $DIR/specs/single.spec

# Deactivate virtualenv
deactivate

echo $delimiters
echo "Build complete"
echo $delimiters