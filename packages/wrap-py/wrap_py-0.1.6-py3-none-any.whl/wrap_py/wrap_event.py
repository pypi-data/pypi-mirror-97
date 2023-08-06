import pygame
from wrap_py import wrap_base as wb

#anyone can assign hook in form func(callback).
#It will be called with func that going to be set as event handler.
#Result of func will be set as event handler instead of original func.
event_handler_hook = None


def _register_event_handler(func, delay=None, count=0, pygame_event_type_filter_data=None, key_codes=None,
                            control_keys=None, mouse_buttons=None):

    #call event handler hook
    if callable(event_handler_hook):
        patched_func = event_handler_hook(func)
    else:
        patched_func = func

    # start event notification
    event_type_id = wb.event_generator.start_event_notification(
        delay=delay, count=count, force_new=True,
        event_filter=pygame_event_type_filter_data,
        key_codes=key_codes,
        control_keys=control_keys,
        mouse_buttons=mouse_buttons
    )

    subs = wb.message_broker.Subscriber(event_type_id, patched_func, func)
    wb.broker.subscribe(subs)

    return event_type_id

def _stop_listening(event_type_id):
    wb.event_generator.stop_event_notification(event_type_id)
    wb.broker.ubsubscribe_by_event_type_id(event_type_id)

class wrap_event():


    #pygame event filter:
    #{pygame_event_attr: pygame_event_attr_val, ...} or
    #{pygame_event_attr: [pygame_event_attr_val], ...}
    #if attr not exists in event - filter not passed
    #if attr value not equals event value - filter not passed OR
    # if attr value not in event value list - filter not passed
    #
    # example:
    #{'type': pygame.KEYDOWN, 'key': [pygame.K_UP, pygame.K_w]}
    # filter only will work on keydown of key Up or 'w'
    @staticmethod
    def register_event_handler(func, delay=None, count=0, pygame_event_type_filter_data=None, key_codes=None,
                            control_keys=None, mouse_buttons=None):
        return _register_event_handler(func, delay, count, pygame_event_type_filter_data, key_codes,
                            control_keys, mouse_buttons)

    @staticmethod
    def stop_listening(event_type_id):
        _stop_listening(event_type_id)

    @staticmethod
    def on_timeout(delay, count, func):
        return _register_event_handler(
            func=func,
            delay=delay,
            count=count
        )

    @staticmethod
    def on_key_down(key, func):
        return _register_event_handler(
            func=func,
            pygame_event_type_filter_data={
                'type': pygame.KEYDOWN,
                'key': key
            })

    @staticmethod
    def on_key_pressed(keys, func, delay=100, control_keys=None):
        #must be iterable
        if not hasattr(keys, "__iter__"):
            keys = [keys]

        # must be iterable
        if control_keys is not None and \
                not hasattr(control_keys, "__iter__"):
            control_keys = [control_keys]

        return _register_event_handler(
            func=func,
            delay=delay,
            key_codes=keys,
            control_keys=control_keys
        )

    @staticmethod
    def on_mouse_pressed(buttons, func, delay=100, control_keys=None):
        # must be iterable
        if not hasattr(buttons, "__iter__"):
            buttons = [buttons]

        # must be iterable
        if control_keys is not None and \
                not hasattr(control_keys, "__iter__"):
            control_keys = [control_keys]

        return _register_event_handler(
            func=func,
            delay=delay,
            mouse_buttons=buttons,
            control_keys=control_keys
        )

    @staticmethod
    def on_close(func):
        global _on_quit_event_id

        if _on_quit_event_id is not None:
            _stop_listening(_on_quit_event_id)

        _on_quit_event_id = _register_event_handler(
            func=func,
            pygame_event_type_filter_data={'type': pygame.QUIT}
        )
        return _on_quit_event_id


#make window closable
_on_quit_event_id = None
def on_close_callback(**kwargs):
    exit()
wrap_event.on_close(on_close_callback)