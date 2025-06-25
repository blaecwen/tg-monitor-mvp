#!/usr/bin/env sh
# Setup Python virtual environment and install dependencies
set -e

# Create virtual environment if it doesn't exist
if [ ! -d .venv ]; then
    python -m venv .venv
fi

# Install dependencies using the venv's pip
.venv/bin/pip install -r requirements.txt

if [ -n "$FISH_VERSION" ]; then
    printf '\nTo activate the virtual environment run:\n  source .venv/bin/activate.fish\n'
else
    printf '\nTo activate the virtual environment run:\n  source .venv/bin/activate\n'
fi
