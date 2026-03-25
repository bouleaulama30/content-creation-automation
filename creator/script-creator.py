import random
import os
import dotenv
import json
from google import genai
from google.genai import types
import re

dotenv.load_dotenv()

TOKEN = os.getenv('TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
INTERMEDIAR_VIDEOS_CAPTIONER_PATH = os.getenv('INTERMEDIAR_VIDEOS_CAPTIONER_PATH')
CREATOR_PATH = os.getenv('CREATOR_PATH')
ORIGINAL_CONTENT_SCRIPTS_FOLDER_PATH = os.getenv('ORIGINAL_CONTENT_SCRIPTS_FOLDER_PATH')
client = genai.Client()


# 1. Tes listes de variables pour automatiser la diversité
# themes = ["la dépression silencieuse", "la solitude moderne", "l'espoir après un échec", "la discipline froide", "l'amour rationnel"]
themes = ["les relations toxiquent"]

# angles = ["Brutalement honnête et stoïque", "Doux, empathique mais ferme", "Scientifique (explication psychologique)", "Philosophique et sombre", "Grand frère qui te recadre"]
angles = ["Honnête et sans filtre"]

# hooks = ["Poser une question inconfortable", "Donner une statistique choquante", "Commencer par 'On t'a menti sur...'", "Un silence de 2 secondes puis une vérité brutale", "Détruire une croyance populaire"]
hooks = ["commencer directement par le text"]

# Variables tirées au hasard pour cette génération
theme_choisi = random.choice(themes)
angle_choisi = random.choice(angles)
hook_choisi = random.choice(hooks)

# lecture des données du client
with open(f"{CREATOR_PATH}/data.json", 'r') as json_data:
    data = json.load(json_data)

# Paramètres fixes
nombre_scripts = data["scriptNumber"]
wordNumber = data["wordNumber"] 
# wordNumber = 100
template = data["template"]

# transcription du lien
with open(f"{INTERMEDIAR_VIDEOS_CAPTIONER_PATH}/video.json", 'r') as f:
    caption = json.load(f)
word_list = [elm['text'] for elm in caption ]
transcription = ' '.join(word_list) 


system_instruction = "Tu es un assistant IA spécialisé dans l'écriture de scripts vidéos courts. Tu obéis strictement aux contraintes de ton, de style et de longueur"

# =====================================================================
# PROMPT 1 : GÉNÉRATION BASÉE SUR UN THÈME
# =====================================================================

prompt_theme = f"""Tu es un expert en création de contenu TikTok percutant et psychologique.
Ta mission : Écrire {nombre_scripts} script(s) original(aux) prêt(s) à être enregistré(s).

PARAMÈTRES DU SCRIPT :
- Durée visée par script : environ {wordNumber} mots.
- Thème central : {theme_choisi}.
- Ton / Angle : {angle_choisi}.
- Type d'accroche (Hook) : {hook_choisi}.

RÈGLES STRICTES :
1. Aucun cliché de développement personnel (Interdit d'utiliser "sors de ta zone de confort", "n'abandonne jamais", "crois en toi").
2. Utilise un vocabulaire brut, authentique et conversationnel.
3. Fais des phrases courtes et percutantes.
4. Ne mets pas de didascalies complexes, juste le texte à prononcer.

Sépare clairement chaque script généré avec "--- SCRIPT [Numéro] ---"."""


# =====================================================================
# PROMPT 2 : GÉNÉRATION BASÉE SUR UN SCRIPT EXISTANT (L'EXEMPLE)
# =====================================================================

prompt_exemple = f"""Tu es un expert en création de contenu TikTok percutant.
Voici un script vidéo qui a fait des millions de vues (Script de référence) :
{transcription}

Ta mission : Écrire {nombre_scripts} NOUVEAU(X) script(s) de {wordNumber} mots.
Tu dois conserver EXACTEMENT la même ambiance globale, le même rythme et le même thème sous-jacent que le script de référence, MAIS tu dois appliquer ces nouvelles contraintes :

NOUVEAUX PARAMÈTRES :
- Ton / Angle : {angle_choisi}.
- Type d'accroche (Hook) : {hook_choisi}.

RÈGLES STRICTES :
1. Ne copie/colle aucune phrase du script de référence. Inspire-toi de sa "vibe" émotionnelle et de son format d'impact.
2. Formule des concepts totalement nouveaux autour du même sujet.
3. Reste brut et sans clichés. Phrases courtes.

Sépare clairement chaque script généré avec "--", respecte le nombre de script qui est de {nombre_scripts} et mets les scripts entre guillemets."""

# Affichage pour vérifier (Dans ton vrai code, tu envoies ça à l'API de Gemma-3)
print("PROMPT SÉLECTIONNÉ PRÊT POUR L'API :\n")
print(prompt_exemple)

reponse = client.models.generate_content(
    model="gemma-3-27b-it",
    contents=prompt_exemple,
)

print("Réponse de l'IA\n")
pattern = r'"(.*?)"'
scripts = re.findall(pattern, reponse.text)
            

print(reponse.text)
print(scripts)

with open(f"{ORIGINAL_CONTENT_SCRIPTS_FOLDER_PATH}/{template}-scripts.txt", 'a') as script_file:
    for script in scripts:
        script.replace('"','')
        script_file.write(script+"\n")
    