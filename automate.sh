#!/bin/bash

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


if [ -n "$LINK_AUDIO" ]; then
    echo "suppresion de l'ancien audio"
    rm ${AUDIO_FILE_PATH}
    echo "Téléchargement de l'audio du lien ${LINK_AUDIO}"
    ${YT_DLP_PATH} -t mp3 --cookies-from-browser firefox "${LINK_AUDIO}" -o ${AUDIO_FILE_PATH}
fi

``
echo "suppression des video dans le dossier public de l'assembleur"
rm ${INTERMEDIAR_VIDEOS_ASSEMBLER_PATH}/*.mp4

echo "🐍 Génération du fichier props.json via Python..."
${PYTHON_PATH} ${SELECTOR_PATH}/select-videos-${TYPE_REEL}.py || exit

# On s'assure d'être dans le bon dossier pour commencer
cd ${ASSEMBLER_PATH} || exit


# --- 3. Premier Rendu Remotion (Vidéo de base) ---
# On génère la vidéo brute dans le dossier public du projet de sous-titrage
echo "🎬 Rendu de la vidéo brute..."
npx remotion render MyComp \
    --props=./props.json \
    --concurrency=${CONCURRENCY} \
    --output=${INTERMEDIAR_VIDEOS_CAPTIONER_PATH}/video.mp4 || exit

# --- 4. Passage au projet de sous-titrage ---
echo "📂 Passage au projet captioner..."
cd ${CAPTIONER_PATH} || exit

# --- 5. Nettoyage et Transcription ---
echo "🗑️ Nettoyage des anciens sous-titres..."
rm -f ${INTERMEDIAR_VIDEOS_CAPTIONER_PATH}/video.json

echo "🎙️ Génération des sous-titres (Whisper/Node)..."
# Ce script doit générer le nouveau ${INTERMEDIAR_VIDEOS_CAPTIONER_PATH}/video.json
node sub.mjs public/video.mp4 

${PYTHON_PATH} ${CAPTIONER_PATH}/remove_caption.py || exit

# --- 6. Rendu Final (Vidéo avec sous-titres) ---
echo "🚀 Rendu final du Reel avec sous-titres..."
# Ici on lance le rendu du projet captioner
npx remotion render \
    --concurrency=${CONCURRENCY} \
    --output=${PRODUCTION_FOLDER_PATH}/video.mp4

echo "Envoie de la video, de la description et de la miniature..."
cd ${PROJECT_BASE_PATH} || exit
${PYTHON_PATH} ${DELIVER_PATH}/deliver.py

echo "✅ Terminé ! Ton Reel est prêt dans le dossier ${PRODUCTION_FOLDER_PATH}."
