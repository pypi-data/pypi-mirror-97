#set module language
import wrap_py
from wrap_py import _transl
_transl.set_lang("ru_RU")

# translator for module strings
from wrap_py._transl import translator as _

#load pygame constants to use directly
from pygame.locals import *

#Say hi to user
wrap_py.say_hi()
#translate window title
wrap_py.app.set_title(_(wrap_py.app.get_title()))

#load modules for external usage
from wrap_py.ru import programma
from wrap_py.ru._event_handler_registrator import *

#init application
def podgotovka(tip_zapuska=wrap_py.SERVER_TYPE_THREAD):
    wrap_py.init(tip_zapuska)