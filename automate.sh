#!/bin/bash

TYPE_REEL=$1
echo "suppression des video dans le dossier public de l'assembleur"

rm /home/leo/content-creation-automation/assembler/public/*.mp4

echo "🐍 Génération du fichier props.json via Python..."
python3 selector/select-videos-${TYPE_REEL}.py || exit

# On s'assure d'être dans le bon dossier pour commencer
cd /home/leo/content-creation-automation/assembler/ || exit


# --- 3. Premier Rendu Remotion (Vidéo de base) ---
# On génère la vidéo brute dans le dossier public du projet de sous-titrage
echo "🎬 Rendu de la vidéo brute..."
npx remotion render MyComp \
    --props=./props.json \
    --concurrency=2 \
    --output=/home/leo/content-creation-automation/captioner/public/video.mp4 || exit

# --- 4. Passage au projet de sous-titrage ---
echo "📂 Passage au projet captioner..."
cd ../captioner/ || exit

# --- 5. Nettoyage et Transcription ---
echo "🗑️ Nettoyage des anciens sous-titres..."
rm -f public/video.json

echo "🎙️ Génération des sous-titres (Whisper/Node)..."
# Ce script doit générer le nouveau public/video.json
node sub.mjs public/video.mp4 

# --- 6. Rendu Final (Vidéo avec sous-titres) ---
echo "🚀 Rendu final du Reel avec sous-titres..."
# Ici on lance le rendu du projet captioner
npx remotion render \
    --concurrency=2 \
    --output=./out/video.mp4

echo "Envoie de la video, de la description et de la miniature..."
cd /home/leo/content-creation-automation/ || exit
python deliver/deliver.py

echo "✅ Terminé ! Ton Reel est prêt dans le dossier out/ de captioner."