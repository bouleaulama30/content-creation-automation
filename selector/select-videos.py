import json
import os
import math
from typing import TypedDict, List
import shutil
import random as rd
from mutagen.mp3 import MP3


# L'équivalent de ton "type" ou "interface" en TypeScript
class VideoToEmbed(TypedDict):
    durationInFrames: int
    src: str

# L'équivalent de ton export let selectedVideos: VideoToEmbed[] = []
selected_videos: List[VideoToEmbed] = []


def nbr_video_to_select(audio_path, duration_per_video):
    audio = MP3(audio_path)
    audioDuration = audio.info.length
    return int(audioDuration/duration_per_video + 1)


def select_videos(video_path, nbr_video): 
    files = os.listdir(video_path)
    files = [f for f in files if os.path.isfile(video_path+'/'+f)]
    rd.shuffle(files)
    selected_videos = files[:nbr_video]
    print(selected_videos, sep="\n")
    return selected_videos

def copy_and_rename(src_path, dst_path, src_name, dst_name):
	# Copy the file
	shutil.copy(f"{src_path}/{src_name}", dst_path)

	# Rename the copied file
	new_name = f"{dst_path}/{dst_name}"
	shutil.move(f"{dst_path}/{src_name}", new_name)
     
def move_selected_videos(folder_video_src_path, folder_video_dst_path, selected_videos):
    for idx, video_name in enumerate(selected_videos):
        print(f"{idx}, {video_name}")
        copy_and_rename(folder_video_src_path, folder_video_dst_path, video_name, f"video{idx}.mp4")
     

def file_exists(path: str):
    """Vérifie si un fichier existe à l'emplacement donné."""
    return os.path.exists(path)

def write_data_json(folder_video_path):
    videos: List[VideoToEmbed] = []
    idx = 0
    # On boucle tant que le fichier existe
    while file_exists(f"{folder_video_path}/video{idx}.mp4"):
        # print(f"la video{idx} existe !")
        videos.append({
            # pour avoir 4 plan toute les 10 sec
            "durationInFrames": math.floor(2.5 * 30), 
            "src": f"video{idx}.mp4"
        })
        idx += 1

    with open('props.json', 'w') as f:
        json.dump({"videosSrc": videos}, f)
        print(videos)


if __name__ == "__main__":
    nbr_video = nbr_video_to_select('/home/leo/Videos/projet_secret/audio/audio.mp3', 2.5)
    copy_and_rename("/home/leo/Videos/projet_secret/audio/", "/home/leo/content-creation-automation/public","audio.mp3", "audio.mp3")
    videos = select_videos("/home/leo/Videos/projet_secret", nbr_video)
    move_selected_videos("/home/leo/Videos/projet_secret", "/home/leo/content-creation-automation/public", videos)
    write_data_json("/home/leo/content-creation-automation/public")
