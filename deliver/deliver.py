import requests as r
import os
import dotenv
import json
from google import genai
from PIL import Image, ImageDraw, ImageFont

dotenv.load_dotenv()

INTERMEDIAR_VIDEOS_CAPTIONER_PATH = os.getenv('INTERMEDIAR_VIDEOS_CAPTIONER_PATH')
PRODUCTION_FOLDER_PATH = os.getenv('PRODUCTION_FOLDER_PATH')
THUMBNAIL_FILE_PATH = os.getenv('THUMBNAIL_FILE_PATH')
DATA_CLIENT_FILE = os.getenv('DATA_CLIENT_FILE')
DELIVER_PATH = os.getenv('DELIVER_PATH')

TOKEN = os.getenv('TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

client = genai.Client()

chat_id = "7921150744"


def _wrap_text_to_width(draw, text, font, max_width, stroke_width=0):
    words = text.split()
    if not words:
        return [""]

    # Ajouter la largeur du stroke aux deux côtés
    adjusted_max_width = max_width - 2 * stroke_width
    
    lines = []
    current_line = words[0]

    for word in words[1:]:
        test_line = f"{current_line} {word}"
        # Utilisation de textbbox pour une précision maximale au pixel près
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if (bbox[2] - bbox[0]) <= adjusted_max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)

    # Si un mot est encore trop long (très grand mot sur petit écran), on coupe par lettre
    final_lines = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        if (bbox[2] - bbox[0]) <= adjusted_max_width:
            final_lines.append(line)
            continue

        chunk = ""
        for char in line:
            test_chunk = chunk + char
            bbox_chunk = draw.textbbox((0, 0), test_chunk, font=font)
            if (bbox_chunk[2] - bbox_chunk[0]) <= adjusted_max_width or not chunk:
                chunk = test_chunk
            else:
                final_lines.append(chunk)
                chunk = char
        if chunk:
            final_lines.append(chunk)

    return final_lines

def generer_image(texte_variable, destination, template):
    # 1. Charger l'image de base
    img = Image.open(f"{DELIVER_PATH}/{template}.png")
    draw = ImageDraw.Draw(img)
    
    # 2. Définir la police
    font_path = f"{INTERMEDIAR_VIDEOS_CAPTIONER_PATH}/Lora-SemiBold.ttf"
    
    # 3. Obtenir les dimensions de l'image
    img_width, img_height = img.size

    # 4. Contraintes d'affichage pour éviter tout dépassement
    margin_x = int(img_width * 0.10) 
    margin_y = int(img_height * 0.08)
    max_text_width = max(50, img_width - 2 * margin_x)
    max_text_height = max(50, img_height - 2 * margin_y)

    texte_variable = " ".join(texte_variable.split()).upper()
    
    if not texte_variable:
        img.save(destination)
        return

    font_size = 100
    min_font_size = 20
    stroke_width = 3

    while True:
        font = ImageFont.truetype(font_path, font_size)
        lines = _wrap_text_to_width(draw, texte_variable, font, max_text_width, stroke_width)

        line_heights = []
        max_line_width = 0
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_w = bbox[2] - bbox[0] + 2 * stroke_width
            line_h = bbox[3] - bbox[1] + 2 * stroke_width
            max_line_width = max(max_line_width, line_w)
            line_heights.append(line_h)

        line_spacing = int(font_size * 0.2)
        # Correction mineure : éviter un espacement en trop si le texte ne fait qu'une ligne
        text_block_height = sum(line_heights) + line_spacing * max(0, len(lines) - 1)

        fits = max_line_width <= max_text_width and text_block_height <= max_text_height
        if fits or font_size <= min_font_size:
            break
        font_size -= 2

    # 5. Dessiner le bloc de texte centré dans la zone utile
    y = (img_height - text_block_height) // 2
    for idx, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        line_w = bbox[2] - bbox[0] + 2 * stroke_width
        line_h = bbox[3] - bbox[1] + 2 * stroke_width
        x = (img_width - line_w) // 2
        
        # Le texte est déjà en majuscules, plus besoin de .upper() ici
        draw.text((x, y), line, fill="yellow", font=font, stroke_width=stroke_width, stroke_fill="black")
        y += line_h + line_spacing
    
    # 6. Sauvegarder le résultat
    img.save(destination)

with open(f"{INTERMEDIAR_VIDEOS_CAPTIONER_PATH}/video.json", 'r') as f:
    caption = json.load(f)
word_list = [elm['text'] for elm in caption ]
transcription = ' '.join(word_list) 

prompt_fr = f"""Tu es un assistant spécialisé dans la création de métadonnées pour Reels Instagram.
### DONNÉES D'ENTRÉE :
1. Transcription du Reel : "{transcription}"
2. Pool de Hashtags : [alone, depression, amour, douleur, mental, réussite, solitude, vie, espoir, conseil, verite, foi, dieu, plan, inspirationfr, sagesse, humour, mentalité, Short, vivre]

### INSTRUCTIONS :
1. Extrais la toute première phrase de la transcription pour l'utiliser comme description.
2. Sélectionne les 2 hashtags les plus pertinents dans le pool fourni.
3. Ta réponse doit être UNIQUEMENT sans texte avant ou après et en français.

### FORMAT DE SORTIE ATTENDU SANS COMMENCE:
La première phrase ici ! #hashtag1 #hastag2"""

prompt_en = f"""You are an assistant specialized in creating metadata for Instagram Reels.
### INPUT DATA:
1. Reel transcription: "{transcription}"
2. Hashtag pool: [joker, oogway, alone, depression, love, pain, mindset, success, solitude, life, hope, advice, truth, faith, god, plan, inspiration, wisdom, humor, mentality, short, living]

### INSTRUCTIONS:
1. Extract the very first sentence of the transcription to use as the description.
2. Select the 2 most relevant hashtags from the provided pool.
3. Your response must be ONLY the output, with no text before or after and in english.

### EXPECTED OUTPUT FORMAT WITHOUT PREFIX:
The first sentence here! #hashtag1 #hashtag2"""


prompt_thumnail_fr = f"""Tu es un expert en copywriting et en psychologie de l'attention sur TikTok, spécialisé dans la niche de la motivation, de la résilience et de la philosophie.

Voici le transcript exact d'une de mes prochaines vidéos :
"{transcription}"

Ta mission est de générer UNE SEULE proposition de texte ultra-court à écrire sur la miniature de cette vidéo pour maximiser le taux de clic (CTR).

Règles strictes à respecter :
1. Longueur : Entre 2 et 5 mots maximum. Le texte doit pouvoir être lu en une fraction de seconde.
2. Objectif : Créer un mystère, une urgence ou un choc émotionnel (Curiosity Gap). Ne résume pas bêtement le transcript, donne une raison irrépressible d'écouter la vidéo.
3. Ton : Direct, philosophique, parfois provocateur ou brutalement honnête.
4. Format de sortie : Renvoie UNIQUEMENT le texte généré, sans guillemets, sans ponctuation finale inutile et sans aucun mot avant ou après."""

prompt_thumnail_en = f"""You are an expert in copywriting and attention psychology on TikTok, specialized in the niche of motivation, resilience, and philosophy.

Here is the exact transcript of one of my upcoming videos:
"{transcription}"

Your mission is to generate ONE SINGLE ultra-short text suggestion to place on the thumbnail of this video to maximize click-through rate (CTR).

Strict rules to follow:
1. Length: Between 2 and 5 words maximum. The text must be readable in a fraction of a second.
2. Objective: Create mystery, urgency, or an emotional shock (Curiosity Gap). Do not simply summarize the transcript—give an irresistible reason to watch the video.
3. Tone: Direct, philosophical, sometimes provocative or brutally honest.
4. Output format: Return ONLY the generated text, without quotes, without unnecessary ending punctuation, and without any words before or after."""

with open(f"{DATA_CLIENT_FILE}", 'r') as json_data:
    data = json.load(json_data)
    template = data["template"]
    lang = data["LANG"]

print(lang)
reponse = client.models.generate_content(
    model="gemma-3-27b-it",
    contents=prompt_fr if lang == "fr" else prompt_en,
)
inter_reponse = reponse.text.replace("\n", "")
final_description = inter_reponse + " #motivation " + "#citation " + "#inspiration" if lang == "fr" else inter_reponse + " #motivation " + "#quote " + "#inspiration"
print(final_description)

reponse = client.models.generate_content(
    model="gemma-3-27b-it",
    contents=prompt_thumnail_fr if lang == "fr" else prompt_thumnail_en,
)
inter_reponse = reponse.text.replace(".", "")
final_txt_thumbnail = inter_reponse.replace("\n", "")

generer_image(final_txt_thumbnail, THUMBNAIL_FILE_PATH, template)

# send txt
url = f"http://localhost:8081/bot{TOKEN}"
data = {'chat_id' : chat_id, 'text' : final_description} 
status_txt = r.get(f"{url}/sendMessage", data=data).json

# send photo
files = {'photo': open(f"{THUMBNAIL_FILE_PATH}", 'rb')}
status_photo = r.post(f"{url}/sendPhoto?chat_id={chat_id}", files=files)

# send video
files = {'video': open(f"{PRODUCTION_FOLDER_PATH}/video.mp4", 'rb')}
status_video = r.post(f"{url}/sendVideo?chat_id={chat_id}", files=files)

print(status_txt)
print(status_photo)
print(status_video)