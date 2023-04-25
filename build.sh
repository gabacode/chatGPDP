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
python -m pip install --upgrade pip

# Install dependencies
pip install -r $DIR/requirements.txt

# Install briefcase
pip install briefcase

# If the project doesn't have a build directory, create it
if [ ! -d "$DIR/build" ]; then
    echo $delimiters
    echo "Build directory created"
    echo $delimiters
    briefcase create
fi

# Build for macOS or Linux
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo $delimiters
    echo "macOS detected"
    echo $delimiters
    briefcase build macos
else
    echo $delimiters
    echo "Building for Linux"
    echo $delimiters
    briefcase build linux
fi

# If the user wants to run the app, run it
read -p "Do you want to run the app? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo $delimiters
    echo "Running the app..."
    echo $delimiters
    briefcase run
else
    echo $delimiters
    echo "See you soon 👋"
    echo $delimiters
fi

# Deactivate virtualenv
deactivate
