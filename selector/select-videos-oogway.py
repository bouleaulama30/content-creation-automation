import json
import os
import math
from typing import TypedDict, List
import shutil
import random as rd
from pathlib import Path
from mutagen.mp3 import MP3
import subprocess
from dotenv import load_dotenv

load_dotenv()

PIECE_VIDEO_TRANSI_DURATION = float(os.getenv('PIECE_VIDEO_TRANSI_DURATION'))
NBR_BEGIN_OOGWAY_VIDEO = int(os.getenv('NBR_BEGIN_OOGWAY_VIDEO'))
FPS = int(os.getenv('FPS'))

VIDEOS_SRC_OOGWAY_PATH = os.getenv('VIDEOS_SRC_OOGWAY_PATH')
VIDEOS_SRC_TRANSI_PATH = os.getenv('VIDEOS_SRC_TRANSI_PATH')
AUDIO_SRC_FOLDER_PATH = os.getenv('AUDIO_SRC_FOLDER_PATH')
AUDIO_NAME = os.getenv('AUDIO_NAME')
AUDIO_SRC_FILE_PATH= os.getenv('AUDIO_SRC_FILE_PATH')


PROJECT_BASE_PATH = os.getenv('PROJECT_BASE_PATH')
ASSEMBLER_PATH = os.getenv('ASSEMBLER_PATH')
CAPTIONER_PATH = os.getenv('CAPTIONER_PATH')

INTERMEDIAR_VIDEOS_PATH = os.getenv('INTERMEDIAR_VIDEOS_PATH')


# L'équivalent de ton "type" ou "interface" en TypeScript
class VideoToEmbed(TypedDict):
    durationInFrames: int
    src: str

# L'équivalent de ton export let selectedVideos: VideoToEmbed[] = []
selected_videos: List[VideoToEmbed] = []

def get_video_duration(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

def get_audio_duration(audio_path):
    audio = MP3(audio_path)
    audioDuration = audio.info.length
    return audioDuration

def nbr_video_to_select(audio_path, duration_per_video):
    audio = MP3(audio_path)
    audioDuration = audio.info.length
    return int(audioDuration/duration_per_video + 1)



def select_oogway_videos(video_path_oogway, video_path_transi, duration_transi_videos, nbr_begin_oogway_video, audio_path): 
    # sélection random des videos d'oogway
    oogway_videos = os.listdir(video_path_oogway)
    oogway_videos = [f for f in oogway_videos if os.path.isfile(video_path_oogway+'/'+f)]
    rd.shuffle(oogway_videos)

    # sélection random des videos de transi
    transi_videos = os.listdir(video_path_transi)
    transi_videos = [f for f in transi_videos if os.path.isfile(video_path_transi+'/'+f)]
    rd.shuffle(transi_videos)

    # pattern (nbr_begin_oogway_video, video transi, video oogway, video transi etc...)
    audio_duration = get_audio_duration(audio_path)
    total_duration = 0
    selected_videos = []
    # début du pattern
    for _ in range(nbr_begin_oogway_video):
        if(total_duration < audio_duration):
            oogway_video = oogway_videos.pop()
            oogway_video_duration = get_video_duration(f"{video_path_oogway}/{oogway_video}") 
            total_duration += oogway_video_duration 
            selected_videos.append((oogway_video, oogway_video_duration, False))

    # suite du pattern
    is_transi_video = True
    while(total_duration < audio_duration):
        if(is_transi_video):
            transi_video = transi_videos.pop()
            transi_video_duration = duration_transi_videos
            total_duration += transi_video_duration 
            selected_videos.append((transi_video, transi_video_duration, is_transi_video))
            is_transi_video =  False
        else:
            oogway_video = oogway_videos.pop()
            oogway_video_duration = get_video_duration(f"{video_path_oogway}/{oogway_video}") 
            total_duration += oogway_video_duration 
            selected_videos.append((oogway_video, oogway_video_duration, is_transi_video))
            is_transi_video =  True

    
    print(selected_videos, sep="\n")
    return selected_videos

     
def move_selected_videos(video_path_oogway, video_path_transi, folder_video_dst_path, selected_videos):
    for idx, (video_src_name, _, is_transi_video) in enumerate(selected_videos):
        print(f"{idx}, {video_src_name}")
        if (is_transi_video):
            copy_video(video_path_transi, folder_video_dst_path, video_src_name)
        else:
            copy_video(video_path_oogway, folder_video_dst_path, video_src_name)
     
def copy_video(src_path, dst_path, src_name):
	# Copy the file
	shutil.copy(f"{src_path}/{src_name}", dst_path)

def copy_and_rename_audio(src_path, dst_path, src_name, dst_name):
	# Copy the file
	shutil.copy(f"{src_path}/{src_name}", dst_path)

	# Rename the copied file
	new_name = f"{dst_path}/{dst_name}"
	shutil.move(f"{dst_path}/{src_name}", new_name)

def file_exists(path: str):
    """Vérifie si un fichier existe à l'emplacement donné."""
    return os.path.exists(path)

def write_data_json(selected_videos):
    videos: List[VideoToEmbed] = []
    # On boucle tant que le fichier existe
        # print(f"la video{idx} existe !")
    for (video_src_name, video_duration, _) in selected_videos: 
        # ffprobe retourne une durée en secondes, Remotion attend des frames.
        duration_in_frames = max(1, math.floor(video_duration * FPS))
        videos.append({
            # pour avoir 4 plan toute les 10 sec
            "durationInFrames": duration_in_frames,
            "src": video_src_name
        })

    with open(f"{ASSEMBLER_PATH}/props.json", 'w') as f:
        json.dump({"videosSrc": videos}, f)
        print(videos)


if __name__ == "__main__":
    # print(f"{AUDIO_NAME}, {AUDIO_SRC_FILE_PATH}")
    duration = get_video_duration(f"{VIDEOS_SRC_OOGWAY_PATH}/oogway1.mp4")
    videos = select_oogway_videos(f"{VIDEOS_SRC_OOGWAY_PATH}", f"{VIDEOS_SRC_TRANSI_PATH}", PIECE_VIDEO_TRANSI_DURATION, NBR_BEGIN_OOGWAY_VIDEO, f"{AUDIO_SRC_FILE_PATH}")
    move_selected_videos(f"{VIDEOS_SRC_OOGWAY_PATH}", f"{VIDEOS_SRC_TRANSI_PATH}", f"{INTERMEDIAR_VIDEOS_PATH}", videos)
    copy_and_rename_audio(f"{AUDIO_SRC_FOLDER_PATH}", f"{INTERMEDIAR_VIDEOS_PATH}",f"{AUDIO_NAME}", f"{AUDIO_NAME}")
    write_data_json(videos)
    # print(videos)
