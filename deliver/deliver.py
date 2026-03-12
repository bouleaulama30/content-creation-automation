import requests as r
import os
import dotenv
import json
from google import genai

dotenv.load_dotenv()

TOKEN = os.getenv('TOKEN')

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

client = genai.Client()

chat_id = "7921150744"


with open('/home/leo/content-creation-automation/captioner/public/video.json', 'r') as f:
    caption = json.load(f)
word_list = [elm['text'] for elm in caption ]
transcription = ' '.join(word_list) 

prompt = f"""Tu es un assistant spécialisé dans la création de métadonnées pour Reels Instagram.
### DONNÉES D'ENTRÉE :
1. Transcription du Reel : "{transcription}"
2. Pool de Hashtags : [alone, depression, amour, douleur, mental, réussite, solitude, vie, espoir]

### INSTRUCTIONS :
1. Extrais la toute première phrase de la transcription pour l'utiliser comme description.
2. Sélectionne les 2 hashtags les plus pertinents dans le pool fourni.
3. Ta réponse doit être UNIQUEMENT sans texte avant ou après.

### FORMAT DE SORTIE ATTENDU SANS COMMENCE:
La première phrase ici ! #hashtag1 #hastag2"""

reponse = client.models.generate_content(
    model="gemma-3-27b-it",
    contents=prompt,
)
inter_reponse = reponse.text.replace("\n", "")
inter_reponse = inter_reponse.replace(".", "!")

final_description = inter_reponse + " #motivation #citation #inspiration"

print(final_description)
# send txt
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
data = {'chat_id' : chat_id, 'text' : final_description} 
status_txt = r.get(url, data=data).json

# # send photo
# files = {'photo': open("/home/leo/content-creation-automation/assembler/public/logo.png", 'rb')}
# status_photo = r.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={chat_id}", files=files)

# send video
files = {'video': open("/home/leo/content-creation-automation/captioner/out/video.mp4", 'rb')}
status_video = r.post(f"https://api.telegram.org/bot{TOKEN}/sendVideo?chat_id={chat_id}", files=files)

print(status_txt)
# print(status_photo)
print(status_video)