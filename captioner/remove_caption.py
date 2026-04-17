import json
from dotenv import load_dotenv
import os

load_dotenv()

INTERMEDIAR_VIDEOS_CAPTIONER_PATH = os.getenv('INTERMEDIAR_VIDEOS_CAPTIONER_PATH')


with open(f"{INTERMEDIAR_VIDEOS_CAPTIONER_PATH}/video.json", 'r', encoding='utf-8') as file:
    data = json.load(file)

remove_caption = data[:-1]

with open(f"{INTERMEDIAR_VIDEOS_CAPTIONER_PATH}/video.json", 'w', encoding='utf-8') as file:
    print(remove_caption)
    json.dump(remove_caption, file, indent=2, ensure_ascii=False)