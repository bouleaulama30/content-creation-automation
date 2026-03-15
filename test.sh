#!/bin/bash

# Enable automatic exporting
set -o allexport

# Source the .env file (the '.' is a synonym for 'source')
if [[ -f .env ]]; then
    source .env
else
    echo ".env file not found!"
    exit 1
fi

# Disable automatic exporting (optional, but good practice to avoid exporting unintended variables)
set +o allexport

# Now you can use the variables in your script

# ... rest of your script
