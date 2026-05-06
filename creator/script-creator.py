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
DATA_CLIENT_FILE = os.getenv('DATA_CLIENT_FILE')
SCRIPT_CREATOR_MODEL = os.getenv('SCRIPT_CREATOR_MODEL')
ORIGINAL_CONTENT_SCRIPTS_FOLDER_PATH = os.getenv('ORIGINAL_CONTENT_SCRIPTS_FOLDER_PATH')
client = genai.Client()

# Read language from data.json
with open(f"{DATA_CLIENT_FILE}", 'r') as json_data:
    data = json.load(json_data)

LANGUAGE = data.get("LANG", "fr")  # Default to French if not specified
is_from_link = data.get("createScriptFromLink", False)


def extract_scripts_from_response(raw_text):
    """Extract script blocks from model output with tolerant parsing."""
    text = (raw_text or "").strip()
    if not text:
        return []

    # Priority 1: quoted scripts (supports straight and typographic quotes).
    quoted = [s.strip() for s in re.findall(r'[""](.*?)[""]', text, flags=re.DOTALL) if s.strip()]
    if quoted:
        return quoted

    # Priority 2: scripts separated with "--" blocks.
    chunks = [c.strip() for c in re.split(r'\s*--+\s*', text) if c.strip()]
    chunks = [c for c in chunks if c not in ("[]", "[ ]")]
    if chunks:
        return chunks

    # Priority 3: if no delimiter is respected, keep the whole response as one script.
    return [text]


# =====================================================================
# FRENCH CONTENT LISTS
# =====================================================================

themes_fr = ["les relations toxiques"]

angles_fr = [
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
    "Auto-critique violente (le narrateur s'accuse lui-même sans chercher d'excuse)",
    "Confession honteuse (dire quelque chose qu'on n'avoue jamais)",
    "Point de vue du 'méchant' (assumer le rôle toxique et l'expliquer)",
    "Lucidité post-rupture (parler comme quelqu'un qui a tout compris trop tard)",
    "Désillusion totale (rien ne marche comme prévu, ton fataliste)",
    "Manipulateur assumé (expliquer comment manipuler sans morale)",
    "Victime qui se réveille (prise de conscience brutale)",
    "Regard extérieur froid (observer comme si c'était une expérience scientifique)",
    "Paranoïa réaliste (tout le monde joue un rôle, rien n'est innocent)",
    "Minimalisme nihiliste (quasi aucun espoir, phrases ultra sèches)",
    "Storytelling fragmenté (pensées décousues mais cohérentes émotionnellement)",
    "Projection futur (décrire ce qui va t'arriver si tu continues)",
    "Flashback émotionnel (parler comme si tu revivais une scène précise)",
    "Lettre jamais envoyée (à un ex, un ami, soi-même)",
    "Dialogue interne (toi vs toi-même)",
    "Analyse froide d'une erreur passée",
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

hooks_fr = [
    "commencer directement par le texte",
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
    "Commencer par 'Personne ne va te dire ça mais...'",
    "Commencer par 'Le problème, c'est pas eux. C'est toi.'",
    "Commencer par une vérité qui fait mal immédiatement",
    "Dire quelque chose que la majorité refuse d'admettre",
    "Commencer par 'Tu fais cette erreur sans t'en rendre compte'",
    "Commencer par une scène directe ('T'es là, tu regardes ton téléphone...')",
    "Créer un malaise immédiat ('Tu sais déjà que ça te concerne')",
    "Commencer par 'Si ça te fait mal, c'est que c'est vrai'",
    "Commencer par une phrase contradictoire ('Plus tu aimes, plus tu perds')",
    "Hook en mode révélation ('Voilà ce que personne t'explique sur...')",
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
    "Créer un sentiment d'urgence ('Si tu vois ça maintenant...')",
    "Commencer par une règle ('Règle numéro 1 : ...')",
    "Hook en mode observation ('Tu remarqueras un truc...')",
    "Commencer par une contradiction humaine ('On dit vouloir l'amour, mais...')",
    "Hook en mode défi ('Regarde jusqu'à la fin si t'es honnête')"
]

system_instruction_fr = "Tu es un assistant IA spécialisé dans l'écriture de scripts vidéos courts. Tu obéis strictement aux contraintes de ton, de style et de longueur"

consignes_default_fr = ""

consignes_oogway_fr = ""

consignes_joker_fr = """
RÈGLES SPÉCIALES POUR LE RYTHME VOCAL (PERSONNAGE : SOMBRE/JOKER) :
Ce script sera dicté par une IA vocale. Le personnage est cynique, imprévisible et théâtral. Le débit doit être CHAOTIQUE et tranchant.
1. Alterne brusquement entre des phrases longues sans ponctuation (pour simuler un débit rapide et maniaque) et des mots isolés terminés par un point (pour des coupures brutales).
2. Utilise beaucoup de questions rhétoriques provocatrices (?).
3. Ajoute des amorces cyniques en début de phrase (ex: "Ah...", "Hmm...", "Vraiment ?") pour forcer le TTS à prendre un ton narquois.
4. Utilise des points de suspension (...) uniquement pour créer des attentes malsaines avant une vérité brutale.
"""

# =====================================================================
# ENGLISH CONTENT LISTS
# =====================================================================

themes_en = ["toxic relationships"]

angles_en = [
    "Honest and unfiltered",
    "Brutally honest and stoic",
    "Cold, calculating and focused on silent revenge",
    "Mystical and metaphorical (use analogies with nature, animals or seasons)",
    "Philosophical and dark (accept the world's darkness to move forward)",
    "Big brother who straightens you out without holding back",
    "Detached and observant (analyze human behavior from above, without emotion)",
    "Ancient wisdom (speak like an old tired master who has seen it all)",
    "Epic and martial (focused on conquest, inner war and training)",
    "Scientific and behavioral (cold psychological explanation of why we suffer)",
    "Minimalist and sharp (use only very short sentences, military style)",
    "Gentle, empathetic but extremely firm on boundaries",
    "Lucid cynicism (gently mock modern society's illusions)",
    "Violent self-criticism (the narrator accuses themselves without making excuses)",
    "Shameful confession (say something you never admit)",
    "Point of view of the 'villain' (assume the toxic role and explain it)",
    "Post-breakup lucidity (speak like someone who understood everything too late)",
    "Total disillusionment (nothing works as planned, fatalistic tone)",
    "Assumed manipulator (explain how to manipulate without morality)",
    "Victim awakening (brutal awakening of awareness)",
    "Cold outside perspective (observe as if it's a scientific experiment)",
    "Realistic paranoia (everyone plays a role, nothing is innocent)",
    "Nihilistic minimalism (almost no hope, ultra dry sentences)",
    "Fragmented storytelling (scattered thoughts but emotionally coherent)",
    "Future projection (describe what will happen to you if you continue)",
    "Emotional flashback (speak as if you're reliving a specific scene)",
    "Letter never sent (to an ex, a friend, yourself)",
    "Internal dialogue (you vs yourself)",
    "Cold analysis of a past mistake",
    "Clinical tone (like a medical diagnosis)",
    "Voluntary dramatic exaggeration (almost theatrical but credible)",
    "Resigned tone (no more energy to fight)",
    "Passive-aggressive irony",
    "Darwinian view of relationships (survival, domination, selection)",
    "Prophetic tone (as if announcing a universal truth)",
    "Total detachment (no emotional involvement)",
    "Silent regret (say little but heavy)",
    "Social observation (like a sociologist of modern relationships)"
]

hooks_en = [
    "Start directly with the text",
    "Ask a very uncomfortable psychological question",
    "Immediately destroy a popular belief about personal development",
    "Address a silent and very specific pain directly ('If you hide this...')",
    "Start with 'You were lied to about...' followed by a fundamental concept",
    "Make a deliberately divisive statement that bruises the ego",
    "Describe a hyper-specific toxic situation where the audience will recognize themselves 100%",
    "Use reverse psychology ('Skip this video if you love your mental comfort')",
    "Reveal the true hidden meaning of a banal human behavior",
    "Start with the tragic consequence before explaining the cause ('Here's how you end up alone...')",
    "Challenge the viewer from the first second ('You're not ready to hear this')",
    "Give a life rule in the form of a universal and implacable law",
    "A cold and emotionless statement about human nature",
    "Start with 'No one's going to tell you this but...'",
    "Start with 'The problem isn't them. It's you.'",
    "Start with a truth that hurts immediately",
    "Say something the majority refuses to admit",
    "Start with 'You're making this mistake without realizing it'",
    "Start with a direct scene ('You're there, looking at your phone...')",
    "Create immediate discomfort ('You already know this concerns you')",
    "Start with 'If this hurts, it's because it's true'",
    "Start with a contradictory sentence ('The more you love, the more you lose')",
    "Hook as a revelation ('Here's what no one explains to you about...')",
    "Start with a direct accusation ('You're lying. To yourself.')",
    "Start with 'Stop doing this right now'",
    "Fatalistic hook ('It always ends like this')",
    "Start with a consequence ('You'll end up alone if...')",
    "Create a mirror effect ('Look at your relationships closely...')",
    "Start with a made-up but credible statistic",
    "Start with 'The day you understand this, everything changes'",
    "Hook as a secret ('I probably shouldn't say this but...')",
    "Start with an ultra-short punchline",
    "Hook as a comparison ('Strong people do this. Others...')",
    "Create a sense of urgency ('If you see this now...')",
    "Start with a rule ('Rule number 1: ...')",
    "Hook as observation ('You'll notice something...')",
    "Start with a human contradiction ('We say we want love, but...')",
    "Hook as a challenge ('Watch until the end if you're honest')"
]

system_instruction_en = "You are an AI assistant specialized in writing compelling short video scripts. You strictly adhere to tone, style, and length constraints"

consignes_default_en = ""

consignes_oogway_en = ""

consignes_joker_en = """
SPECIAL RULES FOR VOCAL RHYTHM (CHARACTER: DARK/JOKER):
This script will be read by a voice AI. The character is cynical, unpredictable and theatrical. The delivery must be CHAOTIC and sharp.
1. Abruptly alternate between long sentences without punctuation (to simulate manic fast delivery) and isolated words ending with a period (for brutal cuts).
2. Use many provocative rhetorical questions (?).
3. Add cynical starters at the beginning of sentences (e.g., "Ah...", "Hmm...", "Really?") to force the TTS to take a sarcastic tone.
4. Use ellipses (...) only to create unhealthy expectations before a brutal truth.
"""

# =====================================================================
# SELECT LANGUAGE
# =====================================================================

if LANGUAGE == "en":
    themes = themes_en
    angles = angles_en
    hooks = hooks_en
    system_instruction = system_instruction_en
    consignes_default = consignes_default_en
    consignes_oogway = consignes_oogway_en
    consignes_joker = consignes_joker_en
else:  # Default to French
    themes = themes_fr
    angles = angles_fr
    hooks = hooks_fr
    system_instruction = system_instruction_fr
    consignes_default = consignes_default_fr
    consignes_oogway = consignes_oogway_fr
    consignes_joker = consignes_joker_fr

# =====================================================================
# RANDOM SELECTION FOR THIS GENERATION
# =====================================================================

theme_choisi = random.choice(themes)
angle_choisi = random.choice(angles)
hook_choisi = random.choice(hooks)

# Fixed parameters (data already loaded above for language)
nombre_scripts = data["scriptNumber"]
wordNumber = data["wordNumber"] 
template = data["template"]
input_prompt = data["createScriptFromInput"]

# Read video transcription
if is_from_link:
    with open(f"{INTERMEDIAR_VIDEOS_CAPTIONER_PATH}/video.json", 'r') as f:
        caption = json.load(f)
else:
    caption = [{'text': ''}]
    
word_list = [elm['text'] for elm in caption ]
transcription = ' '.join(word_list) 

consignes_personnage = consignes_default if template == "default" else (consignes_oogway if template == "oogway" else consignes_joker)

# =====================================================================
# PROMPT 1: GENERATION BASED ON A THEME
# =====================================================================

if LANGUAGE == "en":
    prompt_theme = f"""You are an expert in creating compelling and psychological TikTok content.
Your mission: Write {nombre_scripts} original script(s) ready to be recorded.

SCRIPT PARAMETERS:
- Target duration per script: approximately {wordNumber} words.
- Central theme: {input_prompt}.
- Tone / Angle: {angle_choisi}.
- Hook type: {hook_choisi}.

{consignes_personnage}

STRICT RULES:
1. No personal development clichés (Forbidden: "get out of your comfort zone", "never give up", "believe in yourself").
2. Use raw, authentic and conversational vocabulary.
3. Make short and punchy sentences.
4. Don't put complex stage directions, just the text to be spoken.

Clearly separate each generated script with --, place no words outside the script between the --, respect the number of scripts which is {nombre_scripts} and put the scripts in quotes. If you must put quotes in a script use single quotes.' """
else:
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

Sépare clairement chaque script généré avec --, ne place aucun mot en dehors du script entres les --, respecte le nombre de script qui est de {nombre_scripts} et mets les scripts entre guillemets. Et si tu dois mettres des guillements dans un script utilise "'" """

# =====================================================================
# PROMPT 2: GENERATION BASED ON AN EXISTING SCRIPT (THE EXAMPLE)
# =====================================================================

if LANGUAGE == "en":
    prompt_exemple = f"""You are an expert in creating compelling TikTok content.
Here is a video script that went viral (Reference script):
{transcription}

Your mission: Write {nombre_scripts} NEW script(s) of {wordNumber} words.
You must keep EXACTLY the same overall atmosphere, the same rhythm and the same underlying theme as the reference script, BUT you must apply these new constraints:

NEW PARAMETERS:
- Tone / Angle: {angle_choisi}.
- Hook type: {hook_choisi}.

{consignes_personnage}

STRICT RULES:
1. Don't copy/paste any sentence from the reference script. Be inspired by its emotional "vibe" and impact format.
2. Formulate completely new concepts around the same subject.
3. Stay raw and without clichés. Short sentences.

Clearly separate each generated script with --, respect the number of scripts which is {nombre_scripts} and put the scripts in quotes."""
else:
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

Sépare clairement chaque script généré avec --, respecte le nombre de script qui est de {nombre_scripts} et mets les scripts entre guillemets."""

prompts_dico = {
    "default": [prompt_exemple, prompt_theme],
    "oogway": [prompt_exemple, prompt_theme],
    "joker": [prompt_exemple, prompt_theme],
}

if LANGUAGE == "en":
    print("PROMPT SELECTED READY FOR API:\n")
    ai_response_label = "AI Response\n"
else:
    print("PROMPT SÉLECTIONNÉ PRÊT POUR L'API :\n")
    ai_response_label = "Réponse de l'IA\n"

prompt_select = prompts_dico[template][0] if (data["createScriptFromLink"] == True) else prompts_dico[template][1]
print(prompt_select)


reponse = client.models.generate_content(
    model=SCRIPT_CREATOR_MODEL,
    contents=prompt_select,
    config=types.GenerateContentConfig(
        system_instruction=system_instruction)
)

print(ai_response_label)
scripts = extract_scripts_from_response(reponse.text)
            

print(reponse.text)
print(scripts)

with open(f"{ORIGINAL_CONTENT_SCRIPTS_FOLDER_PATH}/{template}-{LANGUAGE}-scripts.txt", 'a') as script_file:
    for script in scripts:
        cleaned_script = script.replace('"', '').replace('\n', ' ').strip()
        if cleaned_script and cleaned_script not in ("[]", "[ ]"):
            script_file.write(cleaned_script + "\n")

