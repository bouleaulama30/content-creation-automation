#!/bin/bash

echo "test script is running"

TEMPLATE=$1
AUDIO_TMP=audio.wav

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

# Read and remove the first line of the file
SCRIPT=$(head -n 1 "${ORIGINAL_CONTENT_DEFAULT_SCRIPT_FILE_PATH}")
echo "Script: ${SCRIPT}"

tail -n +2 "${ORIGINAL_CONTENT_DEFAULT_SCRIPT_FILE_PATH}" > "${ORIGINAL_CONTENT_DEFAULT_SCRIPT_FILE_PATH}.tmp" && mv "${ORIGINAL_CONTENT_DEFAULT_SCRIPT_FILE_PATH}.tmp" "${ORIGINAL_CONTENT_DEFAULT_SCRIPT_FILE_PATH}"


cd ${CREATOR_PATH}/qwen3-tts-rs/ || exit

echo "run tts"
cargo run --release --features cli --bin generate_audio --   --model-dir ~/IA/modele-base-06b   --text "${SCRIPT}" --ref-audio default.wav   --ref-text "Et un jour je ne te dérangerai plus, je ne t'appellerai plus, je ne t'écrirai plus non plus. Tu n'entendras plus jamais ma voix. Et si un jour je te manque, rappelle-toi que j'étais là un jour. Et c'est toi qui m'as laissé partir. Si ce message te fait penser à quelqu'un, aime et suis-moi.
" --language french --output ${AUDIO_FOLDER_PATH}/${AUDIO_TMP}

ffmpeg -i ${AUDIO_FOLDER_PATH}/${AUDIO_TMP} ${AUDIO_FILE_PATH} -y


