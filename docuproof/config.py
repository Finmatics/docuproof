import os
from typing import Optional


def get_env_str(key: str, default: Optional[str] = None) -> Optional[str]:
    return os.environ.get(key, default)


def get_env_int(key: str, default: Optional[int] = None) -> Optional[int]:
    value = os.environ.get(key, default)
    if value is None:
        return None

    try:
        return int(value)
    except TypeError:
        return None


def get_env_list(key: str, default: list[str] = []) -> list[str]:
    value = os.environ.get(key, None)
    if value is None:
        return default

    return value.split(",")


def get_env_bool(key: str, default: bool = False) -> bool:
    value = os.environ.get(key)
    if value in ["1", "True", "true"]:
        return True
    elif value in ["0", "False", "false"]:
        return False
    return default


class Config:
    DATABASE_CONFIG = {
        "connections": {
            "default": get_env_str("DATABASE_URL", "sqlite://./sqlite.db"),
        },
        "apps": {
            "models": {
                "models": ["docuproof.models"],
                "default_connection": "default",
            }
        },
        "use_tz": True,
        "timezone": "UTC",
    }

    BATCH_TIME = get_env_int("BATCH_TIME", 1)
    BATCH_TIME_UNIT = get_env_str("BATCH_TIME_UNIT", "hours")
