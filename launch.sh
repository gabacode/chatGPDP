#!/bin/bash

delimiters="------------------------------------------------------------"

echo $delimiters
echo "Launching 🚀"
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
python -m pip install --upgrade pip

# Install dependencies
pip install -r $DIR/requirements.txt

# Install briefcase
pip install briefcase

# Run the app in dev mode
briefcase dev

# See if there are errors, if so, exit
if [ $? -ne 0 ]; then
    echo $delimiters
    echo "There was an error, exiting..."
    echo $delimiters
    exit 1
fi

echo $delimiters
echo "See you soon 👋"
echo $delimiters

# Deactivate virtualenv
deactivate