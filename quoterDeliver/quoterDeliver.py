import requests as r
import os
import dotenv
import random as rd
from PIL import Image, ImageDraw, ImageFont

dotenv.load_dotenv()

INTERMEDIAR_VIDEOS_CAPTIONER_PATH = os.getenv('INTERMEDIAR_VIDEOS_CAPTIONER_PATH')
PRODUCTION_FOLDER_PATH = os.getenv('PRODUCTION_FOLDER_PATH')
THUMBNAIL_FILE_PATH = os.getenv('THUMBNAIL_FILE_PATH')
DATA_CLIENT_FILE = os.getenv('DATA_CLIENT_FILE')
DELIVER_PATH = os.getenv('DELIVER_PATH')
ORIGINAL_CONTENT_QUOTES_FILE_PATH = os.getenv('ORIGINAL_CONTENT_QUOTES_FILE_PATH')

TOKEN = os.getenv('TOKEN')
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

    font_size = 80
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

with open(f"{ORIGINAL_CONTENT_QUOTES_FILE_PATH}", 'r') as f:
    quotes = f.readlines()
    rd.shuffle(quotes)

template = ["default", "joker", "oogway"]
rd.shuffle(template)

generer_image(quotes[0], THUMBNAIL_FILE_PATH, template[0])

# send photo
files = {'photo': open(f"{THUMBNAIL_FILE_PATH}", 'rb')}
status_photo = r.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={chat_id}", files=files)


print(status_photo)
