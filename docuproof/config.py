import os
from pathlib import Path
from typing import Optional

from jinja2 import Environment, FileSystemLoader


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
    BASE_DIR = Path(__file__).resolve().parent.parent

    RUN_BACKGROUND_TASKS = get_env_bool("RUN_BACKGROUND_TASKS", True)

    TEMPLATE_ENVIRONMENT = Environment(
        loader=FileSystemLoader(str(BASE_DIR / "docuproof" / "templates")),
        autoescape=True,
        enable_async=True,
    )

    DATABASE_CONFIG = {
        "connections": {
            "default": get_env_str("DATABASE_URL", f"sqlite://{BASE_DIR}/sqlite.db"),
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

    PRIVATE_ENDPOINTS_TOKEN = get_env_str("PRIVATE_ENDPOINTS_TOKEN")

    IPFS_API_ENDPOINT = get_env_str("IPFS_API_ENDPOINT")
    IPFS_ENDPOINT_USERNAME = get_env_str("IPFS_ENDPOINT_USERNAME")
    IPFS_ENDPOINT_PASSWORD = get_env_str("IPFS_ENDPOINT_PASSWORD")

    CONTRACT_ADDRESS = get_env_str("CONTRACT_ADDRESS")
    FROM_WALLET_ADDRESS = get_env_str("FROM_WALLET_ADDRESS")
    FROM_WALLET_PRIVATE_KEY = get_env_str("FROM_WALLET_PRIVATE_KEY")
    POA_BLOCKCHAIN = get_env_bool("POA_BLOCKCHAIN", False)
    BLOCKCHAIN_PROVIDER_URL = get_env_str("BLOCKCHAIN_PROVIDER_URL", "http://127.0.0.1:7545")
