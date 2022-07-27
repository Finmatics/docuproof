from datetime import datetime, timezone

import pytest
from pytest import MonkeyPatch

from docuproof.config import Config
from docuproof.utils import get_batch_threshold_dt


@pytest.mark.freeze_time("2022-07-01")
def test_batch_threshold_hour(monkeypatch: MonkeyPatch) -> None:
    with monkeypatch.context() as m:
        m.setattr(Config, "BATCH_TIME", 1)
        m.setattr(Config, "BATCH_TIME_UNIT", "hours")

        assert get_batch_threshold_dt() == datetime(2022, 6, 30, 23, 0, 0, tzinfo=timezone.utc)


@pytest.mark.freeze_time("2022-07-01")
def test_batch_threshold_day(monkeypatch: MonkeyPatch) -> None:
    with monkeypatch.context() as m:
        m.setattr(Config, "BATCH_TIME", 1)
        m.setattr(Config, "BATCH_TIME_UNIT", "days")

        assert get_batch_threshold_dt() == datetime(2022, 6, 30, 0, 0, 0, tzinfo=timezone.utc)
