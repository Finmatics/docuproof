import uuid
from datetime import datetime
from enum import IntEnum
from typing import Any

from tortoise import Model, fields
from tortoise.fields.relational import ForeignKeyFieldInstance, ReverseRelation

from docuproof.blockchain import DocuProofContract
from docuproof.ipfs import IPFSClient
from docuproof.utils import get_batch_threshold_dt


class TimestampMixin:
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Batch(TimestampMixin, Model):
    class Kind(IntEnum):
        UPLOAD = 1
        CACHE = 2

    id = fields.BigIntField(pk=True)

    proof_id = fields.UUIDField(unique=True, default=uuid.uuid4)
    uploaded_at = fields.DatetimeField(null=True)

    kind = fields.IntEnumField(Kind, default=Kind.UPLOAD)

    files: ReverseRelation

    @staticmethod
    async def get_current_batch() -> "Batch":
        threshold_dt = get_batch_threshold_dt()
        if not (batch := await Batch.filter(kind=Batch.Kind.UPLOAD, created_at__gt=threshold_dt).first()):
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

    @classmethod
    async def cache_json_data(cls, proof_id: str, data: dict[str, Any]) -> "Batch":
        batch = await cls.create(proof_id=proof_id, kind=cls.Kind.CACHE)
        files = []
        for item in data:
            files.append(File(batch=batch, uuid=item["uuid"], sha256=item["sha256"]))

        await File.bulk_create(files)
        return batch


class File(TimestampMixin, Model):
    id = fields.BigIntField(pk=True)
    uuid = fields.UUIDField(unique=True)
    sha256 = fields.CharField(max_length=64)

    batch: ForeignKeyFieldInstance[Batch] = fields.ForeignKeyField(
        "models.Batch", related_name="files", on_delete=fields.RESTRICT
    )
