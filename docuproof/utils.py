from datetime import datetime, timedelta

from docuproof.config import config


def get_batch_threshold_dt() -> datetime:
    timedelta_kwargs = {config.BATCH_TIME_UNIT: config.BATCH_TIME}
    return datetime.now() - timedelta(**timedelta_kwargs)
