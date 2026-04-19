import random
import os
import dotenv
import json
from google import genai
from google.genai import types
import re


def extract_scripts_from_response(raw_text):
    """Extract script blocks from model output with tolerant parsing."""
    text = (raw_text or "").strip()
    if not text:
        return []

    # Priority 1: quoted scripts (supports straight and typographic quotes).
    quoted = [s.strip() for s in re.findall(r'["“](.*?)["”]', text, flags=re.DOTALL) if s.strip()]
    if quoted:
        return quoted

    # Priority 2: scripts separated with "--" blocks.
    chunks = [c.strip() for c in re.split(r'\s*--+\s*', text) if c.strip()]
    chunks = [c for c in chunks if c not in ("[]", "[ ]")]
    if chunks:
        return chunks

    # Priority 3: if no delimiter is respected, keep the whole response as one script.
    return [text]

dotenv.load_dotenv()

TOKEN = os.getenv('TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
INTERMEDIAR_VIDEOS_CAPTIONER_PATH = os.getenv('INTERMEDIAR_VIDEOS_CAPTIONER_PATH')
DATA_CLIENT_FILE = os.getenv('DATA_CLIENT_FILE')
ORIGINAL_CONTENT_SCRIPTS_FOLDER_PATH = os.getenv('ORIGINAL_CONTENT_SCRIPTS_FOLDER_PATH')
client = genai.Client()


# 1. Tes listes de variables pour automatiser la diversité
# themes = ["la dépression silencieuse", "la solitude moderne", "l'espoir après un échec", "la discipline froide", "l'amour rationnel"]
themes = ["les relations toxiquent"]

angles = [
    "Honnête et sans filtre",
    "Brutalement honnête et stoïque",
    "Froid, calculateur et orienté sur la revanche silencieuse",
    "Mystique et métaphorique (utiliser des analogies avec la nature, les animaux ou les saisons)",
    "Philosophique et sombre (accepter la noirceur du monde pour avancer)",
    "Grand frère qui te recadre sans prendre de gants",
    "Détaché et observateur (analyser les comportements humains de haut, sans émotion)",
    "Sagesse ancienne (parler comme un vieux maître fatigué mais qui a tout vu)",
    "Épique et martial (focalisé sur la conquête, la guerre intérieure et l'entraînement)",
    "Scientifique et comportemental (explication psychologique froide de pourquoi on souffre)",
    "Minimaliste et tranchant (utiliser uniquement des phrases très courtes, style militaire)",
    "Doux, empathique mais extrêmement ferme sur les limites à poser",
    "Cynique lucide (se moquer doucement des illusions de la société moderne)",

    # chatgpt
    "Auto-critique violente (le narrateur s'accuse lui-même sans chercher d'excuse)",
    "Confession honteuse (dire quelque chose qu'on n'avoue jamais)",
    "Point de vue du 'méchant' (assumer le rôle toxique et l'expliquer)",
    "Lucidité post-rupture (parler comme quelqu’un qui a tout compris trop tard)",
    "Désillusion totale (rien ne marche comme prévu, ton fataliste)",
    "Manipulateur assumé (expliquer comment manipuler sans morale)",
    "Victime qui se réveille (prise de conscience brutale)",
    "Regard extérieur froid (observer comme si c'était une expérience scientifique)",
    "Paranoïa réaliste (tout le monde joue un rôle, rien n’est innocent)",
    "Minimalisme nihiliste (quasi aucun espoir, phrases ultra sèches)",
    "Storytelling fragmenté (pensées décousues mais cohérentes émotionnellement)",
    "Projection futur (décrire ce qui va t’arriver si tu continues)",
    "Flashback émotionnel (parler comme si tu revivais une scène précise)",
    "Lettre jamais envoyée (à un ex, un ami, soi-même)",
    "Dialogue interne (toi vs toi-même)",
    "Analyse froide d’une erreur passée",
    "Ton clinique (comme un diagnostic médical)",
    "Surenchère dramatique volontaire (presque théâtral mais crédible)",
    "Ton résigné (plus aucune énergie pour se battre)",
    "Ironie passive-agressive",
    "Vision darwinienne des relations (survie, domination, sélection)",
    "Ton prophétique (comme si tu annonçais une vérité universelle)",
    "Détachement total (plus aucune implication émotionnelle)",
    "Regret silencieux (dire peu mais lourd)",
    "Observation sociale (comme un sociologue des relations modernes)"
]
# angles = ["Honnête et sans filtre"]

hooks = [
    "commencer directement par le text",
    "Poser une question psychologique très inconfortable",
    "Détruire immédiatement une croyance populaire sur le développement personnel",
    "S'adresser directement à une douleur silencieuse et très spécifique ('Si tu caches ceci...')",
    "Commencer par 'On t'a menti sur...' suivi d'un concept fondamental",
    "Faire une affirmation volontairement clivante ou qui fâche l'ego",
    "Décrire une situation toxique hyper-spécifique dans laquelle l'audience va se reconnaître à 100%",
    "Utiliser la psychologie inversée ('Passe cette vidéo si tu aimes ton confort mental')",
    "Révéler la vraie signification cachée d'un comportement humain banal",
    "Commencer par la conséquence tragique avant d'expliquer la cause ('Voilà comment tu finis seul...')",
    "Mettre le spectateur au défi dès la première seconde ('Tu n'es pas prêt à entendre ça')",
    "Donner une règle de vie sous forme de loi universelle et implacable",
    "Un constat froid et sans émotion sur la nature humaine",
    
    # chatgpt
    "Commencer par 'Personne ne va te dire ça mais...'",
    "Commencer par 'Le problème, c’est pas eux. C’est toi.'",
    "Commencer par une vérité qui fait mal immédiatement",
    "Dire quelque chose que la majorité refuse d’admettre",
    "Commencer par 'Tu fais cette erreur sans t’en rendre compte'",
    "Commencer par une scène directe ('T’es là, tu regardes ton téléphone...')",
    "Créer un malaise immédiat ('Tu sais déjà que ça te concerne')",
    "Commencer par 'Si ça te fait mal, c’est que c’est vrai'",
    "Commencer par une phrase contradictoire ('Plus tu aimes, plus tu perds')",
    "Hook en mode révélation ('Voilà ce que personne t’explique sur...')",
    "Commencer par une accusation directe ('Tu mens. À toi-même.')",
    "Commencer par 'Arrête de faire ça tout de suite'",
    "Hook fataliste ('Ça finit toujours comme ça')",
    "Commencer par une conséquence ('Tu vas finir seul si...')",
    "Créer un effet miroir ('Regarde bien tes relations...')",
    "Commencer par une statistique inventée mais crédible",
    "Commencer par 'Le jour où tu comprends ça, tout change'",
    "Hook en mode secret ('Je devrais pas dire ça mais...')",
    "Commencer par une punchline ultra courte",
    "Hook en mode comparaison ('Les gens forts font ça. Les autres...')",
    "Créer un sentiment d’urgence ('Si tu vois ça maintenant...')",
    "Commencer par une règle ('Règle numéro 1 : ...')",
    "Hook en mode observation ('Tu remarqueras un truc...')",
    "Commencer par une contradiction humaine ('On dit vouloir l’amour, mais...')",
    "Hook en mode défi ('Regarde jusqu’à la fin si t’es honnête')"
]
# hooks = ["commencer directement par le text"]

# Variables tirées au hasard pour cette génération
theme_choisi = random.choice(themes)
angle_choisi = random.choice(angles)
hook_choisi = random.choice(hooks)

# lecture des données du client
with open(f"{DATA_CLIENT_FILE}", 'r') as json_data:
    data = json.load(json_data)

# Paramètres fixes
nombre_scripts = data["scriptNumber"]
wordNumber = data["wordNumber"] 
template = data["template"]
input_prompt = data["createScriptFromInput"]

# transcription du lien
with open(f"{INTERMEDIAR_VIDEOS_CAPTIONER_PATH}/video.json", 'r') as f:
    caption = json.load(f)
word_list = [elm['text'] for elm in caption ]
transcription = ' '.join(word_list) 


system_instruction = "Tu es un assistant IA spécialisé dans l'écriture de scripts vidéos courts. Tu obéis strictement aux contraintes de ton, de style et de longueur"

consignes_default = ""

consignes_oogway = """
RÈGLES SPÉCIALES POUR LE RYTHME VOCAL (PERSONNAGE : SAGE/OOGWAY) :
Ce script sera dicté par une IA vocale. Le personnage est un vieux maître philosophe. Le débit doit être EXTRÊMEMENT LENT, grave et respirant.
1. Remplace la majorité des virgules par des points de suspension (...) pour forcer le TTS à marquer de longs silences.
2. Formule des phrases très courtes (4 à 6 mots maximum par segment).
3. Ne mets aucune exclamation (!), le ton doit rester plat, ancré et paisible en toutes circonstances.
4. Structure typique attendue : "Une idée... Un silence... Une conclusion implacable."
"""

consignes_joker = """
RÈGLES SPÉCIALES POUR LE RYTHME VOCAL (PERSONNAGE : SOMBRE/JOKER) :
Ce script sera dicté par une IA vocale. Le personnage est cynique, imprévisible et théâtral. Le débit doit être CHAOTIQUE et tranchant.
1. Alterne brusquement entre des phrases longues sans ponctuation (pour simuler un débit rapide et maniaque) et des mots isolés terminés par un point (pour des coupures brutales).
2. Utilise beaucoup de questions rhétoriques provocatrices (?).
3. Ajoute des amorces cyniques en début de phrase (ex: "Ah...", "Hmm...", "Vraiment ?") pour forcer le TTS à prendre un ton narquois.
4. Utilise des points de suspension (...) uniquement pour créer des attentes malsaines avant une vérité brutale.
"""

consignes_personnage = consignes_default if template == "default" else (consignes_oogway if template == "oogway" else consignes_joker)

# =====================================================================
# PROMPT 1 : GÉNÉRATION BASÉE SUR UN THÈME
# =====================================================================

prompt_theme = f"""Tu es un expert en création de contenu TikTok percutant et psychologique.
Ta mission : Écrire {nombre_scripts} script(s) original(aux) prêt(s) à être enregistré(s).

PARAMÈTRES DU SCRIPT :
- Durée visée par script : environ {wordNumber} mots.
- Thème central : {input_prompt}.
- Ton / Angle : {angle_choisi}.
- Type d'accroche (Hook) : {hook_choisi}.

{consignes_personnage}

RÈGLES STRICTES :
1. Aucun cliché de développement personnel (Interdit d'utiliser "sors de ta zone de confort", "n'abandonne jamais", "crois en toi").
2. Utilise un vocabulaire brut, authentique et conversationnel.
3. Fais des phrases courtes et percutantes.
4. Ne mets pas de didascalies complexes, juste le texte à prononcer.

Sépare clairement chaque script généré avec "--", ne place aucun mot en dehors du script entres les "--", respecte le nombre de script qui est de {nombre_scripts} et mets les scripts entre guillemets. Et si tu dois mettres des guillements dans un script utilise "'" """


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

{consignes_personnage}

RÈGLES STRICTES :
1. Ne copie/colle aucune phrase du script de référence. Inspire-toi de sa "vibe" émotionnelle et de son format d'impact.
2. Formule des concepts totalement nouveaux autour du même sujet.
3. Reste brut et sans clichés. Phrases courtes.

Sépare clairement chaque script généré avec "--", respecte le nombre de script qui est de {nombre_scripts} et mets les scripts entre guillemets."""

# Affichage pour vérifier (Dans ton vrai code, tu envoies ça à l'API de Gemma-3)

prompts_dico = {
    "default": [prompt_exemple, prompt_theme],
    "oogway": [prompt_exemple, prompt_theme],
    "joker": [prompt_exemple, prompt_theme],
}

print("PROMPT SÉLECTIONNÉ PRÊT POUR L'API :\n")
prompt_select = prompts_dico[template][0] if (data["createScriptFromLink"] == True) else prompts_dico[template][1]
print(prompt_select)

# reponse = client.models.generate_content(
#     model="gemma-3-27b-it",
#     contents=prompt_select,
# )

reponse = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt_select,
    config=types.GenerateContentConfig(
        system_instruction=system_instruction)
)

print("Réponse de l'IA\n")
scripts = extract_scripts_from_response(reponse.text)
            

print(reponse.text)
print(scripts)

with open(f"{ORIGINAL_CONTENT_SCRIPTS_FOLDER_PATH}/{template}-scripts.txt", 'a') as script_file:
    for script in scripts:
        cleaned_script = script.replace('"', '').strip()
        if cleaned_script and cleaned_script not in ("[]", "[ ]"):
            script_file.write(cleaned_script + "\n")
    
