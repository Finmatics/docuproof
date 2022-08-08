from datetime import datetime, timedelta
from urllib.parse import urlparse

from tortoise import timezone

from docuproof.config import Config


def get_batch_threshold_dt() -> datetime:
    timedelta_kwargs = {Config.BATCH_TIME_UNIT: Config.BATCH_TIME}
    return timezone.now() - timedelta(**timedelta_kwargs)


def convert_url_to_multiaddr(url: str) -> str:
    parsed_url = urlparse(url)
    return f"/dns/{parsed_url.hostname}/tcp/{parsed_url.port}/{parsed_url.scheme}"
