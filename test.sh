#!/bin/bash

echo "test script is running"

TYPE_REEL=$1
LINK_AUDIO=$2

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/.env"

# Enable automatic exporting
set -o allexport

# Source the .env file (the '.' is a synonym for 'source')
if [[ -f "${ENV_FILE}" ]]; then
    source "${ENV_FILE}"
else
    echo ".env file not found at ${ENV_FILE}!"
    exit 1
fi

# Disable automatic exporting (optional, but good practice to avoid exporting unintended variables)
set +o allexport

rm -f ${INTERMEDIAR_VIDEOS_CAPTIONER_PATH}/video.json
rm -f ${INTERMEDIAR_VIDEOS_CAPTIONER_PATH}/video.mp4
yt-dlp -t mp4 --cookies-from-browser firefox "${LINK_AUDIO}" -o ${INTERMEDIAR_VIDEOS_CAPTIONER_PATH}/video.mp4

cd ${CAPTIONER_PATH} || exit
node sub.mjs public/video.mp4 




