import wrap_py
from wrap_py._transl import translator as _

event = wrap_py.event


def _reset_global_interfaces():
    global event
    event = wrap_py.event


def always(orig_func_or_delay=100):
    delay = 100

    def on_timer_handler(orig_func):
        event.register_event_handler(orig_func, delay=delay)
        return orig_func

    if callable(orig_func_or_delay):
        return on_timer_handler(orig_func_or_delay)
    else:
        delay = int(orig_func_or_delay)

    return on_timer_handler


def on_key_down(orig_func_or_key=None, *other_keys):
    keys = None

    def on_key_handler(orig_func):
        filter = {'type': wrap_py.KEYDOWN}
        if keys is not None:
            filter['key'] = [*keys]

        event.register_event_handler(orig_func, pygame_event_type_filter_data=filter)
        return orig_func

    if callable(orig_func_or_key):
        return on_key_handler(orig_func_or_key)
    elif orig_func_or_key is not None:
        keys = [orig_func_or_key, *other_keys]

    return on_key_handler

def on_key_up(orig_func_or_key=None, *other_keys):
    keys = None

    def on_key_handler(orig_func):
        filter = {'type': wrap_py.KEYUP}
        if keys is not None:
            filter['key'] = [*keys]

        event.register_event_handler(orig_func, pygame_event_type_filter_data=filter)
        return orig_func

    if callable(orig_func_or_key):
        return on_key_handler(orig_func_or_key)
    elif orig_func_or_key is not None:
        keys = [orig_func_or_key, *other_keys]

    return on_key_handler

def on_key_always(*keys, delay=50):
    keys = [*keys]

    def on_key_handler(orig_func):
        event.register_event_handler(orig_func, key_codes=keys, delay=delay)
        return orig_func

    return on_key_handler


def on_mouse_left(orig_func):
    filter = {'type': wrap_py.MOUSEBUTTONDOWN}
    filter['button'] = 1

    event.register_event_handler(orig_func, pygame_event_type_filter_data=filter)
    return orig_func

def on_mouse_right(orig_func):
    filter = {'type': wrap_py.MOUSEBUTTONDOWN}
    filter['button'] = 3

    event.register_event_handler(orig_func, pygame_event_type_filter_data=filter)
    return orig_func

def on_mouse_move(orig_func):
    filter = {'type': wrap_py.MOUSEMOTION}
    event.register_event_handler(orig_func, pygame_event_type_filter_data=filter)
    return orig_func

def on_mouse_down(orig_func_or_button=None, *other_buttons):
    buttons = None

    def on_button_handler(orig_func):
        filter = {'type': wrap_py.MOUSEBUTTONDOWN}
        if buttons is not None:
            filter['button'] = [*buttons]

        event.register_event_handler(orig_func, pygame_event_type_filter_data=filter)
        return orig_func

    if callable(orig_func_or_button):
        return on_button_handler(orig_func_or_button)
    elif orig_func_or_button is not None:
        buttons = [orig_func_or_button, *other_buttons]

    return on_button_handler

def on_mouse_up(orig_func_or_button=None, *other_buttons):
    buttons = None

    def on_button_handler(orig_func):
        filter = {'type': wrap_py.MOUSEBUTTONUP}
        if buttons is not None:
            filter['button'] = [*buttons]

        event.register_event_handler(orig_func, pygame_event_type_filter_data=filter)
        return orig_func

    if callable(orig_func_or_button):
        return on_button_handler(orig_func_or_button)
    elif orig_func_or_button is not None:
        buttons = [orig_func_or_button, *other_buttons]

    return on_button_handler

def on_close(orig_func):
    event.on_close(orig_func)
    return orig_func