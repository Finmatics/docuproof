from tortoise import Model, fields

from docuproof.utils import get_batch_threshold_dt


class TimestampMixin:
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class File(TimestampMixin, Model):
    id = fields.BigIntField(pk=True)
    uuid = fields.UUIDField()
    sha256 = fields.CharField(max_length=64)

    batch = fields.ForeignKeyField("models.Batch", related_name="files", on_delete=fields.RESTRICT)


class Batch(TimestampMixin, Model):
    id = fields.BigIntField(pk=True)

    @staticmethod
    async def get_current_batch() -> "Batch":
        threshold_dt = get_batch_threshold_dt()
        if not (batch := await Batch.filter(created_at__gt=threshold_dt).first()):
            batch = await Batch.create()
        return batch

    async def upload(self) -> None:
        pass
