# prepare translator for module strings
from wrap_py._transl import translator as _

from wrap_py import settings

from wrap_engine import  app, world, event_generator, message_broker, object_manager, sprite_type

world = world.World()
world.set_caption(_("Hello World!"))
world.set_icon(settings.ICON_FILE)

sprite_id_manager = object_manager.Object_manager()
sprite_type_manager = sprite_type.Sprite_types_manager()

broker = message_broker.Message_broker()
event_generator = event_generator.Event_generator(broker)

app = app.App(world, event_generator)

def get_sprite_manager():
    return world.sprite_manager