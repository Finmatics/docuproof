from tortoise import Model, fields, transactions
from tortoise.fields.relational import ForeignKeyFieldInstance, ReverseRelation

from docuproof.blockchain import DocuProofContract
from docuproof.ipfs import IPFSClient
from docuproof.utils import get_batch_threshold_dt


class TimestampMixin:
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Batch(TimestampMixin, Model):
    id = fields.BigIntField(pk=True)

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
        files_uuids = await files.values_list("uuid", flat=True)
        ipfs_hash = IPFSClient().upload_json(files_values)

        contract = DocuProofContract()
        # TODO: Could use a lock on the files table to prevent concurrent adding
        # While the files are locked, check whether the files are already added to the blockchain
        # Pop the ones that are (if any) and add the rest
        contract.add_files([str(uuid) for uuid in files_uuids], ipfs_hash)

        # Death smiles at us all. All a man can do is smile back.
        async with transactions.in_transaction():
            await files.delete()
            await self.delete()


class File(TimestampMixin, Model):
    id = fields.BigIntField(pk=True)
    uuid = fields.UUIDField()
    sha256 = fields.CharField(max_length=64)

    batch: ForeignKeyFieldInstance[Batch] = fields.ForeignKeyField(
        "models.Batch", related_name="files", on_delete=fields.RESTRICT
    )
