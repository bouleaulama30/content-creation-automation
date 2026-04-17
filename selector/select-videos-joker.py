import json
import os
import math
from typing import TypedDict, List
import shutil
import random as rd
from mutagen.mp3 import MP3
import subprocess
from dotenv import load_dotenv

load_dotenv()

PIECE_VIDEO_TRANSI_DURATION = float(os.getenv('PIECE_VIDEO_TRANSI_DURATION'))
PIECE_VIDEO_DURATION = float(os.getenv('PIECE_VIDEO_DURATION'))
NBR_BEGIN_JOKER_VIDEO = int(os.getenv('NBR_BEGIN_JOKER_VIDEO', os.getenv('NBR_BEGIN_OOGWAY_VIDEO', '2')))
FPS = int(os.getenv('FPS'))

VIDEOS_SRC_JOKER_PATH = os.getenv('VIDEOS_SRC_JOKER_PATH')
VIDEOS_SRC_TRANSI_PATH = os.getenv('VIDEOS_SRC_TRANSI_PATH')
VIDEOS_SRC_OUTRO_FOLDER_PATH = os.getenv('VIDEOS_SRC_OUTRO_FOLDER_PATH')
VIDEOS_SRC_OUTRO_FILE_NAME = os.getenv('VIDEOS_SRC_OUTRO_FILE_NAME')

AUDIO_FOLDER_PATH = os.getenv('AUDIO_FOLDER_PATH')
AUDIO_NAME = os.getenv('AUDIO_NAME')
AUDIO_FILE_PATH = os.getenv('AUDIO_FILE_PATH')

ORIGINAL_CONTENT_MUSIQUES_JOKER_FOLDER_PATH = os.getenv('ORIGINAL_CONTENT_MUSIQUES_JOKER_FOLDER_PATH')
ORIGINAL_CONTENT_MUSIQUE_NAME = os.getenv('ORIGINAL_CONTENT_MUSIQUE_NAME')
DATA_CLIENT_FILE = os.getenv('DATA_CLIENT_FILE')
VOLUME_MUSIQUE = float(os.getenv('VOLUME_MUSIQUE'))

ASSEMBLER_PATH = os.getenv('ASSEMBLER_PATH')
INTERMEDIAR_VIDEOS_ASSEMBLER_PATH = os.getenv('INTERMEDIAR_VIDEOS_ASSEMBLER_PATH')

OPENING_LIST_JOKER_VIDEO = [line.strip() for line in open('joker_list_opening.txt')]
print(OPENING_LIST_JOKER_VIDEO)


class VideoToEmbed(TypedDict):
    durationInFrames: int
    src: str


selected_videos: List[VideoToEmbed] = []


def get_video_duration(filename):
    result = subprocess.run(
        [
            'ffprobe',
            '-v',
            'error',
            '-show_entries',
            'format=duration',
            '-of',
            'default=noprint_wrappers=1:nokey=1',
            filename,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return float(result.stdout)


def get_audio_duration(audio_path):
    audio = MP3(audio_path)
    audio_duration = audio.info.length
    return audio_duration


def select_musique(musiques_path):
    files = os.listdir(musiques_path)
    files = [f for f in files if os.path.isfile(musiques_path + '/' + f)]
    rd.shuffle(files)
    print(files[0], sep='\n')
    return files[0]


def select_joker_videos(video_path_joker, video_path_transi, duration_transi_videos, nbr_begin_joker_video, audio_path):


    joker_videos = os.listdir(video_path_joker)
    joker_videos = [f for f in joker_videos if os.path.isfile(video_path_joker + '/' + f)]
    rd.shuffle(joker_videos)

    joker_opening_videos = OPENING_LIST_JOKER_VIDEO.copy()
    rd.shuffle(joker_opening_videos)

    transi_videos = os.listdir(video_path_transi)
    transi_videos = [f for f in transi_videos if os.path.isfile(video_path_transi + '/' + f)]
    rd.shuffle(transi_videos)

    audio_duration = get_audio_duration(audio_path)
    total_duration = 0
    selected_videos = []

    for _ in range(nbr_begin_joker_video):
        if total_duration < audio_duration:
            joker_video = joker_opening_videos.pop()
            joker_video_duration = get_video_duration(f'{video_path_joker}/{joker_video}')
            if total_duration + joker_video_duration > audio_duration:
                selected_videos.append((joker_video, audio_duration - total_duration, False))
                total_duration += joker_video_duration
                break
            total_duration += joker_video_duration
            selected_videos.append((joker_video, joker_video_duration, False))

    is_transi_video = True
    while total_duration < audio_duration:
        if is_transi_video:
            transi_video = transi_videos.pop()
            transi_video_duration = duration_transi_videos
            if total_duration + transi_video_duration > audio_duration:
                selected_videos.append((transi_video, audio_duration - total_duration, is_transi_video))
                break
            total_duration += transi_video_duration
            selected_videos.append((transi_video, transi_video_duration, is_transi_video))
            is_transi_video = False
        else:
            joker_video = joker_videos.pop()
            joker_video_duration = get_video_duration(f'{video_path_joker}/{joker_video}')
            if total_duration + joker_video_duration > audio_duration:
                selected_videos.append((joker_video, audio_duration - total_duration, is_transi_video))
                break
            total_duration += joker_video_duration
            selected_videos.append((joker_video, joker_video_duration, is_transi_video))
            is_transi_video = True

    selected_videos.append((VIDEOS_SRC_OUTRO_FILE_NAME, PIECE_VIDEO_DURATION, False))
    print(selected_videos, sep='\n')
    return selected_videos


def move_selected_videos(video_path_joker, video_path_transi, folder_video_dst_path, selected_videos):
    for idx, (video_src_name, _, is_transi_video) in enumerate(selected_videos[:-1]):
        print(f'{idx}, {video_src_name}')
        if is_transi_video:
            copy_video(video_path_transi, folder_video_dst_path, video_src_name)
        else:
            copy_video(video_path_joker, folder_video_dst_path, video_src_name)

    copy_video(VIDEOS_SRC_OUTRO_FOLDER_PATH, folder_video_dst_path, VIDEOS_SRC_OUTRO_FILE_NAME)
    print(f'{len(selected_videos) - 1}, {VIDEOS_SRC_OUTRO_FILE_NAME}')


def copy_video(src_path, dst_path, src_name):
    shutil.copy(f'{src_path}/{src_name}', dst_path)


def copy_and_rename_audio(src_path, dst_path, src_name, dst_name):
    shutil.copy(f'{src_path}/{src_name}', dst_path)
    new_name = f'{dst_path}/{dst_name}'
    shutil.move(f'{dst_path}/{src_name}', new_name)


def write_data_json(selected_videos, is_original):
    videos: List[VideoToEmbed] = []
    props = {'videosSrc': []}

    for (video_src_name, video_duration, _) in selected_videos:
        duration_in_frames = max(1, math.floor(video_duration * FPS))
        videos.append(
            {
                'durationInFrames': duration_in_frames,
                'src': video_src_name,
            }
        )

    props['videosSrc'] = videos

    if is_original:
        props['audioSrc2Prop'] = {'src': f'{ORIGINAL_CONTENT_MUSIQUE_NAME}', 'volume': VOLUME_MUSIQUE}

    with open(f'{ASSEMBLER_PATH}/props.json', 'w') as f:
        json.dump(props, f)
    print(props)


if __name__ == '__main__':
    videos = select_joker_videos(
        f'{VIDEOS_SRC_JOKER_PATH}',
        f'{VIDEOS_SRC_TRANSI_PATH}',
        PIECE_VIDEO_TRANSI_DURATION,
        NBR_BEGIN_JOKER_VIDEO,
        f'{AUDIO_FILE_PATH}',
    )
    move_selected_videos(
        f'{VIDEOS_SRC_JOKER_PATH}',
        f'{VIDEOS_SRC_TRANSI_PATH}',
        f'{INTERMEDIAR_VIDEOS_ASSEMBLER_PATH}',
        videos,
    )
    copy_and_rename_audio(f'{AUDIO_FOLDER_PATH}', f'{INTERMEDIAR_VIDEOS_ASSEMBLER_PATH}', f'{AUDIO_NAME}', f'{AUDIO_NAME}')

    with open(f'{DATA_CLIENT_FILE}', 'r') as json_data:
        data = json.load(json_data)
        original = data['createOriginalContent']

    if original:
        musique = select_musique(ORIGINAL_CONTENT_MUSIQUES_JOKER_FOLDER_PATH)
        copy_and_rename_audio(
            f'{ORIGINAL_CONTENT_MUSIQUES_JOKER_FOLDER_PATH}',
            f'{INTERMEDIAR_VIDEOS_ASSEMBLER_PATH}',
            musique,
            ORIGINAL_CONTENT_MUSIQUE_NAME,
        )

    write_data_json(videos, original)
    print(videos)
