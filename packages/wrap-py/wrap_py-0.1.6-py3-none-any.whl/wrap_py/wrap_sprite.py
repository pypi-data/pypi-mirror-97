# prepare translator for module strings
from wrap_py._transl import translator as _

from wrap_engine.sprite_type_factory import Sprite_type_factory
from wrap_engine.sprite_of_type import Sprite_of_type
from wrap_engine.sprite_text import Sprite_text

from wrap_py import wrap_base, settings

from wrap_py import _wrap_sprite_utils as wsu


class wrap_sprite():
    @staticmethod
    def _register_sprite(sprite):
        id = wrap_base.sprite_id_manager.add_object(sprite)
        wrap_base.world.sprite_manager.add_image_sprite(sprite)
        return id

    @staticmethod
    def _prepare_sprite_type(sprite_type_name):
        if wrap_base.sprite_type_manager.has_sprite_type_name(sprite_type_name):
            return

        st = Sprite_type_factory.create_sprite_type_from_file(sprite_type_name,
                                                              settings.SPRITE_TYPES_PATH, False, False)
        if not st:
            st = Sprite_type_factory.create_sprite_type_from_file(sprite_type_name,
                                                                  settings.SPRITE_TYPES_PATH_ALT, False, False)

        if not st:
            err = _("Sprite {sprite_type_name} loading failed!")
            raise Exception(err.format(sprite_type_name=str(sprite_type_name)))

        wrap_base.sprite_type_manager.add_sprite_type(st, sprite_type_name)

    @staticmethod
    def remove_sprite(id):
        obj = wrap_base.sprite_id_manager.remove_by_id(id)
        if obj is not None:
            wrap_base.world.sprite_manager.remove_image_sprite(obj)

    @staticmethod
    def sprite_exists(id):
        obj = wrap_base.sprite_id_manager.get_obj_id(id)
        return obj is not None

    @staticmethod
    def add_sprite(sprite_type_name, x, y, visible=True, costume=None):
        # get sprite type
        cls._prepare_sprite_type(sprite_type_name)
        sprite_type = wrap_base.sprite_type_manager.get_sprite_type_by_name(sprite_type_name)
        if not sprite_type:
            err = _("Sprite {sprite_type_name} loading failed!")
            raise Exception(err.format(sprite_type_name=str(sprite_type_name)))

        # make sprite of sprite type
        sprite = Sprite_of_type(sprite_type, x, y, costume, visible)

        return cls._register_sprite(sprite)

    @staticmethod
    def add_text(x, y, text, visible=True, font_name="Arial", font_size=20,
                 bold=False, italic=False, underline=False,
                 text_color=(0, 0, 0),
                 back_color=None):
        sprite = Sprite_text(x, y, visible, text, font_name, font_size, bold, italic, underline, text_color, back_color,
                             angle=90)
        return cls._register_sprite(sprite)

    @staticmethod
    def get_sprite_width(id):
        return wsu._get_sprite_by_id(id).get_width_pix()

    @staticmethod
    def get_sprite_height(id):
        return wsu._get_sprite_by_id(id).get_height_pix()

    @staticmethod
    def get_sprite_size(id):
        return wsu._get_sprite_by_id(id).get_size_pix()

    @staticmethod
    def set_sprite_original_size(id):
        wsu._get_sprite_by_id(id).set_original_size()

    @staticmethod
    def change_sprite_size(id, width, height):
        wsu._get_sprite_by_id(id).change_size_pix(int(width), int(height))

    @staticmethod
    def change_sprite_width(id, width):
        wsu._get_sprite_by_id(id).change_width_pix(width)

    @staticmethod
    def change_sprite_height(id, height):
        wsu._get_sprite_by_id(id).change_height_pix(height)

    @staticmethod
    def change_width_proportionally(id, width, from_modified=False):
        wsu._get_sprite_by_id(id).change_width_pix_proportionally(width, from_modified)

    @staticmethod
    def change_height_proportionally(id, height, from_modified=False):
        wsu._get_sprite_by_id(id).change_height_pix_proportionally(height, from_modified)

    @staticmethod
    def get_sprite_width_proc(id):
        return wsu._get_sprite_by_id(id).get_width_proc()

    @staticmethod
    def get_sprite_height_proc(id):
        return wsu._get_sprite_by_id(id).get_height_proc()

    @staticmethod
    def get_sprite_size_proc(id):
        return wsu._get_sprite_by_id(id).get_size_proc()

    @staticmethod
    def change_sprite_size_proc(id, width, height):
        wsu._get_sprite_by_id(id).change_size_proc(int(width), int(height))

    @staticmethod
    def change_sprite_width_proc(id, width):
        wsu._get_sprite_by_id(id).change_width_proc(width)

    @staticmethod
    def change_sprite_height_proc(id, height):
        wsu._get_sprite_by_id(id).change_height_proc(height)

    @staticmethod
    def change_sprite_size_by_proc(id, proc):
        wsu._get_sprite_by_id(id).change_size_by_proc(proc)

    @staticmethod
    def get_sprite_flipx_reverse(id):
        return wsu._get_sprite_by_id(id).get_flipx_reverse()

    @staticmethod
    def get_sprite_flipy_reverse(id):
        return wsu._get_sprite_by_id(id).get_flipy_reverse()

    @staticmethod
    def set_sprite_flipx_reverse(id, flipx):
        return wsu._get_sprite_by_id(id).set_flipx_reverse(flipx)

    @staticmethod
    def set_sprite_flipy_reverse(id, flipy):
        return wsu._get_sprite_by_id(id).set_flipy_reverse(flipy)

    @staticmethod
    def set_sprite_angle(id, angle):
        wsu._get_sprite_by_id(id).set_angle_modification(angle)

    @staticmethod
    def get_sprite_angle(id):
        return wsu._get_sprite_by_id(id).get_angle_modification()

    @staticmethod
    def get_sprite_final_angle(id):
        return wsu._get_sprite_by_id(id).get_final_angle()

    @staticmethod
    def get_sprite_pos(id):
        return wsu._get_sprite_by_id(id).get_sprite_pos()

    @staticmethod
    def get_sprite_x(id):
        return wsu._get_sprite_by_id(id).get_sprite_pos()[0]

    @staticmethod
    def get_sprite_y(id):
        return wsu._get_sprite_by_id(id).get_sprite_pos()[1]

    @staticmethod
    def move_sprite_to(id, x, y):
        return wsu._get_sprite_by_id(id).move_sprite_to(x, y)

    @staticmethod
    def move_sprite_by(id, dx, dy):
        wsu._get_sprite_by_id(id).move_sprite_by(dx, dy)

    @staticmethod
    def get_left(id):
        return wsu._get_sprite_by_id(id).get_sprite_rect().left

    @staticmethod
    def get_right(id):
        return wsu._get_sprite_by_id(id).get_sprite_rect().right

    @staticmethod
    def get_top(id):
        return wsu._get_sprite_by_id(id).get_sprite_rect().top

    @staticmethod
    def get_bottom(id):
        return wsu._get_sprite_by_id(id).get_sprite_rect().bottom

    @staticmethod
    def get_centerx(id):
        return wsu._get_sprite_by_id(id).get_sprite_rect().centerx

    @staticmethod
    def get_centery(id):
        return wsu._get_sprite_by_id(id).get_sprite_rect().centery

    @staticmethod
    def set_left_to(id, left):
        wsu._get_sprite_by_id(id).set_left_to(left)

    @staticmethod
    def set_right_to(id, right):
        wsu._get_sprite_by_id(id).set_right_to(right)

    @staticmethod
    def set_top_to(id, top):
        wsu._get_sprite_by_id(id).set_top_to(top)

    @staticmethod
    def set_bottom_to(id, bottom):
        wsu._get_sprite_by_id(id).set_bottom_to(bottom)

    @staticmethod
    def set_centerx_to(id, centerx):
        wsu._get_sprite_by_id(id).set_centerx_to(centerx)

    @staticmethod
    def set_centery_to(id, centery):
        wsu._get_sprite_by_id(id).set_centery_to(centery)

    @staticmethod
    def is_sprite_visible(id):
        return wsu._get_sprite_by_id(id).get_visible()

    @staticmethod
    def show_sprite(id):
        wsu._get_sprite_by_id(id).set_visible(True)

    @staticmethod
    def hide_sprite(id):
        wsu._get_sprite_by_id(id).set_visible(False)

    @staticmethod
    def calc_point_by_angle_and_distance(id, angle, distance):
        return wsu._get_sprite_by_id(id).calc_point_by_angle_and_distance(angle, distance)

    @staticmethod
    def calc_angle_by_point(id, point):
        return wsu._get_sprite_by_id(id).calc_angle_by_point(point)

    @staticmethod
    def calc_angle_modification_by_angle(id, angle_to_look_to):
        return wsu._get_sprite_by_id(id).calc_angle_modification_by_angle(angle_to_look_to)


    @staticmethod
    def move_sprite_at_angle(id, angle, distance):
        wsu._get_sprite_by_id(id).move_sprite_at_angle(angle, distance)

    @staticmethod
    def move_sprite_to_angle(id, distance):
        wsu._get_sprite_by_id(id).move_sprite_to_angle(distance)

    @staticmethod
    def move_sprite_to_point(id, x, y, distance):
        wsu._get_sprite_by_id(id).move_sprite_to_point([x, y], distance)

    @staticmethod
    def rotate_to_angle(id, angle_to_look_to):
        wsu._get_sprite_by_id(id).rotate_to_angle(angle_to_look_to)

    @staticmethod
    def rotate_to_point(id, x, y):
        wsu._get_sprite_by_id(id).rotate_to_point([x, y])

    @staticmethod
    def sprite_collide_point(id, x, y, use_rect = False):
        sp = wsu._get_sprite_by_id(id)
        if use_rect:
            return sp.collide_point_rect(x, y)
        else:
            return sp.collide_point_mask(x, y)

    @staticmethod
    def sprites_collide(id1, id2):
        sp1 = wsu._get_sprite_by_id(id1)
        sp2 = wsu._get_sprite_by_id(id2)
        manager = wrap_base.get_sprite_manager()
        return manager.sprites_collide(sp1, sp2)

    @staticmethod
    def sprites_collide_any(sprite_id, sprite_id_list):
        sprite_list = wrap_base.sprite_id_manager.get_obj_list_by_id_list(sprite_id_list)
        sprite = _get_sprite_by_id(sprite_id)

        manager = wrap_base.get_sprite_manager()
        collided_sprite = manager.sprite_collide_any(sprite, sprite_list)
        if collided_sprite is None: return None

        collided_sprite_id = wrap_base.sprite_id_manager.get_obj_id(collided_sprite)
        return collided_sprite_id

    @staticmethod
    def sprites_collide_all(sprite_id, sprite_id_list):
        sprite_list = wrap_base.sprite_id_manager.get_obj_list_by_id_list(sprite_id_list)
        sprite = wsu._get_sprite_by_id(sprite_id)

        manager = wrap_base.get_sprite_manager()
        collided_sprite_list = manager.sprite_collide_all(sprite, sprite_list)
        return wrap_base.sprite_id_manager.get_id_list_by_obj_list(collided_sprite_list)

    ###################################################################################
    # methods related to sprites which was created from type
    @staticmethod
    def change_sprite_costume(id, costume_name, save_moving_angle=False, apply_proc_size=True):
        sprite = wsu._get_sprite_by_id(id, Sprite_of_type)
        if hasattr(sprite, "set_costume"):
            sprite.set_costume(costume_name, save_moving_angle, apply_proc_size)

    @staticmethod
    def set_next_costume(id, save_moving_angle=False, apply_proc_size=True):
        sprite = _get_sprite_by_id(id, Sprite_of_type)
        if hasattr(sprite, "set_costume_by_offset"):
            sprite.set_costume_by_offset(1, save_moving_angle, apply_proc_size)

    @staticmethod
    def set_previous_costume(id, save_moving_angle=False, apply_proc_size=True):
        sprite = wsu._get_sprite_by_id(id, Sprite_of_type)
        if hasattr(sprite, "set_costume_by_offset"):
            sprite.set_costume_by_offset(-1, save_moving_angle, apply_proc_size)

    @staticmethod
    def get_sprite_costume(id):
        sprite = wsu._get_sprite_by_id(id, Sprite_of_type)
        if hasattr(sprite, "get_sprite_costume"):
            return sprite.get_sprite_costume()

cls = wrap_sprite