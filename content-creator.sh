#!/bin/bash

echo "test script is running"

TEMPLATE=$1
LANG=$2
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
SCRIPT=$(head -n 1 "${ORIGINAL_CONTENT_SCRIPTS_FOLDER_PATH}/${TEMPLATE}-${LANG}-scripts.txt")
echo "Script: ${SCRIPT}"

tail -n +2 "${ORIGINAL_CONTENT_SCRIPTS_FOLDER_PATH}/${TEMPLATE}-${LANG}-scripts.txt" > "${ORIGINAL_CONTENT_SCRIPTS_FOLDER_PATH}/${TEMPLATE}-${LANG}-scripts.txt.tmp" && mv "${ORIGINAL_CONTENT_SCRIPTS_FOLDER_PATH}/${TEMPLATE}-${LANG}-scripts.txt.tmp" "${ORIGINAL_CONTENT_SCRIPTS_FOLDER_PATH}/${TEMPLATE}-${LANG}-scripts.txt"


cd ${CREATOR_PATH}/qwen3-tts-rs/ || exit

echo "run tts"

if [[ "${TEMPLATE}" == "default" ]]; then
    cargo run --release --features cli --bin generate_audio --   --model-dir ${QWEN_TTS_BASE_BIG_PATH}   --text "${SCRIPT}" --ref-audio default.wav   --ref-text "Et un jour je ne te dérangerai plus, je ne t'appellerai plus, je ne t'écrirai plus non plus. Tu n'entendras plus jamais ma voix. Et si un jour je te manque, rappelle-toi que j'étais là un jour. Et c'est toi qui m'as laissé partir. Si ce message te fait penser à quelqu'un, aime et suis-moi.
" --language french --output ${AUDIO_FOLDER_PATH}/${AUDIO_TMP}
elif [[ "${TEMPLATE}" == "joker" && "${LANG}" == "en" ]]; then
    cargo run --release --features cli --bin generate_audio --   --model-dir ${QWEN_TTS_BASE_BIG_PATH} --text "${SCRIPT}"  --ref-audio en_joker_sample.wav   --ref-text "I'm not angry, I'm just done. That's what people don't get. I'm not mad at anyone. I'm just done with situations that disrupt my peace, with people who don't love me." --output ${AUDIO_FOLDER_PATH}/${AUDIO_TMP}
elif [[ "${TEMPLATE}" == "joker" ]]; then
    cargo run --release --features cli --bin generate_audio --   --model-dir /${QWEN_TTS_BASE_BIG_PATH} --text "${SCRIPT}"  --ref-audio joker_test.wav   --ref-text "Ta loyauté, ton soutien, ton respect, le jour où tu n'as plus rien à offrir, tu deviens invisible. Ils se souviendront toujours de ce qu'ils peuvent te prendre, mais jamais de ce que tu leur offres." --language french --output ${AUDIO_FOLDER_PATH}/${AUDIO_TMP}
elif [[ "${TEMPLATE}" == "oogway" && "${LANG}" == "en" ]]; then
    cargo run --release --features cli --bin generate_audio --   --model-dir ${QWEN_TTS_BASE_BIG_PATH} --text "${SCRIPT}"  --ref-audio en_oogway_audio_sample.wav   --ref-text "Let them lose you. Let them walk away. Let them miss the light that you bring and the kindness you offer. Because my friend, it is not your task to prove your worth to anyone." --output ${AUDIO_FOLDER_PATH}/${AUDIO_TMP}
else
    cargo run --release --features cli --bin generate_audio --   --model-dir ${QWEN_TTS_BASE_BIG_PATH}   --text "${SCRIPT}"   --ref-audio oogway_test2.wav   --ref-text "Ce n'est pas une question de grands gestes ni de moments parfaits. C'est dans les petites choses que tout se joue, l'important, c'est de sentir chaque jour que tu comptes vraiment.
" --language french --output ${AUDIO_FOLDER_PATH}/${AUDIO_TMP}
fi

ffmpeg -i ${AUDIO_FOLDER_PATH}/${AUDIO_TMP} ${AUDIO_FILE_PATH} -y
