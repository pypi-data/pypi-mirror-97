import os, sys

ENGINE_NAME="wrap_engine"

TRANSL_DOMAIN = "wrap_py"
PACK_SOURCE_FOLDER = os.path.split(__file__)[0]
TRANSLATIONS_FOLDER = os.path.join(PACK_SOURCE_FOLDER, "transl", "compiled")

RESOURCE_FOLDER = os.path.join(PACK_SOURCE_FOLDER, "res")
ICON_FILE = os.path.join(RESOURCE_FOLDER, "icon.png")

DATA_CATALOG_NAME = "wrap_py_catalog"

DATA_PATH = os.path.abspath( os.path.join(os.path.expanduser("~"), DATA_CATALOG_NAME) )
DATA_PATH_ALT = os.path.abspath(DATA_CATALOG_NAME)
DATA_DOWNLOAD_URL = "https://www.dropbox.com/sh/22gphub8unhhfhq/AABNuScUjnI23D63LbFPqehva?dl=0"

SPRITES_TYPES_SUBFOLDER="sprite_types"
BACKGROUNDS_SUBFOLDER="backgrounds"
PICTURES_SUBFOLDER="images"
SOUNDS_SUBFOLDER="sounds"


SPRITE_TYPES_PATH = os.path.join(DATA_PATH, SPRITES_TYPES_SUBFOLDER)
BACKGROUNDS_PATH = os.path.join(DATA_PATH, BACKGROUNDS_SUBFOLDER)
PICTURES_PATH = os.path.join(DATA_PATH, PICTURES_SUBFOLDER)
SOUNDS_PATH = os.path.join(DATA_PATH, SOUNDS_SUBFOLDER)

SPRITE_TYPES_PATH_ALT = os.path.join(DATA_PATH_ALT, SPRITES_TYPES_SUBFOLDER)
BACKGROUNDS_PATH_ALT = os.path.join(DATA_PATH_ALT, BACKGROUNDS_SUBFOLDER)
PICTURES_PATH_ALT = os.path.join(DATA_PATH_ALT, PICTURES_SUBFOLDER)
SOUNDS_PATH_ALT = os.path.join(DATA_PATH_ALT, SOUNDS_SUBFOLDER)