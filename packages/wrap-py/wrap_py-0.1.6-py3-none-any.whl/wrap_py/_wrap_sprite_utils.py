import time

from wrap_py import wrap_base
from wrap_py._transl import translator as _

__all__=["_get_sprite_by_id"]

def _get_sprite_by_id(id, check_type=None):
    sprite = wrap_base.sprite_id_manager.get_obj_by_id(id)
    if not sprite:
        err = _("No sprite with id {sprite_id}").format(sprite_id=id)
        raise Exception(err)

    if check_type is not None:
        if not isinstance(sprite, check_type):
            err = _("Sprite is not {sprite_type_name}").format(sprite_type_name=check_type.__name__)
            raise Exception(err)

    return sprite
