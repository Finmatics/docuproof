import uuid
from datetime import datetime

from tortoise import Model, fields
from tortoise.fields.relational import ForeignKeyFieldInstance, ReverseRelation

from docuproof.blockchain import DocuProofContract
from docuproof.ipfs import IPFSClient
from docuproof.utils import get_batch_threshold_dt


class TimestampMixin:
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Batch(TimestampMixin, Model):
    id = fields.BigIntField(pk=True)

    proof_id = fields.UUIDField(unique=True, default=uuid.uuid4)
    uploaded_at = fields.DatetimeField(null=True)

    files: ReverseRelation

    @staticmethod
    async def get_current_batch() -> "Batch":
        threshold_dt = get_batch_threshold_dt()
        if not (batch := await Batch.filter(created_at__gt=threshold_dt).first()):
            batch = await Batch.create()
        return batch

    async def upload(self) -> None:
        files = self.files.all()
        files_values = await files.values("uuid", "sha256")
        ipfs_hash = IPFSClient().upload_json(files_values)

        contract = DocuProofContract()
        contract.add_file(str(self.proof_id), ipfs_hash)

        self.uploaded_at = datetime.now()
        await self.save(update_fields=["uploaded_at"])


class File(TimestampMixin, Model):
    id = fields.BigIntField(pk=True)
    uuid = fields.UUIDField(unique=True)
    sha256 = fields.CharField(max_length=64)

    batch: ForeignKeyFieldInstance[Batch] = fields.ForeignKeyField(
        "models.Batch", related_name="files", on_delete=fields.RESTRICT
    )
