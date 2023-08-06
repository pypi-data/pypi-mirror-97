from wrap_py import _event_handler_registrator as ehr

def vsegda(zaderzhka:int=100):
    """Команда будет выполняться каждые 100мс (10 раз в секунду).

Если указан параметр zaderzhka, то будет выполняться через указанное количество миллисекунд.
    """
    return ehr.always(zaderzhka)