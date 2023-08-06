from wrap_py import app


def ustanovit_fps(fps: int):
    """Устанавливает частоту кадров в игре"""

    app.set_fps(fps)


def zapusk():
    """Запускает игру.

    Работает только в режиме одопоточного приложения."""
    app.start()
