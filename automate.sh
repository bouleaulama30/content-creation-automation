#!/bin/bash

# --- 1. Préparation ---
# On s'assure d'être dans le bon dossier pour commencer
cd ~/content-creation-automation/ || exit

# --- 2. Génération des données (Python) ---
echo "🐍 Génération du fichier props.json via Python..."
python3 test.py

# --- 3. Premier Rendu Remotion (Vidéo de base) ---
# On génère la vidéo brute dans le dossier public du projet de sous-titrage
echo "🎬 Rendu de la vidéo brute..."
npx remotion render MyComp \
    --props=./props.json \
    --concurrency=2 \
    --output=/home/leo/tiktok-template/public/video.mp4

# --- 4. Passage au projet de sous-titrage ---
echo "📂 Passage au projet tiktok-template..."
cd ../tiktok-template/ || exit

# --- 5. Nettoyage et Transcription ---
echo "🗑️ Nettoyage des anciens sous-titres..."
rm -f public/video.json

echo "🎙️ Génération des sous-titres (Whisper/Node)..."
# Ce script doit générer le nouveau public/video.json
node sub.mjs public/video.mp4

# --- 6. Rendu Final (Vidéo avec sous-titres) ---
echo "🚀 Rendu final du Reel avec sous-titres..."
# Ici on lance le rendu du projet tiktok-template
npx remotion render \
    --concurrency=2 \
    --output=./out/final_reel_$(date +%Y%m%d_%H%M%S).mp4

echo "✅ Terminé ! Ton Reel est prêt dans le dossier out/ de tiktok-template."