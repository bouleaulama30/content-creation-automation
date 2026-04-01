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

def generer_image(texte_variable, destination, template):
    # 1. Charger l'image de base
    img = Image.open(f"{DELIVER_PATH}/{template}.png")
    draw = ImageDraw.Draw(img)
    
    # 2. Définir la police
    font = ImageFont.truetype(f"{INTERMEDIAR_VIDEOS_CAPTIONER_PATH}/Cinzel-SemiBold.ttf", 100)
    
    # 3. Obtenir les dimensions de l'image et du texte
    img_width, img_height = img.size
    bbox = draw.textbbox((0, 0), texte_variable, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # 4. Calculer la position centrale
    x = (img_width - text_width) // 2
    y = (img_height - text_height) // 2
    
    # 5. Ajouter le texte centré
    draw.text((x, y), texte_variable, fill="white", font=font)
    
    # 6. Sauvegarder le résultat
    img.save(destination)

with open(f"{INTERMEDIAR_VIDEOS_CAPTIONER_PATH}/video.json", 'r') as f:
    caption = json.load(f)
word_list = [elm['text'] for elm in caption ]
transcription = ' '.join(word_list) 

prompt = f"""Tu es un assistant spécialisé dans la création de métadonnées pour Reels Instagram.
### DONNÉES D'ENTRÉE :
1. Transcription du Reel : "{transcription}"
2. Pool de Hashtags : [alone, depression, amour, douleur, mental, réussite, solitude, vie, espoir, conseil, verite]

### INSTRUCTIONS :
1. Extrais la toute première phrase de la transcription pour l'utiliser comme description.
2. Sélectionne les 2 hashtags les plus pertinents dans le pool fourni.
3. Ta réponse doit être UNIQUEMENT sans texte avant ou après.

### FORMAT DE SORTIE ATTENDU SANS COMMENCE:
La première phrase ici ! #hashtag1 #hastag2"""

prompt_thumnail = f"""Tu es un expert en copywriting et en psychologie de l'attention sur TikTok, spécialisé dans la niche de la motivation, de la résilience et de la philosophie.

Voici le transcript exact d'une de mes prochaines vidéos :
"{transcription}"

Ta mission est de générer UNE SEULE proposition de texte ultra-court à écrire sur la miniature de cette vidéo pour maximiser le taux de clic (CTR).

Règles strictes à respecter :
1. Longueur : Entre 2 et 5 mots maximum. Le texte doit pouvoir être lu en une fraction de seconde.
2. Objectif : Créer un mystère, une urgence ou un choc émotionnel (Curiosity Gap). Ne résume pas bêtement le transcript, donne une raison irrépressible d'écouter la vidéo.
3. Ton : Direct, philosophique, parfois provocateur ou brutalement honnête.
4. Format de sortie : Renvoie UNIQUEMENT le texte généré, sans guillemets, sans ponctuation finale inutile et sans aucun mot avant ou après."""

reponse = client.models.generate_content(
    model="gemma-3-27b-it",
    contents=prompt,
)
inter_reponse = reponse.text.replace("\n", "")
inter_reponse = inter_reponse.replace(".", "!")

final_description = inter_reponse + " #motivation #citation #inspiration"
print(final_description)

reponse = client.models.generate_content(
    model="gemma-3-27b-it",
    contents=prompt_thumnail,
)
final_txt_thumbnail = reponse.text.replace("\n", "")
with open(f"{DATA_CLIENT_FILE}", 'r') as json_data:
    data = json.load(json_data)
    template = data["template"]

generer_image(final_txt_thumbnail, THUMBNAIL_FILE_PATH, template)

# send txt
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
data = {'chat_id' : chat_id, 'text' : final_description} 
status_txt = r.get(url, data=data).json

# send photo
files = {'photo': open(f"{THUMBNAIL_FILE_PATH}", 'rb')}
status_photo = r.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={chat_id}", files=files)

# send video
files = {'video': open(f"{PRODUCTION_FOLDER_PATH}/video.mp4", 'rb')}
status_video = r.post(f"https://api.telegram.org/bot{TOKEN}/sendVideo?chat_id={chat_id}", files=files)

print(status_txt)
print(status_photo)
print(status_video)