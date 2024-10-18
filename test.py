import os

from utils.paths import audios_path

un_audio_json_path = [_.path for _ in os.scandir(audios_path) if _.is_dir()]
print(un_audio_json_path)