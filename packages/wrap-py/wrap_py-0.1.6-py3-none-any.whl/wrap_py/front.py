from wrap_py import settings
import pathlib

def make_data_folders():
    pathlib.Path(settings.SPRITE_TYPES_PATH).mkdir(parents=True, exist_ok=True)
    pathlib.Path(settings.BACKGROUNDS_PATH).mkdir(parents=True, exist_ok=True)
    pathlib.Path(settings.PICTURES_PATH).mkdir(parents=True, exist_ok=True)
    pathlib.Path(settings.SOUNDS_PATH).mkdir(parents=True, exist_ok=True)

def make_data_folders_alt():
    pathlib.Path(settings.SPRITE_TYPES_PATH_ALT).mkdir(parents=True, exist_ok=True)
    pathlib.Path(settings.BACKGROUNDS_PATH_ALT).mkdir(parents=True, exist_ok=True)
    pathlib.Path(settings.PICTURES_PATH_ALT).mkdir(parents=True, exist_ok=True)
    pathlib.Path(settings.SOUNDS_PATH_ALT).mkdir(parents=True, exist_ok=True)