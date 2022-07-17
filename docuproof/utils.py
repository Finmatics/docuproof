from datetime import datetime, timedelta

from tortoise import timezone

from docuproof.config import Config


def get_batch_threshold_dt() -> datetime:
    timedelta_kwargs = {Config.BATCH_TIME_UNIT: Config.BATCH_TIME}
    return timezone.now() - timedelta(**timedelta_kwargs)
