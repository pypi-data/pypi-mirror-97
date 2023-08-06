from wrap_py import _wrap_sprite_utils as wsu
from wrap_engine.sprite_text import Sprite_text

class wrap_sprite_text():
    @staticmethod
    def is_sprite_text(id):
        sprite = wsu._get_sprite_by_id(id)
        return isinstance(sprite, Sprite_text)

    @staticmethod
    def get_font_name(id):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.get_font_name()

    @staticmethod
    def set_font_name(id, name):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.change_data(font_name=name)

    @staticmethod
    def get_font_size(id):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.get_font_size()

    @staticmethod
    def set_font_size(id, size):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.change_data(font_size=size)

    @staticmethod
    def get_font_bold(id):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.get_font_bold()

    @staticmethod
    def set_font_bold(id, bold):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.change_data(bold=bold)

    @staticmethod
    def get_font_italic(id):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.get_font_italic()

    @staticmethod
    def set_font_italic(id, italic):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.change_data(italic=italic)

    @staticmethod
    def get_font_underline(id):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.get_font_underline()

    @staticmethod
    def set_font_underline(id, underline):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.change_data(underline=underline)

    @staticmethod
    def get_text(id):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.get_text()

    @staticmethod
    def set_text(id, text):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.change_data(text=text)

    @staticmethod
    def get_text_color(id):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.get_text_color()

    @staticmethod
    def set_text_color(id, text_color):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.change_data(text_color=text_color)

    @staticmethod
    def get_back_color(id):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.get_back_color()

    @staticmethod
    def set_back_color(id, back_color):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.change_back_color(back_color)

    @staticmethod
    def get_pos(id):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.get_pos()

    @staticmethod
    def set_pos(id, pos):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.change_pos(pos)

    @staticmethod
    def get_angle(id):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.get_angle()

    @staticmethod
    def set_angle(id, pos):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.change_angle(pos)
    
cls = wrap_sprite_text