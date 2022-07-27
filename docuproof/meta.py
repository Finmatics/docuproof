from threading import Lock
from typing import Any


class SingletonMeta(type):
    """
    Thread-safe implementation of Singleton.
    """

    _instances: dict = {}
    _lock: Lock = Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> None:
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
