from wrap_py import  wrap_base

class wrap_world():

    @staticmethod
    def create_world(width:int, height:int):
        """Creates screen with given sizes"""
        wrap_base.world.create_world(width, height)

    @staticmethod
    def change_world(width, height):
        wrap_base.world.change_world(width, height)

    @staticmethod
    def set_world_background_color(color):
        wrap_base.world.set_world_background_color(color)

    @staticmethod
    def set_world_background_color_rgb(r, g, b):
        wrap_base.world.set_world_background_color([r, g, b])

    @staticmethod
    def set_world_background_image(path_to_file, fill=False):
        wrap_base.world.set_world_background_image(path_to_file, fill)