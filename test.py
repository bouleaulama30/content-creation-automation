import json
import os
from typing import TypedDict, List
import math
import random as rd

# L'équivalent de ton "type" ou "interface" en TypeScript
class VideoToEmbed(TypedDict):
    durationInFrames: int
    src: str

# L'équivalent de ton export let selectedVideos: VideoToEmbed[] = []
selected_videos: List[VideoToEmbed] = []

def file_exists(path: str):
    """Vérifie si un fichier existe à l'emplacement donné."""
    return os.path.exists(path)

def select_videos():
    indice = 0
    videos: List[VideoToEmbed] = []

    # On boucle tant que le fichier existe
    while file_exists(f"./public/video{indice}.mp4"):
        # print(f"la video{indice} existe !")
        
        # videos.append({
        #     "durationInFrames": math.floor(1 * 30), # ou juste int(1 * 30)
        #     "src": f"video{indice}.mp4"
        # })
        indice += 1

    for _ in range(indice):
        random = rd.randint(0, indice-1)
        videos.append({
            "durationInFrames": math.floor(1 * 30), # ou juste int(1 * 30)
            "src": f"video{random}.mp4"
        })

    return videos


if __name__ == "__main__":
    result = select_videos()
    with open('props.json', 'w') as f:
        json.dump({"videosSrc": result}, f)
    print(result)